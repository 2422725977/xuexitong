'use strict';
var LOG='/data/local/tmp/plog/propfix.log';
var FP='google/coral/coral:10/QQ3A.200805.001/6578210:user/release-keys';
var FIX={
 'ro.build.fingerprint': FP,
 'ro.bootimage.build.fingerprint': FP,
 'ro.system.build.fingerprint': FP,
 'ro.vendor.build.fingerprint': FP,
 'ro.odm.build.fingerprint': FP,
 'ro.product.build.fingerprint': FP,
 'ro.build.characteristics': 'nosdcard',
 'ro.build.tags': 'release-keys',
 'ro.system.build.tags': 'release-keys',
 'ro.vendor.build.tags': 'release-keys',
 'ro.odm.build.tags': 'release-keys',
 'ro.build.type': 'user',
 'ro.build.flavor': 'coral-user',
 'ro.build.id': 'QQ3A.200805.001',
 'ro.build.display.id': 'QQ3A.200805.001',
 'ro.build.version.incremental': '6578210',
 'ro.build.description': 'coral-user 10 QQ3A.200805.001 6578210 release-keys',
 'ro.build.user': 'android-build',
 'ro.build.host': 'abfarm730',
 'ro.product.brand': 'google',
 'ro.product.manufacturer': 'Google',
 'ro.product.model': 'Pixel 4',
 'ro.product.device': 'coral',
 'ro.product.name': 'coral',
 'ro.product.board': 'coral',
 'ro.product.odm.brand': 'google',
 'ro.product.odm.device': 'coral',
 'ro.product.odm.model': 'Pixel 4',
 'ro.product.system.brand': 'google',
 'ro.product.system.device': 'coral',
 'ro.product.system.model': 'Pixel 4',
 'ro.product.vendor.brand': 'google',
 'ro.product.vendor.device': 'coral',
 'ro.product.vendor.model': 'Pixel 4',
 'ro.board.platform': 'msmnile',
 'ro.soc.manufacturer': 'Qualcomm',
 'ro.soc.model': 'SM8150',
 'ro.debuggable': '0',
 'ro.secure': '1',
 'ro.adb.secure': '1',
 'ro.kernel.qemu': '0',
 'ro.kernel.qemu.avd_name': '',
 'ro.kernel.android.qemud': '0',
 'ro.serialno': '0A1B2C3D4E5F',
 'ro.boot.serialno': '0A1B2C3D4E5F',
 'ro.boot.verifiedbootstate': 'green',
 'ro.boot.flash.locked': '1',
 'ro.boot.veritymode': 'enforcing',
 'ro.bootloader': 'coral-0.4-6791234',
 'ro.boot.bootloader': 'coral-0.4-6791234',
 'ro.boot.mode': 'normal',
 'ro.boot.baseband': 'msm',
 'ro.boot.hardware': 'coral',
 'ro.product.first_api_level': '29'
};
var libc=Process.findModuleByName('libc.so');
function sym(n){ try{ return libc.findExportByName(n); }catch(e){ return null; } }
var fd=-1, writeF=null;
try{
  var openF=new NativeFunction(sym('open'),'int',['pointer','int','int']);
  fd=openF(Memory.allocUtf8String(LOG), 1|64|512, 438);
}catch(e){}
try{ writeF=new NativeFunction(sym('write'),'long',['int','pointer','long']); }catch(e){}
function log(s){
  try{
    s=(''+s).replace(/[^\x20-\x7e]/g,'.');
    if(fd>=0 && writeF){ var p=Memory.allocUtf8String(s+'\n'); writeF(fd,p,s.length+1); } else send(s);
  }catch(e){}
}
send('PROPFIX_START pid='+Process.id);
var findP=sym('__system_property_find');
var updP=sym('__system_property_update');
var getP=sym('__system_property_get');
var addP=sym('__system_property_add');
var readP=sym('__system_property_read');
log('sym find='+findP+' update='+updP+' get='+getP+' add='+addP+' read='+readP);
var findF=findP? new NativeFunction(findP,'pointer',['pointer']) : null;
var updF=updP? new NativeFunction(updP,'int',['pointer','pointer','uint']) : null;
var addF=addP? new NativeFunction(addP,'int',['pointer','uint','pointer','uint']) : null;
var getF=getP? new NativeFunction(getP,'int',['pointer','pointer']) : null;
var okCount=0, missCount=0, failCount=0;
function patchAll(){
  for(var k in FIX){
    var v=FIX[k];
    var kb=Memory.allocUtf8String(k), vb=Memory.allocUtf8String(v);
    var pi=findF(kb);
    if(pi.isNull()){
      if(addF){ var ra=addF(kb,k.length,vb,v.length); log('ADD '+k+'='+v+' rc='+ra); if(ra===0) okCount++; else failCount++; }
      else { log('MISS '+k); missCount++; }
      continue;
    }
    var rc=updF(pi, vb, v.length);
    if(rc===0) okCount++; else { failCount++; log('UPD-FAIL '+k+'='+v+' rc='+rc); }
  }
  log('patch done ok='+okCount+' fail='+failCount+' miss='+missCount);
}
try{ patchAll(); }catch(e){ log('patchAll err '+e); }
try{
  var buf=Memory.alloc(256);
  getF(Memory.allocUtf8String('ro.build.characteristics'), buf);
  log('READBACK characteristics='+buf.readUtf8String());
  getF(Memory.allocUtf8String('ro.build.fingerprint'), buf);
  log('READBACK fingerprint='+buf.readUtf8String());
  getF(Memory.allocUtf8String('ro.product.model'), buf);
  log('READBACK model='+buf.readUtf8String());
  getF(Memory.allocUtf8String('ro.debuggable'), buf);
  log('READBACK debuggable='+buf.readUtf8String());
}catch(e){ log('readback err '+e); }
try{
  Interceptor.attach(findP,{ onEnter:function(a){ try{ log('FIND '+a[0].readUtf8String()); }catch(e){} } });
  log('hook find ok');
}catch(e){ log('hook find err '+e); }
try{
  Interceptor.attach(getP,{
    onEnter:function(a){ try{ this.n=a[0].readUtf8String(); }catch(e){ this.n='?'; } this.b=a[1]; },
    onLeave:function(r){ var v=''; try{ v=this.b.readUtf8String(); }catch(e){}
      log('GET '+this.n+' = '+v);
      if(FIX[this.n]!==undefined && v!==FIX[this.n]){ try{ this.b.writeUtf8String(FIX[this.n]); r.replace(FIX[this.n].length); log('GET-FIXED '+this.n); }catch(e){} } } });
  log('hook get ok');
}catch(e){ log('hook get err '+e); }
try{
  if(readP){ var readFn=new NativeFunction(readP,'int',['pointer','pointer','pointer']);
    Interceptor.attach(readP,{ onEnter:function(a){ this.nb=a[1]; this.vb=a[2]; },
      onLeave:function(r){ try{ var n=this.nb.isNull()?'':this.nb.readUtf8String(); var v=this.vb.isNull()?'':this.vb.readUtf8String();
        log('READ '+n+' = '+v);
        if(FIX[n]!==undefined && v!==FIX[n]){ this.vb.writeUtf8String(FIX[n]); r.replace(FIX[n].length); log('READ-FIXED '+n); } }catch(e){} } });
    log('hook read ok'); }
}catch(e){ log('hook read err '+e); }
setInterval(function(){ log('HB'); }, 3000);
