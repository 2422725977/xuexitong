// 学习通 真机 capture 脚本（Frida 17 / Android）
// 用法: frida -U -f com.chaoxing.mobile -l scripts/hide_env.js -l scripts/device/frida_android_capture.js
// 作用: okhttp 请求(URL+头) / multipart 字段 / 响应体 / WebView 加载 / 云盘上传配置 / 人脸桥 / Cookie 写入
'use strict';
var TAG = '[cxcap]';
function ts() { return new Date().toISOString().substr(11, 12); }
function log() {
  var a = [TAG, ts()];
  for (var i = 0; i < arguments.length; i++) a.push(String(arguments[i]));
  console.log(a.join(' '));
}
function trunc(s, n) { s = String(s === undefined || s === null ? '' : s); return s.length <= n ? s : (s.substr(0, n) + '...<' + s.length + 'B>'); }
var INTEREST = /chaoxing|cldisk/;

Java.perform(function () {
  // 1) okhttp 请求 URL + 请求头
  try {
    var RB = Java.use('okhttp3.Request$Builder');
    RB.build.implementation = function () {
      var req = this.build();
      try {
        var u = req.url().toString();
        if (INTEREST.test(u)) {
          log('REQ', req.method(), u);
          var h = req.headers();
          if (h) log('  headers:', trunc(h.toString().replace(/\n/g, ' | '), 900));
        }
      } catch (e) { log('req parse err', e); }
      return req;
    };
    log('hook okhttp3.Request$Builder OK');
  } catch (e) { log('okhttp3.Request$Builder 未命中:', e); }

  // 2) multipart 表单字段（上传的 puid / _token / 文件名）
  try {
    var Part = Java.use('okhttp3.MultipartBody$Part');
    Part.createFormData.overload('java.lang.String', 'java.lang.String', 'okhttp3.RequestBody').implementation = function (n, fn, body) {
      log('MULTIPART field=', n, 'filename=', fn, 'type=', trunc(body && body.contentType && body.contentType(), 60));
      return this.createFormData(n, fn, body);
    };
    log('hook MultipartBody$Part OK');
  } catch (e) { log('MultipartBody$Part 未命中:', e); }

  // 3) 响应体（objectId / photoAuthError / success）
  try {
    var RBody = Java.use('okhttp3.ResponseBody');
    RBody.string.implementation = function () {
      var s = this.string();
      try { if (s && s.length < 20000) log('RESP', trunc(s, 1500)); } catch (e) {}
      return s;
    };
    log('hook ResponseBody.string OK');
  } catch (e) { log('ResponseBody 未命中:', e); }

  // 4) WebView 加载 + 强制打开远程调试
  try {
    var WV = Java.use('android.webkit.WebView');
    WV.loadUrl.overload('java.lang.String').implementation = function (u) {
      log('WEBVIEW loadUrl', u);
      return this.loadUrl(u);
    };
    try {
      WV.setWebContentsDebuggingEnabled.overload('boolean').implementation = function (b) {
        log('WebView.setWebContentsDebuggingEnabled(', b, ') -> 强制 true');
        return this.setWebContentsDebuggingEnabled(true);
      };
    } catch (e2) { log('setWebContentsDebuggingEnabled hook 失败:', e2); }
    log('hook WebView OK');
  } catch (e) { log('WebView 未命中:', e); }

  // 5) 云盘上传：配置(URL/业务参数) 与 结果(objectId)
  try {
    var Ub = Java.use('com.chaoxing.mobile.clouddisk.upload.b');
    Ub.B.overload('android.net.Uri', 'com.chaoxing.mobile.clouddisk.upload.CloudUploadConfig', 'okhttp3.Callback').implementation = function (uri, cfg, cb) {
      try {
        log('UPLOAD uri=', uri);
        log('  requestParams=', trunc(cfg.getRequestParams && cfg.getRequestParams(), 800));
        log('  uploadConfigs=', trunc(cfg.getUploadConfigs && cfg.getUploadConfigs(), 800));
      } catch (e2) { log('cfg dump err', e2); }
      return this.B(uri, cfg, cb);
    };
    log('hook clouddisk upload.b.B OK');
  } catch (e) { log('clouddisk upload.b 未命中（类名/重载可能不同）:', e); }

  // 6) 人脸桥：拿 signToken / faceEnc / clientId
  try {
    var FR = Java.use('com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor');
    FR.execute.overload('java.lang.String', 'java.lang.String').implementation = function (tag, params) {
      log('FACE execute', tag, trunc(params, 800));
      var r = this.execute(tag, params);
      log('FACE return', trunc(r, 800));
      return r;
    };
    log('hook FaceRecognitionExecutor.execute OK');
  } catch (e) { log('FaceRecognitionExecutor 未命中:', e); }

  // 7) Cookie 写入（App 登录后可能种设备 cookie）
  try {
    var CM = Java.use('android.webkit.CookieManager');
    CM.setCookie.overload('java.lang.String', 'java.lang.String').implementation = function (u, c) {
      log('COOKIE SET', u, trunc(c, 300));
      return this.setCookie(u, c);
    };
    log('hook CookieManager.setCookie OK');
  } catch (e) { log('CookieManager 未命中:', e); }

  log('全部 hook 装载完成');
});