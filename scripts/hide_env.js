'use strict';
/* hide_env.js — 梆梆 SecNeo(com.secneo.apkwrapper) 启动自毁绕过 + 诊断
   frida -U -f com.chaoxing.mobile -l hide_env.js
   症状：启动 ~1s 后 tid 与主线程同名的子线程 SIGSEGV，pc=0x3dc lr=0 sp=0（跳空），
        崩溃前该线程读过 /proc/version 与 /proc/self/maps，寄存器里带 "emulator" 串。 */
const CFG = { spoof_props:true, sanitize_files:true, block_paths:true, neutral_strstr:true, log:false };

const FAKE_PROPS = {
  'ro.product.model':'SM-G975F', 'ro.product.device':'beyond2', 'ro.product.board':'{{SECRET_fl4x0r2s}}',
  'ro.product.brand':'samsung', 'ro.product.manufacturer':'samsung', 'ro.product.name':'beyond2lte',
  'ro.hardware':'{{SECRET_fl4x0r2s}}', 'ro.boot.hardware':'{{SECRET_fl4x0r2s}}',
  'ro.kernel.qemu':'0', 'ro.boot.qemu':'0', 'ro.boot.qemu.avd_name':'',
  'ro.build.fingerprint':'samsung/beyond2lte/beyond2:11/RP1A.200720.012/G975FXXU9FUBD:user/release-keys',
  'ro.build.type':'user', 'ro.build.tags':'release-keys', 'ro.debuggable':'0', 'ro.secure':'1',
  'ro.bootmode':'unknown', 'ro.boot.verifiedbootstate':'green', 'ro.boot.veritymode':'enforcing',
  'ro.serialno':'R58M12ABCDE', 'ro.boot.serialno':'R58M12ABCDE'
};
const SUBST = [
  ['emulator','exynos98'], ['Emulator','Exynos98'], ['EMULATOR','EXYNOS98'],
  ['qemu_pipe','cleanpipe'], ['qemu','none'], ['QEMU','NONE'],
  ['goldfish','exynos98'], ['ranchu','beyond'], ['frida','tride'], ['magisk','masixx'],
  ['genymotion','genymot10x'], ['bluestacks','bluestack1'], ['/data/local/tmp','/data/local/xyz']
];
const BAD_STR = ['emulator','qemu','goldfish','ranchu','frida','magisk','genymotion','bluestacks','ttvm','nox_','vbox'];
const BLOCK_PATH = ['/dev/qemu_pipe','/dev/goldfish','/sys/qemu_trace','/system/bin/qemud','libc_malloc_debug_qemu',
  '/data/local/tmp','/data/adb','/system/xbin/su','/system/bin/su','/sbin/su','/system/xbin/daemonsu',
  'frida-server','/proc/self/attr'];

function H(n){ try { return Process.getModuleByName('libc.so').getExportByName(n); } catch(e){} try { return Module.getGlobalExportByName(n); } catch(e){ return null; } }
function W(m){ console.log('[watch] '+m); }
function isBadStr(s){ if(!s) return false; const l=s.toLowerCase(); if(l.length<4) return false; for(const b of BAD_STR){ if(l.indexOf(b)>=0) return true; } return false; }
function isBadPath(p){ for(const b of BLOCK_PATH){ if(p.indexOf(b)>=0) return true; } return false; }

/* ---------- 1. 属性 ---------- */
const gsp = H('__system_property_get');
if (gsp) Interceptor.attach(gsp, {
  onEnter(a){ try{ this.n=a[0].readCString(); }catch(e){ this.n=null; } this.buf=a[1];
    if (this.n) W('propget '+this.n); },
  onLeave(r){ if(!this.n) return; const v = CFG.spoof_props ? FAKE_PROPS[this.n] : undefined;
    if (v!==undefined){ try{ this.buf.writeUtf8String(v); r.replace(v.length); }catch(e){ W('prop-spoof-fail '+this.n); } } }
});
const gpc = H('__system_property_read_callback');
if (gpc) Interceptor.attach(gpc, { onEnter(a){ try{ this.n=a[0].readCString(); }catch(e){ this.n=null; } },
  onLeave(){ if (this.n && CFG.log) W('prop-cb '+this.n); } });

/* ---------- 2. 打开文件：记录 fd->path，拦掉 qemu/root 痕迹 ---------- */
const FD = {};
function noteFd(fd, path){ if (fd>=0){ FD[fd]=path; } }
function hookOpen(name, isAt){
  const a=H(name); if(!a) return;
  Interceptor.attach(a, {
    onEnter(args){ const p = isAt ? args[1] : args[0]; try{ this.path=p.readCString(); }catch(e){ this.path=null; } },
    onLeave(r){ const p=this.path; if(!p) return; const fd=r.toInt32();
      if (isBadPath(p)){
        if (CFG.block_paths){ W('BLOCK '+name+' '+p); try{ r.replace(-1); }catch(e){} return; }
      }
      if (fd>=0){ noteFd(fd,p); if (/^\/proc|^\/sys|^\/dev|qemu|frida|maps|version|cpuinfo/.test(p)) W(name+' '+p+' fd='+fd); }
    }
  });
}
['open','openat','open64','openat64'].forEach(n=>hookOpen(n, n.indexOf('at')>=0));
const fopenP = H('fopen'); const filenoF = H('fileno');
const _fileno = filenoF ? new NativeFunction(filenoF, 'int', ['pointer']) : null;
if (fopenP) Interceptor.attach(fopenP, {
  onEnter(a){ try{ this.path=a[0].readCString(); }catch(e){ this.path=null; } },
  onLeave(r){ if(!this.path) return;
    if (isBadPath(this.path) && CFG.block_paths){ W('BLOCK fopen '+this.path); try{ r.replace(ptr(0)); }catch(e){} return; }
    if (!r.isNull() && _fileno){ try { const fd=_fileno(r); noteFd(fd,this.path); W('fopen '+this.path+' fd='+fd); } catch(e){} } }
});
['access','stat','stat64','lstat','opendir'].forEach(n=>{ const a=H(n); if(!a) return;
  const isAccess = (n==='access'||n==='opendir');
  Interceptor.attach(a, { onEnter(args){ try{ this.path=args[0].readCString(); }catch(e){ this.path=null; } },
    onLeave(r){ if (this.path && isBadPath(this.path) && CFG.block_paths){ W('BLOCK '+n+' '+this.path); try{ r.replace(-1); }catch(e){} } } });
});

/* ---------- 3. read/fread 就地洗掉 qemu/emulator 串 ---------- */
function sanitizePtr(p, len){
  let buf; try { buf = new Uint8Array(p.readByteArray(len)); } catch(e){ return; }
  let s=''; for (let i=0;i<buf.length;i++) s += String.fromCharCode(buf[i]);
  let hit=null;
  for (const [a,b] of SUBST){ if (s.indexOf(a)>=0){ if(!hit) hit=a; s = s.split(a).join(b); } }
  if (!hit) return;
  for (let i=0;i<buf.length;i++) buf[i]=s.charCodeAt(i)&0xff;
  try{ p.writeByteArray(buf.buffer); W('SANITIZE('+hit+') '+len+'B'); }catch(e){}
}
['read','pread','pread64'].forEach(n=>{ const a=H(n); if(!a) return;
  Interceptor.attach(a, { onEnter(args){ this.fd=args[0].toInt32(); this.buf=args[1]; this.n=args[2].toInt32(); this.path=FD[this.fd]; },
    onLeave(r){ const n=r.toInt32(); if (n>0 && CFG.sanitize_files && this.path && /^\/proc|^\/sys|^\/dev/.test(this.path)) sanitizePtr(this.buf, Math.min(n, this.n)); } });
});
const freadP = H('fread');
if (freadP) Interceptor.attach(freadP, { onEnter(a){ this.p=a[0]; this.sz=a[1].toInt32(); this.nm=a[2].toInt32(); },
  onLeave(r){ const n=r.toInt32(); if (n>0 && CFG.sanitize_files) sanitizePtr(this.p, Math.min(n*this.sz, this.sz*this.nm)); } });

/* ---------- 4. strstr 类：坏针直接返回 NULL ---------- */
['strstr','strcasestr','strnstr'].forEach(n=>{ const a=H(n); if(!a) return;
  Interceptor.attach(a, { onEnter(args){ try{ this.needle=args[1].readCString(); }catch(e){ this.needle=null; } },
    onLeave(r){ if (this.needle){ W('strstr needle='+this.needle+(isBadStr(this.needle)?' <BAD>':'')); if (isBadStr(this.needle) && CFG.neutral_strstr) try{ r.replace(ptr(0)); }catch(e){} } } });
});
['strcmp','strcasecmp','strncmp'].forEach(n=>{ const a=H(n); if(!a) return;
  Interceptor.attach(a, { onEnter(args){ try{ this.a=args[0].readCString(); this.b=args[1].readCString(); }catch(e){ this.a=null; } },
    onLeave(){ if (this.a && (isBadStr(this.a)||isBadStr(this.b)) && CFG.log) W('strcmp "'+this.a+'" vs "'+this.b+'"'); } });
});

/* ---------- 5. 加载/线程/映射观测 ---------- */
['dlopen','android_dlopen_ext'].forEach(n=>{ const a=H(n); if(!a) return;
  Interceptor.attach(a, { onEnter(args){ try{ W(n+' '+args[0].readCString()); }catch(e){} } });
});
const ptc = H('pthread_create');
if (ptc) Interceptor.attach(ptc, { onEnter(args){ try{ W('pthread_create fn='+args[2]+' name='+(args[3]&&!args[3].isNull()?args[3].readCString():'')); }catch(e){} } });
const mmapP = H('mmap');
if (mmapP) { let n=0; Interceptor.attach(mmapP, { onEnter(a){ if(n++<200) try{ W('mmap len='+a[1]+' prot='+a[2]+' flags='+a[3]); }catch(e){} } }); }

console.log('[hide] armed: props='+!!gsp+' fopen='+!!fopenP+' fread='+!!freadP);
