// ==UserScript==
// @name         学习通 / 大屏二维码秒级中继 (Chaoxing QR Relay)
// @namespace    local.chaoxing.relay
// @version      1.0
// @description  每 0.5 秒解码页面上的签到二维码，把内容 POST 给本地中继（qr_sign_remote.py --serve）。用于「几秒刷新」的动态二维码：不用人截图，机器自己看。
// @match        *://mobilelearn.chaoxing.com/*
// @match        *://*.chaoxing.com/*
// @require      https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.js
// @grant        GM_xmlhttpRequest
// @grant        GM_setValue
// @grant        GM_getValue
// @connect      127.0.0.1
// @connect      localhost
// @run-at       document-idle
// ==/UserScript==
/*
 * 为什么能这么干：
 *   教师大屏的二维码是网页渲染的（mobilelearn.chaoxing.com/widget/sign/e?id=..&c=..&enc=..）。
 *   其中 c 每 10 秒递增（显示用计数），**id 与 enc 从签到开始到结束都不变** —— 服务端提交时只要 enc。
 *   所以在能看见这个页面的机器上解码一次，后续无论过多久都能签。
 * 部署：Tampermonkey 装上本脚本 -> 点脚本菜单配置中继地址与 token -> 打开/停在教师大屏页。
 *   中继端：python3 qr_sign_remote.py --serve 8765 --uid <puid> --cookie-file ck.txt --token mysecret
 */
(function () {
  'use strict';
  const CFG_KEY = 'cx_relay_cfg';
  let cfg = Object.assign({ relay: 'http://127.0.0.1:8765', token: '', auto: true, interval: 500 },
                          JSON.parse(GM_getValue(CFG_KEY, '{}') || '{}'));
  let lastHash = '';
  let sent = 0, failed = 0;

  function saveCfg() { GM_setValue(CFG_KEY, JSON.stringify(cfg)); }

  function decodeCanvas(cv) {
    try {
      const ctx = cv.getContext('2d');
      const d = ctx.getImageData(0, 0, cv.width, cv.height);
      if (typeof jsQR !== 'function') return null;
      const r = jsQR(d.data, d.width, d.height, { inversionAttempts: 'dontInvert' });
      return r && r.data ? r.data : null;
    } catch (e) { return null; }
  }

  function decodeImg(img) {
    try {
      const cv = document.createElement('canvas');
      cv.width = img.naturalWidth || img.width;
      cv.height = img.naturalHeight || img.height;
      if (!cv.width || !cv.height) return null;
      cv.getContext('2d').drawImage(img, 0, 0);
      return decodeCanvas(cv);
    } catch (e) { return null; }   // 跨域图片会污染 canvas，直接忽略
  }

  function scan() {
    const found = [];
    document.querySelectorAll('canvas').forEach(c => { const t = decodeCanvas(c); if (t) found.push(t); });
    document.querySelectorAll('img').forEach(i => { const t = decodeImg(i); if (t) found.push(t); });
    // 有些页面把二维码链接直接写在 DOM/JS 里
    const html = document.documentElement.innerHTML;
    const m = html.match(/https?:\/\/[^"'\s]*widget\/sign\/e\?[^"'\s<]+/g);
    if (m) m.forEach(x => found.push(x.replace(/&amp;/g, '&')));
    return found;
  }

  function push(text) {
    const h = text.length + ':' + text.slice(0, 40) + ':' + text.slice(-40);
    if (h === lastHash) return;
    if (cfg.relay.indexOf('widget/sign') >= 0) return;
    lastHash = h;
    const url = cfg.relay.replace(/\/$/, '') + '/sign?token=' + encodeURIComponent(cfg.token);
    GM_xmlhttpRequest({
      method: 'POST',
      url: url,
      data: text,
      headers: { 'Content-Type': 'text/plain' },
      onload: r => {
        sent++;
        console.log('[CX-Relay] ->', r.status, r.responseText.slice(0, 300));
        badge(sent, failed);
      },
      onerror: () => { failed++; badge(sent, failed); }
    });
  }

  function badge(ok, bad) {
    let el = document.getElementById('cx-relay-badge');
    if (!el) {
      el = document.createElement('div');
      el.id = 'cx-relay-badge';
      el.style.cssText = 'position:fixed;right:8px;bottom:8px;z-index:2147483647;background:#111;' +
        'color:#0f0;font:12px/1.4 monospace;padding:6px 8px;border-radius:6px;opacity:.85';
      document.body.appendChild(el);
    }
    el.textContent = 'CX-Relay ' + cfg.relay + '  ok=' + ok + ' fail=' + bad;
  }

  function loop() {
    if (cfg.auto) {
      const list = scan();
      if (list.length) push(list[0]);
    }
    setTimeout(loop, cfg.interval);
  }

  // 菜单：配置中继
  function menu() {
    const r = prompt('中继地址（qr_sign_remote.py --serve 的地址）', cfg.relay);
    if (r) cfg.relay = r.trim();
    const t = prompt('token（服务端 --token，没有就留空）', cfg.token);
    if (t !== null) cfg.token = t.trim();
    saveCfg();
    alert('已保存：' + cfg.relay + '  token=' + (cfg.token || '(空)'));
    location.reload();
  }

  if (typeof GM_registerMenuCommand === 'function') {
    GM_registerMenuCommand('配置中继地址', menu);
    GM_registerMenuCommand('立即扫描一次并上报', () => { const l = scan(); if (l.length) { lastHash = ''; push(l[0]); } else alert('页面上没找到二维码'); });
  }
  console.log('[CX-Relay] loaded, relay=' + cfg.relay);
  loop();
})();
