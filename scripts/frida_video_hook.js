/*
 * frida_video_hook.js — 学习通视频任务点上报链路抓取/校验
 *
 * 目的：拿到**真值**来验证 video_task.py 的公式
 *   1) enc 明文（com.fanzhou.util.j.d 的入参，形如 [clazzId][puid][jobid][objectId][ms][盐][ms][clip]）
 *   2) 完整上报 URL（含服务端下发的 reportUrl 形状，静态里看不到）
 *   3) 每次上报的服务器判定（CourseDotRes: result / rollbackStatus / rollbackPoint）
 *
 * 用法（AVD 或真机，frida-server 已推入）：
 *   frida -U -f com.chaoxing.mobile -l scripts/frida_video_hook.js --no-pause
 *   然后正常去课程里播一段视频（拖动一次更好，能抓到 isdrag=1 的分支）。
 *   抓到的行同时打到 console 和 /data/local/tmp/cx_video_cap.jsonl：
 *     adb shell cat /data/local/tmp/cx_video_cap.jsonl
 *   再校验：
 *     python3 scripts/video_task.py --verify-capture cap.json     # 每行一个 JSON 对象
 */
'use strict';

var CAP_FILE = '/data/local/tmp/cx_video_cap.jsonl';
var WRITE_FILE = true;
var LOG_URLS = true;
var captures = [];

function nowMs() { return Date.now(); }

function save(obj) {
    obj.t = nowMs();
    captures.push(obj);
    if (captures.length > 500) captures.shift();
    var line = JSON.stringify(obj);
    console.log('[cap] ' + line);
    if (!WRITE_FILE) return;
    try {
        var F = Java.use('java.io.File');
        var FW = Java.use('java.io.FileWriter');
        var fw = FW.$new(F.$new(CAP_FILE), true);
        fw.write(line + '\n');
        fw.flush();
        fw.close();
    } catch (e) {
        console.log('[cap] 写文件失败（不影响 console 输出）：' + e);
    }
}

function looksLikeEncPlain(s) {
    return s.length > 16 && s.charAt(0) === '[' && s.indexOf('][') > 0 && s.charAt(s.length - 1) === ']';
}

function md5Of(s) {
    try {
        var MD5 = Java.use('java.security.MessageDigest').getInstance('MD5');
        var bytes = Java.use('java.lang.String').$new(s).getBytes('UTF-8');
        MD5.update(bytes);
        var d = MD5.digest();
        var out = '';
        for (var i = 0; i < d.length; i++) {
            var h = (d[i] & 0xff).toString(16);
            out += (h.length === 1 ? '0' : '') + h;
        }
        return out;
    } catch (e) {
        return null;
    }
}

function hookEnc() {
    try {
        var J = Java.use('com.fanzhou.util.j');
        J.d.overload('java.lang.String').implementation = function (s) {
            var r = this.d(s);
            if (looksLikeEncPlain(s)) {
                save({ kind: 'enc', plain: s, salt_plain_len: s.length, enc: r, local_md5: md5Of(s) });
            }
            return r;
        };
        console.log('[+] hooked com.fanzhou.util.j.d —— enc 明文/密文一起抓');
    } catch (e) {
        console.log('[-] hook enc 失败：' + e);
    }
}

function hookViewModel() {
    try {
        var CVM = Java.use('com.chaoxing.mobile.player.course.viewmodel.CourseViewModel');
        CVM.S.implementation = function (ctx, playingMs, isdrag, clipMs, mode, owner, cb) {
            save({
                kind: 'commit_call',
                playing_ms: playingMs,
                playing_sec: Math.floor((playingMs >= 0 ? playingMs : 0) / 1000),
                isdrag: isdrag,
                clip_ms: clipMs,
                clip_sec: Math.floor((clipMs >= 0 ? clipMs : 0) / 1000),
                mode: mode
            });
            return this.S(ctx, playingMs, isdrag, clipMs, mode, owner, cb);
        };
        console.log('[+] hooked CourseViewModel.S —— 拿到 playingTime / isdrag / clipTime 的真实来源');
    } catch (e) {
        console.log('[-] hook CourseViewModel.S 失败：' + e);
    }
}

function hookSender() {
    try {
        var B = Java.use('com.chaoxing.mobile.player.course.model.b');
        B.g.overload('android.content.Context', 'java.lang.String', 'androidx.lifecycle.LifecycleOwner',
                      'com.chaoxing.mobile.study.course.e').implementation = function (ctx, url, owner, cb) {
            save({ kind: 'report_url', url: url, len: url.length });
            return this.g(ctx, url, owner, cb);
        };
        console.log('[+] hooked model.b.g —— 抓到完整上报 URL（含服务端下发的 reportUrl）');
    } catch (e) {
        console.log('[-] hook model.b.g 失败：' + e);
    }
}

function hookVerdict() {
    try {
        var F = Java.use('com.chaoxing.mobile.player.course.CoursePlayerFragment');
        F.Ua.implementation = function (res) {
            try {
                save({
                    kind: 'verdict',
                    result: res.getResult(),
                    rollbackPoint: res.getRollbackPoint === undefined ? null : res.getRollbackPoint(),
                    rollbackStatus: res.isRollbackStatus === undefined ? null : res.isRollbackStatus(),
                    errorMsg: res.getErrorMsg === undefined ? null : res.getErrorMsg()
                });
            } catch (e2) { }
            return this.Ua(res);
        };
        console.log('[+] hooked CoursePlayerFragment.Ua —— 抓到服务器判定与回退点');
    } catch (e) {
        console.log('[-] hook CoursePlayerFragment.Ua 失败：' + e);
    }
}

function hookOkHttp() {
    if (!LOG_URLS) return;
    try {
        var Client = Java.use('okhttp3.OkHttpClient');
        Client.newCall.implementation = function (req) {
            try {
                var u = req.url().toString();
                if (u.indexOf('chaoxing') >= 0) {
                    save({ kind: 'http_req', method: req.method(), url: u });
                }
            } catch (e) { }
            return this.newCall(req);
        };
        console.log('[+] hooked OkHttpClient.newCall');
    } catch (e) {
        console.log('[-] hook OkHttpClient.newCall 失败：' + e);
    }
    try {
        var Chain = Java.use('okhttp3.internal.http.RealInterceptorChain');
        Chain.proceed.overload('okhttp3.Request').implementation = function (req) {
            var resp = this.proceed(req);
            try {
                var u = req.url().toString();
                if (u.indexOf('chaoxing') >= 0) {
                    var body = '';
                    try { body = resp.peekBody(8192).string(); } catch (e3) { }
                    save({ kind: 'http_resp', url: u, code: resp.code(), body: body.slice(0, 800) });
                }
            } catch (e2) { }
            return resp;
        };
        console.log('[+] hooked RealInterceptorChain.proceed —— 抓状态码与响应体（203/回退用得上）');
    } catch (e) {
        console.log('[-] hook RealInterceptorChain.proceed 失败：' + e);
    }
}

/* ---------------- RPC ---------------- */
rpc.exports = {
    captures: function () { return JSON.stringify(captures); },
    last: function () { return captures.length ? JSON.stringify(captures[captures.length - 1]) : 'null'; },
    clear: function () { captures = []; return true; },
    setwrite: function (v) { WRITE_FILE = !!v; return WRITE_FILE; },
    capfile: function () { return CAP_FILE; }
};

Java.perform(function () {
    console.log('[i] 抓取文件：' + CAP_FILE + '（frida RPC: captures()/last()/clear()/setwrite()）');
    hookEnc();
    hookViewModel();
    hookSender();
    hookVerdict();
    hookOkHttp();
    console.log('[i] 现在去课程里播一段视频；拖动进度条一次能抓到 isdrag=1。');
});
