// frida_app_probe.js —— root/frida 模拟客户端：抓上传/签到请求 + 注入学生会话
// 占位符 __COOKIE__ 由 Python 驱动替换为真实 cookie 串（不打印）
var CK = __COOKIE__;
function log() { var a = []; for (var i = 0; i < arguments.length; i++) a.push(arguments[i]); console.log(a.join(' ')); }
var WANT = /(upload|sign|photo|pan-yz|clouddisk|newTaskSign|stuSignajax|jsprotocal)/i;

Java.perform(function () {
  // 1) okhttp：注入 Cookie + 记录 URL
  try {
    var B = Java.use('okhttp3.Request$Builder');
    B.build.overload().implementation = function () {
      try {
        var u = this.url().toString();
        if (/chaoxing\.com|cldisk\.com/.test(u)) {
          try { this.header('Cookie', CK); } catch (e) {}
          if (WANT.test(u)) log('[REQ]', u.substring(0, 220));
        }
      } catch (e) {}
      return this.build();
    };
  } catch (e) { log('[!] okhttp3.Request$Builder hook 失败', e); }

  // 2) 记录表单/多部分字段（上传参数就在这里）
  try {
    var FB = Java.use('okhttp3.FormBody$Builder');
    FB.add.overload('java.lang.String', 'java.lang.String').implementation = function (k, v) {
      log('[FORM]', k, '=', String(v).substring(0, 120));
      return this.add(k, v);
    };
  } catch (e) {}
  try {
    var MB = Java.use('okhttp3.MultipartBody$Builder');
    MB.addFormDataPart.overload('java.lang.String', 'java.lang.String').implementation = function (k, v) {
      log('[MP]', k, '=', String(v).substring(0, 120));
      return this.addFormDataPart(k, v);
    };
    MB.addFormDataPart.overload('java.lang.String', 'java.lang.String', 'okhttp3.RequestBody').implementation = function (k, f, b) {
      log('[MP-FILE]', k, 'file=', String(f));
      return this.addFormDataPart(k, f, b);
    };
  } catch (e) {}

  // 3) WebView cookie 读写
  try {
    var CM = Java.use('android.webkit.CookieManager');
    CM.setCookie.overload('java.lang.String', 'java.lang.String').implementation = function (u, c) {
      log('[CM.set]', u, '->', String(c).substring(0, 80));
      return this.setCookie(u, c);
    };
  } catch (e) {}

  // 4) 账密/上传相关 native 入口
  try {
    var b = Java.use('com.chaoxing.mobile.clouddisk.upload.b');
    b.B.overloads.forEach(function (o) {
      o.implementation = function () {
        log('[CLOUD_UPLOAD] 调用参数数=' + o.argumentTypes.length);
        return o.apply(this, arguments);
      };
    });
  } catch (e) { log('[!] clouddisk.upload.b 未就绪（可能未加载）'); }

  log('[*] hooks installed');
});