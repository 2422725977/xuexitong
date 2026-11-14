'use strict';
const libc = Process.getModuleByName("libc.so");
function ex(n){ try { return libc.findExportByName(n); } catch(e){ return null; } }
function hook(name, cb){
  const a = ex(name);
  if (!a) { send({t:'miss', n:name}); return; }
  try { Interceptor.attach(a, cb); send({t:'hook', n:name}); } catch(e) { send({t:'err', n:name, e:String(e)}); }
}
const seenFind = {};
hook('__system_property_get', {
  onEnter(args){ this.n = args[0].readCString(); this.vp = args[1]; },
  onLeave(ret){ try { if (this.n) send({t:'prop', n:this.n, v: this.vp ? this.vp.readCString() : null}); } catch(e){} }
});
hook('__system_property_find', {
  onEnter(args){ try { const n = args[0].readCString(); if (n && !seenFind[n]) { seenFind[n]=1; send({t:'find', n:n}); } } catch(e){} }
});
const PAT = /proc|qemu|goldfish|ranchu|frida|magisk|selinux|build\.prop|tombstone|emulator|\/dev\/|superuser|busybox|xposed|substrate|maps|status|cmdline/i;
function pathHook(name, idx){
  hook(name, { onEnter(args){ try { const p = args[idx].readCString(); if (p && PAT.test(p)) send({t:name, p:p}); } catch(e){} } });
}
['open','openat','access','faccessat','stat','lstat','statx','opendir','readlink','readlinkat','fopen','fopen64'].forEach(n=>pathHook(n, (n==='openat'||n==='faccessat'||n==='readlinkat')?1:0));
send({t:'ready', pid: Process.id, arch: Process.arch});
