// frida_app_scan_sim.js —— 在真机/模拟器里用 App 自己的 WebView 走签到 H5，并"模拟扫码"注入二维码内容
// 逆向依据：WebAppWebViewer$2.onActivityResult(ScanResult) 收扫码结果；WebAppWebViewer.m5(String,String) 派发给 JS；
// 页面 preSign 的 JS：jsBridge.bind('CLIENT_BARCODE_SCANNER', sacn_callback) → signDetail(msg) → msg==res.signCode → navOpen()
var TAG = '[scan-sim]';
function log(o){ send(Object.assign({tag:TAG}, o)); }

Java.perform(function () {
  log({ev:'loaded'});

  // 1) 把浏览器会话 cookie 灌进 App 的 WebView cookie 仓（H5 侧认证走 cookie）
  rpc.exports.setck = function (cookie) {
    Java.perform(function () {
      try {
        var CM = Java.use('android.webkit.CookieManager');
        var cm = CM.getInstance();
        ['mobilelearn.chaoxing.com','mooc1.chaoxing.com','mooc1-api.chaoxing.com','i.chaoxing.com',
         'passport2.chaoxing.com','chaoxing.com','fanyappfy.chaoxing.com','x.chaoxing.com'].forEach(function (h) {
          try { cm.setCookie('https://' + h, cookie); } catch (e) {}
        });
        cm.flush();
        log({ev:'cookie-injected'});
      } catch (e) { log({ev:'cookie-err', m:'' + e}); }
    });
    return 'ok';
  };

  // 2) 绕过 App 原生登录态闸门 AccountManager.Z()（页面本身只需要 cookie）
  try {
    var AM = Java.use('com.chaoxing.study.account.AccountManager');
    AM.Z.implementation = function () { return true; };
    log({ev:'gate-bypass'});
  } catch (e) { log({ev:'gate-err', m:'' + e}); }

  // 3) 观察扫码派发点
  try {
    var W = Java.use('com.chaoxing.mobile.webapp.ui.WebAppWebViewer');
    W.m5.overload('java.lang.String', 'java.lang.String').implementation = function (a, b) {
      log({ev:'m5-dispatch', a:a, b:b});
      return this.m5(a, b);
    };
  } catch (e) { log({ev:'m5-err', m:'' + e}); }

  // 4) 打开签到 H5
  rpc.exports.opencal = function (url) {
    Java.scheduleOnMainThread(function () {
      try {
        var AT = Java.use('android.app.ActivityThread');
        var app = AT.currentApplication();
        var ctx = app.getApplicationContext();
        var Intent = Java.use('android.content.Intent');
        var Comp = Java.use('android.content.ComponentName');
        var i = Intent.$new();
        i.setComponent(Comp.$new('com.chaoxing.mobile', 'com.chaoxing.mobile.webapp.ui.WebAppViewerActivity'));
        i.putExtra('url', Java.use('java.lang.String').$new(url));
        i.putExtra('title', Java.use('java.lang.String').$new('签到'));
        i.addFlags(268435456);
        ctx.startActivity(i);
        log({ev:'activity-started', url:url});
      } catch (e) { log({ev:'activity-err', m:'' + e}); }
    });
    return 'ok';
  };

  var cbN = 0;
  function evalJs(wv, code, tag) {
    var VC = Java.use('android.webkit.ValueCallback');
    var CB = Java.registerClass({
      name: 'cxsim.Cb' + (++cbN),
      implements: [VC],
      methods: { onReceiveValue: function (v) { log({ev:'js', tag:tag, v: v ? v.toString() : null}); } }
    });
    Java.scheduleOnMainThread(function () {
      try {
        var S = Java.use('java.lang.String');
        wv.evaluateJavascript(S.$new(code), CB.$new());
      } catch (e) { log({ev:'eval-err', tag:tag, m:'' + e}); }
    });
  }

  function eachWebView(code, tag) {
    Java.perform(function () {
      var n = 0;
      Java.choose('android.webkit.WebView', {
        onMatch: function (w) {
          n++;
          try { log({ev:'wv-found', url:'' + w.getUrl()}); } catch (e) {}
          evalJs(w, code, tag + '#' + n);
        },
        onComplete: function () { log({ev:'wv-scan-done', n:n, tag:tag}); }
      });
    });
  }

  var PATCH = "(function(){ if(window.__patched) return 'already'; window.__patched=1; window.__req=[]; window.__tips=[];" +
    "var o=XMLHttpRequest.prototype.open,s=XMLHttpRequest.prototype.send;" +
    "XMLHttpRequest.prototype.open=function(m,u){this.__u=u;window.__req.push(m+' '+u);return o.apply(this,arguments)};" +
    "XMLHttpRequest.prototype.send=function(d){var x=this;x.addEventListener('load',function(){window.__req.push('RESP '+(x.__u||'')+' => '+String(x.responseText).slice(0,200))});return s.apply(this,arguments)};" +
    "var t=window.showTip; window.showTip=function(m){window.__tips.push(String(m)); try{return t.apply(this,arguments)}catch(e){return 0}};" +
    "if(typeof jQuery!=='undefined'&&jQuery.ajax){var a=jQuery.ajax;jQuery.ajax=function(opt){try{window.__req.push('AJAX '+((opt&&opt.url)||''))}catch(e){} return a.apply(this,arguments)};}" +
    "return 'patched'; })()";

  rpc.exports.patch = function () { eachWebView(PATCH, 'patch'); return 'ok'; };
  rpc.exports.feed = function (qr) {
    var code = "(function(){ var r=[]; try{ window.__tips && window.__tips.push('[feed]"+0+"'); sacn_callback({message:" + JSON.stringify(qr) + ",cancelFlag:0}); r.push('sacn_callback-called'); }catch(e){ r.push('ERR '+e); } return r.join('|'); })()";
    eachWebView(code, 'feed');
    return 'ok';
  };
  rpc.exports.readback = function () {
    eachWebView("JSON.stringify({tips:window.__tips||null,req:window.__req||null,enc:(typeof enc!=='undefined'?enc:null),sc:(typeof res!=='undefined'&&res?res.signCode:null),over:(typeof res!=='undefined'&&res?res.isOver:null)})", 'readback');
    return 'ok';
  };
});
