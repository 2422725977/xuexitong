/*
 * frida_sign_hook.js - 学习通 (com.chaoxing.mobile 6.7.8) 签到向 hook / RPC 注入
 *
 * 干什么：
 *   1. 打印扫码签到的全部关键量：二维码内容、enc 拼接原文、enc、phoneId、最终 URL
 *   2. RPC 直接调 SignInfoActivity.m5(二维码JSON, puid) —— 不用相机、不用到场
 *   3. 自动抓 App 的 Cookie（省掉 mitmproxy）
 *   4. 人脸回传 JSON 模板（H5 签到人脸跳过用，配合 frida_face_puppet.js）
 *
 * 用法：
 *   frida -U -f com.chaoxing.mobile -l frida_sign_hook.js --no-pause
 *   # 已启动的进程：
 *   frida -U -n 学习通 -l frida_sign_hook.js
 *
 *   # CLI 里直接注入二维码（等于"远程扫到了这张码"）：
 *   rpc.exports.signQR('{"time":"1712000000","signId":"1234567890"}', '你的puid')
 *   # 抓 cookie：
 *   rpc.exports.dumpCookie()
 *
 * 适配：学习通 6.7.8（versionCode 10946），梆梆 SecNeo 壳
 *   SignInfoActivity.m5(String qrJson, String puid)
 *     -> enc = com.fanzhou.util.j.d(signId + "-" + uid + "-" + time + "-" + phoneId)
 *     -> GET fanyappfy.chaoxing.com/usersign/addsign?...&ctype=stusign
 */
var CONFIG = {
  dumpCookie: true,      // 自动导出 Cookie
  logVolley: true,       // 打印所有 volley 请求 URL（过滤签到相关）
  logFace: true,         // 打印 H5 人脸桥调用
  autoInject: null,      // 形如 {qr:'{"time":..,"signId":".."}', uid:'123'} 启动后自动签
};

var T = "sign-hook";
function log() {
  var a = [];
  for (var i = 0; i < arguments.length; i++) a.push(arguments[i]);
  console.log("[" + T + "] " + a.join(" "));
}

var COOKIES = {};

function cookieOf(url) {
  try {
    var CM = Java.use("android.webkit.CookieManager");
    var c = CM.getInstance().getCookie(url);
    if (c) { COOKIES[url] = c; log("cookie(" + url + ") = " + c.slice(0, 400)); }
    return c;
  } catch (e) { log("cookieOf failed " + e); return null; }
}

function tryHook(desc, fn) {
  try { fn(); log("hook OK  : " + desc); }
  catch (e) { log("hook SKIP: " + desc + " -> " + e); }
}

Java.perform(function () {
  log("loaded");

  /* ---------- 1. 二维码 -> enc -> URL 全链路 ---------- */
  tryHook("SignInfoActivity.m5(String,String)", function () {
    var A = Java.use("com.chaoxing.mobile.sign.ui.SignInfoActivity");
    A.m5.overload("java.lang.String", "java.lang.String").implementation = function (qr, uid) {
      log("QR 内容 = " + qr);
      log("uid     = " + uid);
      return this.m5(qr, uid);
    };
  });

  tryHook("SignInfoActivity.j5(String)", function () {
    var A = Java.use("com.chaoxing.mobile.sign.ui.SignInfoActivity");
    A.j5.overload("java.lang.String").implementation = function (s) {
      log("j5(扫码回调) = " + s);
      return this.j5(s);
    };
  });

  tryHook("SignInfoActivity.r5(String)", function () {
    var A = Java.use("com.chaoxing.mobile.sign.ui.SignInfoActivity");
    A.r5.overload("java.lang.String").implementation = function (u) {
      log("提交 URL = " + u);
      return this.r5(u);
    };
  });

  /* ---------- 2. enc / phoneId / 基址 ---------- */
  tryHook("com.fanzhou.util.j.d", function () {
    var J = Java.use("com.fanzhou.util.j");
    J.d.overload("java.lang.String").implementation = function (s) {
      var r = this.d(s);
      log("MD5 原文 = " + s + "  ->  enc = " + r);
      return r;
    };
  });

  tryHook("an.b.d() / uniqueId", function () {
    var B = Java.use("an.b");
    if (B.d) {
      try {
        B.d.overload().implementation = function () {
          var v = this.d();
          log("phoneId(an.b.d) = " + v);
          return v;
        };
      } catch (e) { log("an.b.d() hook 跳过: " + e); }
    }
  });

  tryHook("wm.a.a (addsign 基址)", function () {
    var W = Java.use("wm.a");
    log("wm.a.a = " + W.a.value);
  });

  tryHook("gc.b 基址常量", function () {
    var G = Java.use("gc.b");
    log("gc.b.j(fanyappfy) = " + G.j.value + " | gc.b.k(mobilelearn) = " + G.k.value);
  });

  /* ---------- 3. 扫码分发（SIGNIN: / GROUP: / ...） ---------- */
  tryHook("com.chaoxing.mobile.main.f.s(String)", function () {
    var F = Java.use("com.chaoxing.mobile.main.f");
    F.s.overload("java.lang.String").implementation = function (s) {
      log("扫码分发 s(" + s + ")");
      return this.s(s);
    };
  });

  /* ---------- 4. 所有 volley 请求（拿最终 URL + 响应码） ---------- */
  if (CONFIG.logVolley) {
    tryHook("volley.toolbox.StringRequest ctor", function () {
      var SR = Java.use("com.android.volley.toolbox.StringRequest");
      SR.$init.overloads.forEach(function (ov) {
        ov.implementation = function () {
          for (var i = 0; i < arguments.length; i++) {
            var a = arguments[i];
            if (typeof a === "string" && (a.indexOf("addsign") >= 0 || a.indexOf("sign") >= 0
                || a.indexOf("chaoxing.com") >= 0)) {
              log("volley URL = " + a);
            }
          }
          return ov.apply(this, arguments);
        };
      });
    });
  }

  /* ---------- 5. Cookie 自动导出 ---------- */
  if (CONFIG.dumpCookie) {
    tryHook("CookieManager.getCookie", function () {
      var CM = Java.use("android.webkit.CookieManager");
      CM.getCookie.overload("java.lang.String").implementation = function (u) {
        var c = this.getCookie(u);
        if (c) COOKIES[u] = c;
        return c;
      };
    });
    tryHook("okhttp3.Headers$Builder.add", function () {
      var HB = Java.use("okhttp3.Headers$Builder");
      HB.add.overload("java.lang.String", "java.lang.String").implementation = function (k, v) {
        if (k && k.toLowerCase() === "cookie") { COOKIES["okhttp"] = v; log("okhttp Cookie = " + v.slice(0, 300)); }
        return this.add(k, v);
      };
    });
  }

  /* ---------- 6. H5 人脸桥（跳过人脸用） ---------- */
  if (CONFIG.logFace) {
    tryHook("FaceRecognitionExecutor.execute", function () {
      var FE = Java.use("com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor");
      FE.execute.overload("java.lang.String").implementation = function (j) {
        log("人脸桥 execute(" + j + ")");
        return this.execute(j);
      };
    });
    tryHook("FaceRecognitionExecutor 回调", function () {
      var FE = Java.use("com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor");
      FE.Y.overload("com.chaoxing.facedetection.CollectResult", "int", "int").implementation = function (r, a, b) {
        log("人脸桥回调 Y: liveStatus=" + r.getLiveDetectionStatus() + " a=" + a + " b=" + b);
        return this.Y(r, a, b);
      };
    });
  }

  /* ---------- 7. 启动后自动注入 ---------- */
  if (CONFIG.autoInject) {
    setTimeout(function () { signQR(CONFIG.autoInject.qr, CONFIG.autoInject.uid); }, 6000);
  }

  log("ready. RPC: signQR(qrJson, uid) / listInstances() / dumpCookie() / faceReplyTemplate()");
});

/* ================= RPC ================= */

function withInstance(cb) {
  var A = Java.use("com.chaoxing.mobile.sign.ui.SignInfoActivity");
  var hit = 0;
  Java.choose("com.chaoxing.mobile.sign.ui.SignInfoActivity", {
    onMatch: function (inst) { hit++; try { cb(inst); } catch (e) { log("cb err " + e); } },
    onComplete: function () { if (!hit) log("当前没有 SignInfoActivity 实例（先让签到页面/扫码页起来）"); }
  });
  return hit;
}

function signQR(qr, uid) {
  if (!qr || !uid) { log("signQR 需要 (qrJson, uid)"); return "bad args"; }
  var n = withInstance(function (inst) {
    log("调用实例 m5 注入二维码: " + qr);
    inst.m5(qr, uid);
  });
  return "instances=" + n;
}

rpc.exports = {
  signqr: signQR,
  signQR: signQR,
  listinstances: function () {
    var out = [];
    withInstance(function (inst) { out.push(String(inst)); });
    return out;
  },
  dumpcookie: function (url) {
    url = url || "https://mobilelearn.chaoxing.com/";
    cookieOf(url);
    cookieOf("https://fanyappfy.chaoxing.com/");
    cookieOf("https://passport2-api.chaoxing.com/");
    return COOKIES;
  },
  faceReplyTemplate: function () {
    // FaceRecognitionExecutor.Y() 回传 JS 的 JSON 形状（人脸跳过演示：活体=1、采集=成功）
    return {
      currentFaceId: 0,
      collectStatus: 1,
      liveDetectionStatus: 1,
      recogType: 1,
      sessionId: "",
      senseDetectionStatus: 1,
      extraData: "",
      signToken: "",
      cxcid: 0,
      cxtime: Date.now()
    };
  }
};
