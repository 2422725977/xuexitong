'use strict';
var LOG='/data/local/tmp/plog/probe.log';
function libcSym(n){ try{ var m=Process.findModuleByName('libc.so'); return m? m.findExportByName(n): null; }catch(e){ return null; } }
var fd=-1, writeF=null, sent=0;
try{
  var openF=new NativeFunction(libcSym('open'),'int',['pointer','int','int']);
  fd=openF(Memory.allocUtf8String(LOG), 1|64|1024, 438);
}catch(e){}
try{ writeF=new NativeFunction(libcSym('write'),'long',['int','pointer','long']); }catch(e){}
function log(s){
  try{
    s=(''+s).replace(/[^\x20-\x7e]/g,'.');
    if(fd>=0 && writeF){ var p=Memory.allocUtf8String(s+'\n'); writeF(fd,p,s.length+1); }
    else if(sent<400){ sent++; send(s); }
  }catch(e){}
}
send('PROBE_START pid='+Process.id);
log('== probe start pid='+Process.id+' frida='+Frida.version+' fd='+fd);
log('== modules: '+Process.enumerateModules().filter(function(m){return /DexHelper|dexjni|encrypt|RiskStub|secneo|art|libc\.so|libnative/.test(m.name);}).map(function(m){return m.name+'@'+m.base;}).join(' '));
function hookProp(){
  var g=libcSym('__system_property_get');
  if(!g){ log('!! no __system_property_get'); return; }
  Interceptor.attach(g,{
    onEnter: function(a){ try{ this.n=a[0].readUtf8String()||'?'; }catch(e){ this.n='?'; } this.b=a[1]; },
    onLeave: function(r){ var v=''; try{ v=this.b.readUtf8String()||''; }catch(e){ v='<err>'; } log('PROP '+this.n+' = '+v); }
  });
  log('hook get ok');
}
function hookReadCallback(){
  var rc=libcSym('__system_property_read_callback');
  var rd=libcSym('__system_property_read');
  if(!rc){ log('!! no read_callback'); return; }
  var readF=rd? new NativeFunction(rd,'void',['pointer','pointer','pointer']) : null;
  Interceptor.attach(rc,{
    onEnter: function(a){
      try{
        if(readF){ var nb=Memory.alloc(128), vb=Memory.alloc(128); readF(a[0],nb,vb); log('PROPCB '+nb.readUtf8String()+' = '+vb.readUtf8String()); }
      }catch(e){ log('PROPCB err '+e); }
    }
  });
  log('hook read_callback ok');
}
var KEY=['qemu','goldfish','ranchu','genymotion','vbox','bluestacks','magisk','frida','xposed','tracerpid','emulator','substrate','qemud','/dev/socket/','/sys/qemu','cpuinfo','/proc/version','sdk_gphone','aosp','ro.debuggable','/proc/self/maps','maps'];
function interesting(p){
  if(!p) return false; var l=(''+p).toLowerCase();
  for(var i=0;i<KEY.length;i++){ if(l.indexOf(KEY[i])>=0) return true; }
  return false;
}
function hookPath(fname, pathIdx, tag){
  var f=libcSym(fname); if(!f) return;
  try{ Interceptor.attach(f,{ onEnter: function(a){ var p=null; try{ p=a[pathIdx].readUtf8String(); }catch(e){ return; } if(interesting(p)) log(tag+' '+p); } }); log('hook '+tag+' ok'); }
  catch(e){ log('hook '+fname+' fail '+e); }
}
function hookDlopen(){
  try{ var d=libcSym('android_dlopen_ext'); if(d){ Interceptor.attach(d,{ onEnter:function(a){ try{ log('DLOPEN '+a[0].readUtf8String()); }catch(e){} } }); log('hook dlopen_ext ok'); } }catch(e){}
  try{ var d2=libcSym('dlopen'); if(d2){ Interceptor.attach(d2,{ onEnter:function(a){ try{ log('dlopen '+a[0].readUtf8String()); }catch(e){} } }); } }catch(e){}
}
hookProp(); hookReadCallback();
hookPath('open',0,'OPEN'); hookPath('openat',1,'OPENAT'); hookPath('access',0,'ACCESS'); hookPath('faccessat',1,'FACCESSAT');
hookDlopen();
log('== hooks installed tid='+Process.getCurrentThreadId());
setInterval(function(){ log('HB'); }, 2000);
