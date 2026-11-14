# xuexitong — 学习通 Android 客户端签到模块逆向研究

> 学习通（com.chaoxing.mobile）6.7.8 的**加固解壳 → 签到协议还原 → 自动化提交**完整研究记录。
> 仓库私有。全部结论基于对本人账号所用客户端的静态/动态分析，仅用于本人考勤事务的自动化。

## 样本

| 项 | 值 |
|---|---|
| 文件 | `学习通.apk`（263,211,994 B） |
| sha256 | `bd020876a60d61deffd9819440faf0890e3d7b544a4396559817b2142fa8cb14` |
| package / version | com.chaoxing.mobile / versionCode 10946 / versionName 6.7.8 |
| compileSdk / minSdk / targetSdk | 34 / 21 / 30 |
| 加固 | 梆梆安全（Bangcle / SecNeo）：`application=com.secneo.apkwrapper.AW`、`appComponentFactory=com.secneo.apkwrapper.AP` |
| 真实 dex | `classes.dex` 头声明 file_size 98,377,912，但真实内容止于 ~24,728 B，其后 98 MB 为加密载荷 |

解壳后取出 **11 个真 dex（合 121 MB）**，见 `evidence/dexes.sha256`。

## 结论速览：签到一共四条提交通道

| 通道 | 入口（反编译位置） | 提交请求 | 何时用 |
|---|---|---|---|
| **A 原生扫签** | `com.chaoxing.mobile.sign.ui.SignInfoActivity.m5` → `r5` | `GET https://fanyappfy.chaoxing.com/usersign/addsign?signId=&userId=&time=&phoneId=&enc=&ctype=stusign` | 二维码内容是 `{"time":..,"signId":..}` |
| **B H5 扫签** | `com.chaoxing.mobile.main.f.s`（前缀 `SIGNIN:`）→ `com.chaoxing.mobile.s.I7` → WebView | `GET https://mobilelearn.chaoxing.com/newsign/studentSign?rcode=<urlencoded>&uid=<uid>` | 二维码内容是 `SIGNIN:...` |
| **C 大屏二维码** | 服务端页面 `widget/sign/e?id=..&c=..&enc=..`（页面是网页，App 里只有它的后端 API `widget/sign/api/findPuidsByActiveId`） | `GET https://mobilelearn.chaoxing.com/pptSign/stuSignajax?enc=&name=&activeId=&uid=&clientip=&useragent=&latitude=-1&longitude=-1&fid=&appType=15` | 教室大屏/投影上的二维码 |
| **D 免二维码直签** | 列表接口 `/ppt/activeAPI/courseactivelist`、`/ppt/activeAPI/taskactivelist`、`/mycourse/backclazzdata` | 同 C，只要 `activeId` | **没有二维码也能签**（普通/定位/签到码等类型） |

### 通道 A 的 enc 是纯本地 MD5（关键突破）

```
enc = MD5( signId + "-" + userId + "-" + time + "-" + phoneId )     # com.fanzhou.util.j.d
phoneId: SharedPreferences "appProfile"/"uniqueId"；无值时 = UUID 去横线（32 位 hex）→ 可自造
成功判定：响应 JSON 的 statusCode == 300
错误码：301 插入失败 / 306 enc验证错误 / 307 二维码时间过期 / 308 签到id不存在
        309 用户不存在 / 310 单位信息错误 / 311 角色错误 / 312 系统错误
```

**所以通道 A 完全不需要相机、不需要人脸、不需要人到场**：只要二维码里的 `signId`+`time`、自己的 `puid`、一个自己生成的 `phoneId`、一条登录 cookie。

### 服务端校验顺序（实测，排错很有用）

| 端点 | 无 cookie + 假参数的响应 | 含义 |
|---|---|---|
| `fanyappfy…/usersign/addsign` | `{"msg":"signId  not exists","statusCode":308}` | 先查 signId → time → enc → 用户；未登录不会先报登录错 |
| `mobilelearn…/pptSign/stuSignajax` | `HTTP 200` 文本 `请先登录再进行签到` | 先校验登录，必须有 cookie |

### 动态二维码（几秒刷新）不是防护

大屏二维码里 **只有显示计数 `c` 每 10 秒变，`id` 与 `enc` 全程不变**，提交时服务端只要 `enc` → **任意时刻的一张截图永久有效**。真正的瓶颈是"你多久能拿到二维码"，因此本仓库提供五档中继（见 `docs/报告-已解壳版.md` 第 12 章）。

### 人脸

- 全 App 的人脸只挂在两处：H5 桥 `com.chaoxing.mobile.webapp.jsprotocal.exam.FaceRecognitionExecutor` 与 office 打卡 `/api/apps/punch/user/face/verify[match]`。
- **签到两条提交链路的参数里没有任何人脸字段** → 不打开 H5 页面就不会触发人脸；比对对象是云端已存的 `remoteImage`（本人照片），活体只是客户端状态位 `CollectResult.liveDetectionStatus`。

## 快速开始

```bash
pip install -r requirements.txt          # requests / opencv-python-headless

# 1) 一条二维码就签（内容文本 / 截图 / 都行）
python3 scripts/qr_sign_remote.py --qr '{"time":"1712000000","signId":"1234567890"}' \
        --uid <你的puid> --cookie-file ck.txt

# 2) 动态二维码：自动看屏（adb / macOS 截屏），解出即签
python3 scripts/qr_relay.py --source adb --serial emulator-5554 --submit \
        --uid <puid> --cookie-file ck.txt --interval 0.7 --stop-on-success

# 3) 没有二维码的活动：轮询 + 自动提交
python3 scripts/autosign.py --uid <puid> --cookie-file ck.txt --name 张三 --fid 12345 --loop --interval 30

# 4) 中继服务（把"看得见二维码的机器"和"握着 cookie 的机器"分开）
python3 scripts/qr_sign_remote.py --serve 8765 --uid <puid> --cookie-file ck.txt --token mysecret
```

cookie 三种来源：Frida `dumpcookie`（`scripts/frida_sign_hook.js`）、mitmproxy、浏览器 Copy as cURL。

## 目录

```
docs/报告-已解壳版.md      完整报告（12 章，解壳 / 协议 / 人脸 / 动态二维码）
docs/报告-静态初版.md      加固前的静态可达面分析（对照用）
docs/签到类型全表.md       ★ 不同课程的不同签到方式：判定方法 + 每类必需参数
docs/工装与环境.md         从零搭出可复现环境（AVD / frida / dump / droidasc）
scripts/                   56 个脚本：解壳、协议重放、自动签到、Frida hook、抓屏中继
userscript/                油猴脚本：在渲染二维码的电脑上直接解码上报
evidence/                  证据：类清单、字符串、findrefs 结果、反编译源码、dex 校验
```

## 边界

- 本仓库只处理**本人账号**的考勤事务，不含任何他人数据、不含账号密码、不含 cookie。
- 所有脚本的 `--uid` / `--cookie-file` 都由使用者自己提供；仓库内没有任何凭据。
- 报告中的判定接口（`signDetail` 等）为服务端公开接口，仅用于识别签到类型。
