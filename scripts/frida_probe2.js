'use strict';
// frida_probe2.js —— Frida 17 兼容版：抓启动自毁现场 + /proc 三件套重定向 + libDexHelper 采样点回溯
function findExport(name) {
  var cands = ["getGlobalExportByName", "findGlobalExportByName", "getExportByName", "findExportByName"];
  for (var i = 0; i < cands.length; i++) {
    try {
      if (cands[i].indexOf("Global") >= 0) { var r = Module[cands[i]](name); if (r) return r; }
      else { var r2 = Module[cands[i]](null, name); if (r2) return r2; }
    } catch (e) {}
  }
  return null;
}
var REDIRECT = {
  "/proc/version": "/data/local/tmp/fake_version",
  "/proc/cmdline": "/data/local/tmp/fake_cmdline",
  "/proc/cpuinfo": "/data/local/tmp/fake_cpuinfo"
};
var fakePtrs = {};
Object.keys(REDIRECT).forEach(function (k) { fakePtrs[k] = Memory.allocUtf8String(REDIRECT[k]); });

var ring = [];
function note(p) { ring.push(p); if (ring.length > 30) ring.shift(); }
function modInfo(a) {
  try { var m = Process.findModuleByAddress(a); if (m) return m.name + "+0x" + a.sub(m.base).toString(16); } catch (e) {}
  try { return String(DebugSymbol.fromAddress(a)); } catch (e) { return String(a); }
}
function btOf(ctx, n) {
  var out = [];
  try { var bt = Thread.backtrace(ctx, Backtracer.FUZZY); bt.slice(0, n).forEach(function (a, i) { out.push("#" + i + " " + a + " " + modInfo(a)); }); }
  catch (e) { out.push("btfail " + e); }
  return out;
}

var STALK = [];
var stalkerOn = false;

Process.setExceptionHandler(function (d) {
  var c = d.context || {};
  var L = ["=== CRASH " + d.type + " @ " + d.address + " tid=" + Process.getCurrentThreadId()];
  ["pc", "lr", "sp", "x0", "x1", "x8", "x19", "x20", "x21", "x22", "x23", "x24", "x25"].forEach(function (r) {
    if (c[r] !== undefined) L.push("  " + r + "=" + c[r] + " " + modInfo(c[r]));
  });
  L.push("  bt: " + btOf(c, 12).join(" ; "));
  L.push("  opens: " + ring.join(" | "));
  if (STALK.length) L.push("  stalk tail: " + STALK.slice(-60).map(function (x) { return x[0] + "->" + x[1]; }).join(" "));
  send("CRASHREPORT\n" + L.join("\n"));
  return false;
});

["open", "open64", "openat", "openat64"].forEach(function (name) {
  var p = findExport(name);
  if (!p) { send("HOOKMISS " + name); return; }
  Interceptor.attach(p, {
    onEnter: function (args) {
      var idx = (name === "open" || name === "open64") ? 0 : 1;
      try {
        var path = args[idx].readCString();
        if (!path) return;
        note(path);
        if (REDIRECT.hasOwnProperty(path)) { send("REDIRECT " + path); args[idx] = fakePtrs[path]; }
      } catch (e) {}
    }
  });
});

// 采样点：崩溃现场 x22 = libDexHelper.so+0xe63ca
try {
  var m = Process.findModuleByName("libDexHelper.so");
  if (m) {
    var t = m.base.add(0xe63ca);
    Interceptor.attach(t, { onEnter: function () { send("SAMPLE_HIT libDexHelper+0xe63ca bt=" + btOf(this.context, 14).join(" ; ")); } });
    send("ATTACHED sample " + t);
  } else { send("NO libDexHelper"); }
} catch (e) { send("sample fail " + e); }

// Stalker call 轨迹（只在主动开启时）
rpc.exports = {
  stalkstart: function () {
    if (stalkerOn) return "already";
    stalkerOn = true;
    Stalker.follow(Process.getCurrentThreadId(), {
      events: { call: true },
      onReceive: function (ev) {
        try {
          var e = Stalker.parse(ev, { annotate: false, stringify: false });
          for (var i = 0; i < e.length; i++) {
            if (e[i][0] === "call") {
              var tgt = e[i][1];
              STALK.push([modInfo(ptr(e[i][2])), modInfo(tgt)]);
              if (STALK.length > 400) STALK.shift();
            }
          }
        } catch (e2) {}
      }
    });
    return "on";
  }
};
send("READY probe2");
