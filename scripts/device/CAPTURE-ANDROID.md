# 学习通 · 真机 Android 抓包 / 复现作战清单

目的：拿到一次成功拍照签到的三跳原始数据，闭合 photoAuthError_PCR007。

## 一、你需要做的三件事
1. 手机开 USB 调试：设置 → 关于手机 → 连点「版本号」7 次 → 开发者选项 → 打开「USB 调试」
2. 数据线插电脑，手机弹「允许 USB 调试」→ 勾「一律允许」（看清指纹再点）
3. 手机上的学习通登录到那个能签到的账号，停在拍照签到页（别退出）

顺便告诉我三样：机型 / Android 版本 / 有没有 root（Magisk），这决定走哪条路线。

## 二、环境自检（连上就让我跑）

    bash scripts/device/android_check.sh

## 三、三条路线，按顺序试

### S1 chrome://inspect 看 WebView ★ 首选（不需要 root、不需要证书、不改网络）
1. 电脑 Chrome 打开 chrome://inspect/#devices，勾上 Discover USB devices
2. 手机上打开学习通，进拍照签到页
3. Chrome 里出现 com.chaoxing.mobile 的 WebView → 点 inspect
4. Console 里粘 scripts/device/webview_console.js 的内容 → 一次性把 PHOTO_RESULT / deviceCode / cookie / fid / objectId 全打出来
5. Network 面板找到 /pptSign/stuSignajax → 右键 → Copy → Copy as cURL ← 这就是我最想要的那一份
6. 没出现 WebView：说明 App 没开 setWebContentsDebuggingEnabled → 走 S2（或 S3 里用 frida 强制打开）

### S2 mitmproxy（USB 代理，不用动 WiFi）

    bash scripts/device/mitm_capture.sh start   # 起代理 + adb reverse + 设备全局 http_proxy
    # ... 手机上做一次拍照签到 ...
    bash scripts/device/mitm_capture.sh stop    # 一定要执行，否则手机没网

注意（很重要）：Android 7+ 的 App 默认不信任用户安装的 CA。
- 能 root：把 CA 装进系统证书（/system/etc/security/cacerts，Magisk 用 Move Certificates 模块）→ native + WebView 全可见
- 不能 root：WebView 里的 H5 请求（preSign / stuSignajax）大概率能解，原生上传（pan-yz）会 TLS 失败 → 那就从 S1 的 Console 里取 objectId，或走 S3

### S3 root + frida（最完整，能直接读内存里的请求）

    # 前提：adb shell su -c id 返回 uid=0
    adb push frida-server-17.26.3-android-arm64 /data/local/tmp/fsd
    adb shell chmod 755 /data/local/tmp/fsd
    adb shell 'setsid /data/local/tmp/fsd -D </dev/null >/data/local/tmp/fsd.log 2>&1 &'
    frida -U -f com.chaoxing.mobile -l scripts/hide_env.js -l scripts/device/frida_android_capture.js

hide_env.js 必须一起加载：学习通是梆梆加固，frida 会被检测自毁（模拟器上实测 0.0s 就被杀）。
真机没有模拟器检测，成功率比模拟器高一个数量级，但反 frida 那一层仍在。

## 四、要回收的六样（截图/文本都行，别裁掉 Cookie 和 User-Agent）
1. POST /pptSign/stuSignajax 的完整请求头 + body + 响应原文
2. PHOTO_RESULT 的原值（页面 JS 变量，Console 里直接敲）
3. deviceCode、fid、name、uid 的实际值
4. Cookie 全量（Console: document.cookie）
5. 上传响应 JSON（objectId / resid / data.encryptedId / crc）
6. 如果是 H5：预签页响应 HTML（含 enc 隐藏域）

## 五、踩坑提醒
- 抓包期间手机别切蜂窝、关掉「私人 DNS」；QUIC/HTTP3 会绕过代理
- Android 上 WebView 调试开关在 App 侧，S1 看不到属正常
- 抓完一定 mitm_capture.sh stop，否则手机会像断网
- 别在设备上执行 settings put global adb_enabled 0（会把 adb 永久搞成 offline）
