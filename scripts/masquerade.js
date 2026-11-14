'use strict';
// masquerade.js v2 - hide emulator/frida fingerprints for Bangcle DexHelper + full crash diagnostics.
const SPOOF = {
  "ro.kernel.qemu": "0", "ro.boot.qemu": "0", "ro.hardware": "qcom", "ro.boot.hardware": "qcom",
  "ro.boot.hardware.platform": "qcom", "ro.product.model": "Pixel 5", "ro.product.brand": "google",
  "ro.product.manufacturer": "Google", "ro.product.name": "redfin", "ro.product.device": "redfin",
  "ro.product.board": "redfin", "ro.build.tags": "release-keys", "ro.build.type": "user",
  "ro.build.user": "android-build", "ro.build.host": "abfarm", "ro.build.flavor": "redfin-user",
  "ro.build.display.id": "RQ3A.210805.001.A1", "ro.build.id": "RQ3A.210805.001.A1",
  "ro.build.fingerprint": "google/redfin/redfin:11/RQ3A.210805.001.A1/7474174:user/release-keys",
  "ro.build.description": "redfin-user 11 RQ3A.210805.001.A1 7474174 release-keys",
  "ro.debuggable": "0", "ro.secure": "1", "ro.adb.secure": "1", "ro.bootloader": "unknown",
  "ro.boot.verifiedbootstate": "green", "ro.boot.flash.locked": "1", "ro.serialno": "0C071FQ2G0000",
  "ro.boot.serialno": "0C071FQ2G0000", "ro.bootmode": "unknown", "ro.boot.veritymode": "enforcing",
  "ro.build.version.security_patch": "2021-08-05", "ro.build.version.sdk": "30",
  "ro.build.version.release": "11", "ro.product.first_api_level": "30", "ro.treble.enabled": "true",
  "ro.bluetooth.hfp.ver": "1.7", "gsm.version.ril-impl": "android reference-ril 1.0",
  "qemu.hw.mainkeys": "0", "ro.dalvik.vm.native.bridge": "0", "ro.kernel.qemu.gles": "0",
  "ro.boot.qemu.avd_name": "", "vendor.qemu.hwc": "", "ro.hardware.egl": "adreno",
  "ro.hardware.vulkan": "adreno", "ro.board.platform": "msmnile", "ro.soc.model": "SM8150",
  "ro.soc.manufacturer": "QTI", "ro.build.characteristics": "default",
  "ro.vendor.build.tags": "release-keys", "ro.system.build.tags": "release-keys",
  "ro.product.build.tags": "release-keys", "ro.odm.build.tags": "release-keys",
  "ro.vendor.build.type": "user", "ro.system.build.type": "user",
  "ro.boot.qemu.initrd": "", "ro.boot.qemu.kernel": "", "ro.boot.qemu.ramdisk": ""
};
const BAD = ["qemu", "goldfish", "ranchu", "genymotion", "bluestacks", "nox", "vbox", "ttvm", "frida",
  "xposed", "magisk", "substrate", "droidbox", "cuckoo", "vmos", "microvirt", "windroy", "andy_",
  "waydroid", "redroid", "anbox", "tracerpid"];
const REDIRECT = {
  "/proc/version": "/data/data/com.chaoxing.mobile/files/.fake_version",
  "/proc/cpuinfo": "/data/data/com.chaoxing.mobile/files/.fake_cpuinfo"
};
function has(o, k) { return Object.prototype.hasOwnProperty.call(o, k); }
function log(m) { try { send({ type: "log", msg: String(m) }); } catch (e) {} }
function sym(moduleName, name) { try { return Process.getModuleByName(moduleName).findExportByName(name); } catch (e) { return null; } }
function symAny(names) {
  const mods = ["libc.so", "libdl.so", "liblog.so", "libart.so", "linker64"];
  for (const n of names) for (const m of mods) { const a = sym(m, n); if (a) return a; }
  return null;
}
function modName(a) {
  const m = Process.findModuleByAddress(a);
  return m ? m.name + "+0x" + a.sub(m.base).toString(16) : a.toString();
}
function bt(ctx, n) {
  try {
    return Thread.backtrace(ctx, Backtracer.ACCURATE).slice(0, n || 10).map(modName).join(" | ");
  } catch (e) { return "bt-error:" + e; }
}
function badPath(p) {
  if (!p) return false;
  const s = p.toLowerCase();
  for (let i = 0; i < BAD.length; i++) if (s.indexOf(BAD[i]) >= 0) return true;
  return false;
}
function installDiagnostics() {
  try {
    Process.setExceptionHandler(function (d) {
      const ctx = d.context || {};
      const pc = ctx.pc || ptr(0);
      log("### EXCEPTION type=" + d.type + " addr=" + d.address + " pc=" + modName(pc) + " lr=" + modName(ctx.lr || ptr(0)));
      log("### BT: " + bt(ctx, 14));
      try { log("### lastsend=" + JSON.stringify(d.lastError || null)); } catch (e) {}
      return false;
    });
    log("exception handler installed");
  } catch (e) { log("exc handler failed " + e); }
  const exits = [["libc.so", "exit"], ["libc.so", "_exit"], ["libc.so", "abort"], ["libc.so", "kill"],
    ["libc.so", "tgkill"], ["libc.so", "raise"], ["libc.so", "pthread_kill"], ["libc.so", "pthread_exit"],
    ["libc.so", "quick_exit"], ["libc.so", "android_set_abort_message"]];
  for (const [m, n] of exits) {
    const a = sym(m, n);
    if (!a) continue;
    try {
      Interceptor.attach(a, {
        onEnter(args) {
          let extra = "";
          try {
            if (n === "kill" || n === "tgkill") extra = " pid=" + args[0] + " sig=" + (n === "kill" ? args[1] : args[2]);
            else if (n === "android_set_abort_message") extra = " msg=" + args[0].readCString();
          } catch (e) {}
          log("### CALL " + n + "()" + extra + " from " + modName(this.returnAddress) + " BT: " + bt(this.context, 8));
        }
      });
    } catch (e) {}
  }
  log("exit/abort hooks installed");
  const logp = sym("liblog.so", "__android_log_print") || sym("liblog.so", "__android_log_write");
  if (logp) {
    try {
      Interceptor.attach(logp, {
        onEnter(args) {
          try {
            const tag = args[1].readCString();
            const fmt = args[2].readCString();
            log("LOG[" + tag + "] " + fmt);
          } catch (e) {}
        }
      });
      log("__android_log_print hooked");
    } catch (e) { log("log hook failed " + e); }
  }
  for (const n of ["android_dlopen_ext", "dlopen"]) {
    const a = symAny([n]);
    if (!a) continue;
    try {
      Interceptor.attach(a, {
        onEnter(args) { try { log("dlopen(" + args[0].readCString() + ") from " + modName(this.returnAddress)); } catch (e) {} }
      });
    } catch (e) {}
  }
  log("dlopen hooks installed");
}
function installPropertyHooks() {
  try {
    const g = sym("libc.so", "__system_property_get");
    if (!g) throw new Error("no __system_property_get");
    Interceptor.attach(g, {
      onEnter(args) { this.k = args[0].readCString(); this.buf = args[1]; },
      onLeave(ret) {
        const k = this.k;
        if (k && has(SPOOF, k)) { const v = SPOOF[k]; try { this.buf.writeUtf8String(v); ret.replace(ptr(v.length)); } catch (e) {} }
      }
    });
    log("hook __system_property_get ok");
  } catch (e) { log("hook prop_get failed: " + e); }
  try {
    const rc = sym("libc.so", "__system_property_read_callback");
    if (!rc) throw new Error("no read_callback");
    Interceptor.attach(rc, {
      onEnter(args) {
        const orig = args[1];
        const cb = new NativeCallback(function (cookie, name, value, serial) {
          let useVal = value;
          try { const n = name.readCString(); if (n && has(SPOOF, n)) useVal = Memory.allocUtf8String(SPOOF[n]); } catch (e) {}
          orig(cookie, name, useVal, serial);
        }, "void", ["pointer", "pointer", "pointer", "uint"]);
        args[1] = cb;
      }
    });
    log("hook __system_property_read_callback ok");
  } catch (e) { log("hook read_callback failed: " + e); }
}
function installFileHooks() {
  const names = ["open", "openat", "access", "faccessat", "stat", "lstat", "fstatat", "statx", "__xstat", "opendir", "readlinkat", "readlink"];
  let n = 0;
  for (const name of names) {
    const addr = symAny([name]);
    if (!addr) continue;
    try {
      Interceptor.attach(addr, {
        onEnter(args) {
          this.blocked = false; this.logged = false;
          let p = null;
          try {
            if (name === "open" || name === "access" || name === "stat" || name === "lstat" || name === "__xstat" || name === "opendir" || name === "readlink") p = args[0].readCString();
            else p = args[1].readCString();
          } catch (e) { return; }
          if (!p) return;
          if (badPath(p)) { this.blocked = true; this.p = p; return; }
          if (has(REDIRECT, p)) {
            const t = Memory.allocUtf8String(REDIRECT[p]);
            if (name === "open" || name === "access" || name === "stat" || name === "lstat" || name === "__xstat" || name === "opendir" || name === "readlink") args[0] = t;
            else args[1] = t;
            this.logged = true; this.p = p;
          }
        },
        onLeave(ret) {
          if (this.blocked) { log("HIDE " + this.p + " (deny " + name + ")"); ret.replace(ptr(-1)); }
          else if (this.logged) log("REDIR " + this.p);
        }
      });
      n++;
    } catch (e) {}
  }
  log("file hooks installed: " + n);
}
function installJavaHooks() {
  try {
    Java.perform(function () {
      const props = Java.use("android.os.SystemProperties");
      props.get.overload("java.lang.String", "java.lang.String").implementation = function (k, d) { return has(SPOOF, k) ? SPOOF[k] : this.get(k, d); };
      props.get.overload("java.lang.String").implementation = function (k) { return has(SPOOF, k) ? SPOOF[k] : this.get(k); };
      const fields = { MODEL: "Pixel 5", BRAND: "google", MANUFACTURER: "Google", DEVICE: "redfin", PRODUCT: "redfin", HARDWARE: "redfin", BOARD: "redfin", FINGERPRINT: SPOOF["ro.build.fingerprint"], TAGS: "release-keys", TYPE: "user", HOST: "abfarm", ID: "RQ3A.210805.001.A1", DISPLAY: "RQ3A.210805.001.A1", BOOTLOADER: "unknown" };
      for (const f in fields) { try { Java.use("android.os.Build")[f].value = fields[f]; } catch (e) {} }
      log("java hooks ok");
    });
  } catch (e) { log("java hooks failed: " + e); }
}
function scanDex(minSize, maxTotal) {
  const MAGIC = "64 65 78 0a 30 33 35 00";
  const out = [];
  let bytes = 0, scanned = 0;
  const ranges = Process.enumerateRanges("r--").concat(Process.enumerateRanges("rw-"));
  for (const r of ranges) {
    if (r.size < 0x100) continue;
    if (r.file && r.file.path && r.size > 0x200000) continue;
    if (bytes > maxTotal) break;
    scanned++; bytes += r.size;
    let hits = [];
    try { hits = Memory.scanSync(r.base, r.size, MAGIC); } catch (e) { continue; }
    for (const h of hits) {
      try {
        const base = h.address;
        const size = base.add(0x20).readU32();
        const hsz = base.add(0x24).readU32();
        const endian = base.add(0x28).readU32();
        const mapOff = base.add(0x34).readU32();
        if (size < minSize || size > 0x20000000) continue;
        if (hsz !== 0x70 || endian !== 0x12345678) continue;
        if (mapOff < 0x70 || mapOff >= size) continue;
        out.push({ base: base.toString(), size: size });
      } catch (e) {}
    }
  }
  log("scan done: ranges=" + scanned + " bytes=" + bytes + " cands=" + out.length);
  return { ranges: scanned, bytes: bytes, cands: out };
}
rpc.exports = {
  ping: function () { return { ok: true, t: Date.now(), pid: Process.id }; },
  scan: function (minSize, maxTotal) { return scanDex(minSize || 0x70, maxTotal || 0x60000000); },
  grab: function (addr, size, label) {
    send({ type: "dex", name: label || ("dex_" + addr) }, Memory.readByteArray(ptr(addr), size));
    return true;
  },
  info: function () {
    return Process.enumerateModules().filter(function (m) { return /DexHelper|dexjni|encrypt|RiskStub|secneo/i.test(m.name); })
      .map(function (m) { return { name: m.name, base: m.base.toString(), size: m.size }; });
  }
};
installDiagnostics();
installPropertyHooks();
installFileHooks();
if (typeof Java !== "undefined") installJavaHooks(); else log("no java bridge (frida 17), native-only");
setInterval(function () { try { send({ type: "hb", t: Date.now() }); } catch (e) {} }, 1000);
log("masquerade v2 ready");
