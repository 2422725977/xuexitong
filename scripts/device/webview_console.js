// 学习通拍照签到页 · 取证片段（chrome://inspect -> Console 整段粘贴）
// 目标：一次拿到 PHOTO_RESULT / deviceCode / fid / name / uid / cookie / objectId / UA
(function () {
  function g(n, d) { try { return eval(n); } catch (e) { return d; } }
  var out = {};
  out.href = String(location.href);
  out.cookie = document.cookie;
  out.uid = g('typeof uid !== "undefined" ? uid : null', null);
  out.acId = g('typeof acId !== "undefined" ? acId : null', null);
  out.fid_var = g('typeof fid !== "undefined" ? fid : null', null);
  out.fid_dom = (document.getElementById('fid') || {}).value || null;
  out.name = g('typeof name !== "undefined" ? name : null', null);
  out.name2 = g('typeof name2 !== "undefined" ? name2 : null', null);
  out.deviceCode = g('typeof deviceCode !== "undefined" ? deviceCode : null', null);
  out.PHOTO_RESULT = g('typeof PHOTO_RESULT !== "undefined" ? PHOTO_RESULT : null', null);
  var img = document.getElementById('image_1');
  out.objectId = img ? img.getAttribute('nvalue') : null;
  out.userAgent = navigator.userAgent;
  out.hasCaptcha = !!(window.mySignCaptchaUtils);
  out.validate = (window.mySignCaptchaUtils && window.mySignCaptchaUtils.VALIDATE_CODE_STR) || null;
  out.jsBridge = (typeof jsBridge !== 'undefined') ? 'jsBridge ok' : 'no jsBridge';
  out.winKeys = Object.keys(window).filter(function (k) { return /sign|bridge|captcha|photo|face/i.test(k); }).slice(0, 40);
  console.log(JSON.stringify(out, null, 2));
  try { copy(JSON.stringify(out)); console.log('已复制到剪贴板'); } catch (e) {}
  return out;
})();
// 第二步：页面里已经挂了一张图时，原地重放一次提交，看服务端到底回什么：
// sign();
// 第三步：Network 面板 -> /pptSign/stuSignajax -> 右键 -> Copy -> Copy as cURL