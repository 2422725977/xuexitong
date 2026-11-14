/* anti_anti.js — keep 学习通 (Bangcle everisk) alive on emulator + expose unpack timing
 * 用法: frida -U -f com.chaoxing.mobile -l anti_anti.js --no-pause
 */
'use strict';

function log(m) { console.log('[aa] ' + m); }

Java.perform(function () {
  try {
    var Debug = Java.use('android.os.Debug');
    Debug.isDebuggerConnected.implementation = function () { return false; };
    Debug.waitingForDebugger.implementation = function () { return false; };
    log('Debug hooked');
  } catch (e) { log('Debug: ' + e); }

  try {
    var Props = Java.use('android.os.SystemProperties');
    var origGet = Props.get.overload('java.lang.String');
    origGet.implementation = function (k) {
      if (k && k.indexOf('qemu') >= 0) return '0';
      if (k && k.indexOf('ro.build.tags') >= 0) return 'release-keys';
      return origGet.call(this, k);
    };
    log('SystemProperties hooked');
  } catch (e) { log('Props: ' + e); }

  try {
    var Process = Java.use('android.os.Process');
    Process.killProcess.implementation = function (pid) { log('killProcess(' + pid + ') swallowed'); };
    log('Process hooked');
  } catch (e) { log('Process: ' + e); }

  try {
    var Sys = Java.use('java.lang.System');
    Sys.exit.implementation = function (c) { log('System.exit(' + c + ') swallowed'); };
    log('System hooked');
  } catch (e) { log('System: ' + e); }
});

try {
  var ptrace = Module.findExportByName(null, 'ptrace');
  if (ptrace) {
    Interceptor.replace(ptrace, new NativeCallback(function () { return 0; }, 'long', []));
    log('ptrace replaced');
  }
} catch (e) { log('ptrace: ' + e); }

['libDexHelper.so', 'libdexjni.so', 'libencrypt.so'].forEach(function (n) {
  var m = Process.findModuleByName(n);
  log('module ' + n + ' -> ' + (m ? m.base + ' size=' + m.size : 'not loaded yet'));
});

try {
  var dlopen = Module.findExportByName(null, 'android_dlopen_ext') || Module.findExportByName(null, 'dlopen');
  if (dlopen) {
    Interceptor.attach(dlopen, {
      onEnter: function (a) { try { var s = a[0].readCString(); if (s) log('dlopen ' + s); } catch (e) {} }
    });
    log('dlopen traced');
  }
} catch (e) { log('dlopen: ' + e); }
