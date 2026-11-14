/*
 * frida_face_puppet.js — 学习通 (com.chaoxing.mobile) 人脸链路注入工具包
 * 用途：在无摄像头 / 远程环境下完成人脸采集类流程（打卡人脸、考试人脸抓拍），
 *       或把提交请求里的人脸图替换为预置素材。
 *
 * 用法：
 *   frida -U -f com.chaoxing.mobile -l frida_face_puppet.js --no-pause
 *   参数（frida CLI 里改 CONFIG，或用 -e 注入）：
 *     CONFIG.mode    = "log" | "inject"     // log: 只记录; inject: 真的替换素材
 *     CONFIG.face    = "/data/local/tmp/face.jpg"   // 预置人脸图（提前用本人真脸采集一次）
 *     CONFIG.liveness= true                 // 强制活体状态为成功
 *     CONFIG.webcam  = true                 // 授予 H5 getUserMedia，允许网页开摄像头
 *     CONFIG.hookEnc = true                 // 记录 enc/sign 的原文（协议重放用）
 *   adb push face.jpg /data/local/tmp/face.jpg
 *
 * 适配版本：学习通 6.7.8（versionCode 10946），梆梆 SecNeo 壳，RF/商汤双人脸引擎
 */

var CONFIG = {
  mode: "log",
  face: "/data/local/tmp/face.jpg",
  liveness: true,
  webcam: true,
  hookEnc: true,
};

var T = "face-puppet";
function log() { var a = []; for (var i = 0; i < arguments.length; i++) a.push(arguments[i]);
  console.log("[" + T + "] " + a.join(" ")); }
function javaFileOk(p) {
  try { var F = Java.use("java.io.File"); var f = F.$new(p); return f.exists() && f.isFile(); }
  catch (e) { log("file check failed", e); return false; }
}
function readBase64(p) {
  try {
    var FileInputStream = Java.use("java.io.FileInputStream");
    var Base64 = Java.use("android.util.Base64");
    var fis = FileInputStream.$new(p);
    var buf = Java.array("byte", new Array(8192).fill(0));
    var out = Java.array("byte", []);
    // 简化：一次性读（图片 < 8MB 够用）
    var F = Java.use("java.io.File"); var len = F.$new(p).length();
    var all = Java.array("byte", new Array(len).fill(0));
    fis.read(all); fis.close();
    return Base64.encodeToString(all, 2); // NO_WRAP
  } catch (e) { log("readBase64 failed", e); return null; }
}

Java.perform(function () {
  log("loaded, mode=" + CONFIG.mode + " face=" + CONFIG.face + " exists=" + javaFileOk(CONFIG.face));

  /* ---------- L2 采集结果层：活体状态 / 采集结果 ---------- */
  try {
    var CR = Java.use("com.chaoxing.facedetection.CollectResult");
    if (CONFIG.liveness) {
      CR.setLiveDetectionStatus.implementation = function (v) {
        log("CollectResult.setLiveDetectionStatus " + v + " -> 1(LIVE_STATUS_SUCCESS)");
        return this.setLiveDetectionStatus(1);
      };
    }
    CR.setImagePath.implementation = function (p) {
      log("CollectResult.setImagePath " + p + (CONFIG.mode === "inject" ? " -> " + CONFIG.face : ""));
      return this.setImagePath(CONFIG.mode === "inject" ? CONFIG.face : p);
    };
    CR.getLiveDetectionStatus.implementation = function () {
      var v = this.getLiveDetectionStatus();
      return CONFIG.liveness ? 1 : v;
    };
  } catch (e) { log("CollectResult hook skip: " + e); }

  try {
    var CF = Java.use("com.chaoxing.facedetection.bean.CollectFile");
    CF.getPath.implementation = function () {
      var p = this.getPath();
      if (CONFIG.mode === "inject" && javaFileOk(CONFIG.face)) { log("CollectFile.getPath " + p + " -> " + CONFIG.face); return CONFIG.face; }
      log("CollectFile.getPath " + p);
      return p;
    };
  } catch (e) { log("CollectFile hook skip: " + e); }

  // 采集结束统一回调：拿到最终结果（含 objectId / 活体状态 / 结果图片路径）
  try {
    var FC = Java.use("com.chaoxing.facedetection.FaceCollector");
    FC.i.overload("com.chaoxing.facedetection.CollectResult").implementation = function (r) {
      try {
        log("FaceCollector.i live=" + r.getLiveDetectionStatus() + " img=" + r.getImagePath() +
            " upload=" + (r.getUploadResult() ? (r.getUploadResult().getStatus() + "/" + r.getUploadResult().getObjectIdStr()) : "null"));
      } catch (e) {}
      return this.i(r);
    };
  } catch (e) { log("FaceCollector hook skip: " + e); }

  /* ---------- L3 上传层：云盘/OSS 上传 ---------- */
  try {
    var UP = Java.use("com.chaoxing.mobile.clouddisk.upload.c");
    UP.C.overload("androidx.lifecycle.LifecycleOwner", "android.net.Uri", "com.chaoxing.mobile.clouddisk.upload.a").implementation = function (o, u, cb) {
      log("clouddisk upload " + u);
      if (CONFIG.mode === "inject" && javaFileOk(CONFIG.face)) {
        var Uri = Java.use("android.net.Uri"); var F = Java.use("java.io.File");
        u = Uri.fromFile(F.$new(CONFIG.face));
        log("  -> swapped to " + u);
      }
      return this.C(o, u, cb);
    };
  } catch (e) { log("clouddisk hook skip (overload not found): " + e); }

  /* ---------- L4 协议层：打卡/人脸比对参数 ---------- */
  try {
    var PR = Java.use("com.chaoxing.mobile.office.bean.PunchRecord");
    PR.setFacePicture.implementation = function (s) {
      log("PunchRecord.setFacePicture(" + (s ? s.length + "B" : "null") + ")");
      if (CONFIG.mode === "inject") { var b = readBase64(CONFIG.face); if (b) { log("  -> replaced"); return this.setFacePicture(b); } }
      return this.setFacePicture(s);
    };
    PR.setClockinLngLat.implementation = function (s) { log("PunchRecord.setClockinLngLat " + s); return this.setClockinLngLat(s); };
    PR.getSign.implementation = function () { var s = this.getSign(); log("PunchRecord.getSign = " + s); return s; };
    PR.getEnc.implementation = function () { var s = this.getEnc(); log("PunchRecord.getEnc = " + s); return s; };
  } catch (e) { log("PunchRecord hook skip: " + e); }

  try {
    var PP = Java.use("com.chaoxing.mobile.office.bean.PunchParams");
    PP.setFacePictureBase64.implementation = function (s) {
      log("PunchParams.setFacePictureBase64(" + (s ? s.length + "B" : "null") + ")");
      if (CONFIG.mode === "inject") { var b = readBase64(CONFIG.face); if (b) return this.setFacePictureBase64(b); }
      return this.setFacePictureBase64(s);
    };
  } catch (e) { log("PunchParams hook skip: " + e); }

  // 人脸比对请求体：[datetime=][deptId=][image=][remoteImage=][sign=officeApp][uid=] -> enc
  if (CONFIG.hookEnc) {
    try {
      var N = Java.use("vt.n");
      N.f.overload("java.lang.String").implementation = function (s) {
        log("ENC input: " + String(s).substring(0, 400));
        var r = this.f(s);
        log("ENC output: " + r);
        return r;
      };
    } catch (e) { log("vt.n.f hook skip: " + e); }
  }
  // 打卡提交（gl.i.h / gl.i.i，base https://supportoffice.chaoxing.com）
  try {
    var GI = Java.use("gl.i");
    ["h", "i", "c", "g"].forEach(function (m) {
      try {
        var ov = GI[m].overloads;
        for (var i = 0; i < ov.length; i++) {
          ov[i].implementation = (function (orig) {
            return function () {
              try { log("gl.i." + m + " args=" + JSON.stringify(Array.prototype.slice.call(arguments).map(String).slice(0, 3))); } catch (e) {}
              return orig.apply(this, arguments);
            };
          })(ov[i]);
        }
      } catch (e) {}
    });
  } catch (e) { log("gl.i hook skip: " + e); }

  /* ---------- L1 相机层：拍照回调 ---------- */
  try {
    var CI = Java.use("com.chaoxing.camera.CameraInterface");
    log("CameraInterface methods: " + Object.keys(CI).filter(function (k) { return k.indexOf("take") >= 0 || k.indexOf("Picture") >= 0; }).join(","));
  } catch (e) { log("CameraInterface hook skip: " + e); }

  /* ---------- L5 H5 层：getUserMedia / 文件选择 ---------- */
  if (CONFIG.webcam) {
    try {
      var WCC = Java.use("android.webkit.WebChromeClient");
      WCC.onPermissionRequest.implementation = function (req) {
        try { log("H5 onPermissionRequest " + req.getResources()); req.grant(req.getResources()); } catch (e) {}
      };
    } catch (e) { log("onPermissionRequest hook skip: " + e); }
  }
  try {
    var WCC2 = Java.use("android.webkit.WebChromeClient");
    WCC2.onShowFileChooser.implementation = function (wv, cb, params) {
      log("H5 onShowFileChooser mode=" + params.getMode() + " accept=" + params.getAcceptTypes());
      if (CONFIG.mode === "inject" && javaFileOk(CONFIG.face)) {
        try {
          var Uri = Java.use("android.net.Uri"); var F = Java.use("java.io.File");
          var arr = Java.array("android.net.Uri", [Uri.fromFile(F.$new(CONFIG.face))]);
          cb.onReceiveValue(arr); log("  -> returned " + CONFIG.face); return true;
        } catch (e) { log("  fileChooser inject failed " + e); }
      }
      return this.onShowFileChooser(wv, cb, params);
    };
  } catch (e) { log("onShowFileChooser hook skip: " + e); }
  // H5 里的签到/采集 URL 观察
  try {
    var WV = Java.use("android.webkit.WebView");
    WV.loadUrl.overload("java.lang.String").implementation = function (u) { if (String(u).indexOf("sign") >= 0 || String(u).indexOf("face") >= 0) log("WebView.loadUrl " + u); return this.loadUrl(u); };
    WV.evaluateJavascript.overload("java.lang.String", "android.webkit.ValueCallback").implementation = function (js, cb) { if (String(js).indexOf("face") >= 0 || String(js).indexOf("sign") >= 0) log("evaluateJavascript " + js); return this.evaluateJavascript(js, cb); };
  } catch (e) { log("WebView hook skip: " + e); }

  log("hooks installed");
});
