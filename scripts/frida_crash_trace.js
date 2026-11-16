'use strict';
// frida_crash_trace.js —— 捕获学习通启动自毁（SIGSEGV）现场：pc/lr/sp + 模块偏移 + 回溯 +
// 把 /proc/version、/proc/cmdline、/proc/cpuinfo 重定向到假文件（frida 层 open/openat 改路径）。
var REDIRECT = {
  "/proc/version": "/data/local/tmp/fake_version",
  "/proc/cmdline": "/data/local/tmp/fake_cmdline",
  "/proc/cpuinfo": "/data/local/tmp/fake_cpuinfo",
  "/sys/class/net/wlan0/address": null
};
var fakePtrs = {};
Object.keys(REDIRECT).forEach(function (k) { if (REDIRECT[k]) fakePtrs[k] = Memory.allocUtf8String(REDIRECT[k]); });

var ring = [];
function note(p) { ring.push(p); if (ring.length > 40) ring.shift(); }

function modInfo(addr) {
  try {
    var m = Process.findModuleByAddress(addr);
    if (m) return m.name + "+0x" + addr.sub(m.base).toString(16);
  } catch (e) {}
  try { return String(DebugSymbol.fromAddress(addr)); } catch (e) { return String(addr); }
}

Process.setExceptionHandler(function (d) {
  var c = d.context || {};
  var lines = [];
  lines.push("=== CRASH " + d.type + " at " + d.address + " ===");
  ["pc", "lr", "sp", "x0", "x1", "x8", "x19", "x20", "x21", "x22", "x23", "x24", "x25"].forEach(function (r) {
    if (c[r] !== undefined) lines.push("  " + r + " = " + c[r] + "   " + modInfo(c[r]));
  });
  try {
    var bt = Thread.backtrace(c, Backtracer.ACCURATE);
    lines.push("  backtrace(" + bt.length + "):");
    bt.slice(0, 16).forEach(function (a, i) { lines.push("    #" + i + " " + a + " " + modInfo(a)); });
  } catch (e) { lines.push("  backtrace failed: " + e); }
  lines.push("  last opens: " + ring.join(" | "));
  send("CRASHREPORT " + lines.join("\n"));
  return false;
});

function hookOpen(name) {
  var p = Module.findExportByName("libc.so", name);
  if (!p) { send("HOOK miss " + name); return; }
  Interceptor.attach(p, {
    onEnter: function (args) {
      var idx = (name === "open" || name === "open64") ? 0 : 1;
      try {
        var path = args[idx].readCString();
        if (!path) return;
        note(path);
        if (REDIRECT.hasOwnProperty(path) && fakePtrs[path]) {
          send("REDIRECT " + path + " -> " + REDIRECT[path]);
          args[idx] = fakePtrs[path];
        }
      } catch (e) {}
    }
  });
}
["open", "open64", "openat", "openat64"].forEach(hookOpen);
send("READY crash-trace installed, redirect=" + JSON.stringify(Object.keys(REDIRECT)));
