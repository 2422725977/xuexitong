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

## 签到之外：学生高频操作 + 伪装层 + 风控层 + 视频任务点（报告第 13/14/15 章）

签到链路本身已复核**无遗漏**；本轮补的是「签到之外」和「伪装层」：

- `docs/学生高频操作接口.md`：
  - **视频/音频任务点进度上报**（挂机/秒过）——`CourseViewModel.S` 参数表 + `enc` 公式（盐 `d_yHJ!$pdA~5`，`[`/`][`/`]` 分隔）；URL 是服务端下发的 `CourseVideo.reportUrl`
  - **取真值的低暴露姿势**：[`docs/低暴露抓取.md`](docs/低暴露抓取.md) —— 浏览器 cookie（零设备信号）> 手机导出 cookie > 模拟器登录（新设备+模拟器指纹，最差）；含尺度纪律与 `scripts/fsd.sh`（非默认端口、抓完即清）
  - **视频任务点协议（★ 新增，本轮定稿）**：[`docs/视频任务点协议.md`](docs/视频任务点协议.md) —— enc 明文模板 + 单位坑（查询串秒 / enc 毫秒、必为 1000 整数倍）+ 服务端 `result=203` 与 `rollbackPoint` 回退机制 + 门禁与开关（reportTimeInterval/doubleSpeed/fastforward/faceRecConfig）+ 五项待实测；脚本 `scripts/video_task.py`（`--selftest` 全绿、`--dry-run` 干跑、`--pace real` 按真实节奏）与 `scripts/frida_video_hook.js`（抓 reportUrl 真值）
  - **未完成活动巡检** `teachingPlanAPI/noFinishActiveCount`（不签到也能知道有没有新东西）
  - 作业/考试直跳 `task/getStuWorkAndExamSkipUrl`、讨论/投票、直播、成绩、课程任务点 `gas/course`、`work/task/library`
  - 活动体系全景（学生侧 17 个接口 + 教师侧 12 个）
  - 两条此前只提前缀的到课链路：`INTELLIGENT_CLASSROOM:` → `intelligentclassroom.ConfirmScreenActivity`；座位核销 → `reserveseat.ui.QRcodeVerifyActivity`
- `docs/隐身与风控.md`（v2）：客户端两条旁证链（`analysis/ac_event`、`analysis/datalog`）、服务端可见信号 10 项排序、**六维伪装**（身份/指纹/头/时序/流量/审计）、**三层风控**（判级 HALT/COOLDOWN/WARN/NOTICE/OK + 闸门 + 调用方熔断）、9 条反模式、A/B 验证设计。
  - 用法：给任意提交脚本加 `--stealth`（`autosign.py`、`qr_sign_remote.py` 已支持），签到前会先发 1–2 条只读学习请求做掩护；再加 `--max-writes-per-hour / --min-interval / --quiet-hours` 控制写频率。
  - 被风控时脚本会打印 `[STOP]`（登录失效/验证码/403，停手）或 `[WAIT]`（限流/配额满，本轮不重试），并落盘审计 `~/.chaoxing_audit.jsonl`（长值打码）。
  - 体检与回归：`python3 scripts/stealth_session.py --doctor`（六维）、`python3 scripts/selftest.py`（43 项全绿）、`python3 scripts/risk_guard.py --monitor`（实时盯风控）。

### 一键自动签到流水线（★ 新增）

`scripts/cx_pipeline.py` 把「教师侧取当前二维码 → 学生侧提交」的中间过程全部粘好一条命令：

```bash
# 教师 cookie 放 ck_tch.txt（浏览器 F12 复制整条 Cookie）；学生 cookie 放 ck.txt
python3 scripts/cx_pipeline.py --mode watch \
    --tch-cookie-file ck_tch.txt --stu-cookie-file ck.txt --uid <学生puid> \
    --course <courseId> --class <classId> --stop-on-success --verbose

# 没有教师 cookie 也能自动登（cookie 失效会当场重登一次）
export CX_TCH_PHONE=1xxxxxxxxxx CX_TCH_PASS=********
python3 scripts/cx_pipeline.py --mode watch --tch-login --stu-cookie-file ck.txt --uid <学生puid>
```

- 四段全自动：教师班级枚举 → 活跃活动定位 → **教师侧取 enc（页面正则 + 二维码图片 cv2 多尺度解码，双路并存，候选带评分排序）** → 学生侧 `pptSign/stuSignajax` 提交。
- 取不到 enc **不静默**：每个可疑响应落盘 `out/tch_probe/*.html`（文件头写了请求与最终跳转 URL），判定流水写 `out/pipeline.jsonl`。
- 模式：`discover`（只枚举不提交）/ `once` / `watch`（默认）/ `submit-url`（已有 enc 直接提交）/ **`create`（教师侧新建签到 → 取码 → 提交，一条命令）**。

**新建一个"不扫脸"的签到并当场签成**（教师页发起签到表单 `POST /pptSign/newTaskSign`，详见 `docs/一键自动签到.md` 第 12 章）：

```bash
python3 scripts/cx_pipeline.py --mode create --uid <学生puid> \
    --tch-cookie-file ck_tch.txt --stu-cookie-file ck.txt \
    --course <courseId> --class <classId> \
    --create-type 2 --time-long 1800000 --want-type 2 --max-submits 1 --verbose
# --create-type：0 普通 / 1 拍照 / 2 二维码 / 3 手势 / 4 位置 / 5 签到码
# 默认 --no-face（openCheckFaceFlag=0）；--sign-address 改位置签到（--lat/--lon/--address）
# --auto-create：watch 模式下没有可用活动时自动建一个
```

- 位置类签到的硬约束：提交必须**同时**带 `location` 与 `locationResult`（同一个 JSON 串），只带一个得到 `errorLocation3`；位置真值从教师活动页 `widget/active/teaActiveView` 的活动 `content` 取（`signDetail` 里只有 `latitude/longitude=-1`）。
- 依据（三条实测）：学生端页面 `var aidInEwm=""; var enc="";` 只能靠扫码回调赋值；`newsign/signDetail` 带 4 种 msg 参数返回 69 字段完全一致、无 enc；服务端错误文案分类（clone → «签到失败，请重新扫描» / 父活动 → «此次签到未开始»）证明唯一门槛就是 enc。
- 详见 [`docs/一键自动签到.md`](docs/一键自动签到.md)。

## 扫码签到：一张截图就够（★ 2026-11-23 真机实测）

二维码签到的真身只有一串 `enc`，「扫码」只是把它从图里读出来。实测有效窗：

| 二维码模式 | 有效窗 | 结论 |
|---|---|---|
| 不刷新（ifRefreshEwm=0） | ≥25 秒（25s 后仍 success） | 一张截图长期有效 |
| 5 秒刷新（ifRefreshEwm=1, ewmRefreshTime=5） | 约 10 秒（6.1s/10.2s success，14.3s 失效） | 能签，但必须「拿到图 → 自动提交」 |

```bash
# 别人把二维码截图丢进目录
python3 scripts/qr_watch.py --source folder --dir out/qrdrop --uid <puid> --cookie-file ck.txt --stop-on-success
# 二维码显示在手机屏幕上
python3 scripts/qr_watch.py --source adb --serial <序列号> --uid <puid> --cookie-file ck.txt --stop-on-success
# 复现动态大屏码（教师侧）
python3 scripts/qr_screen_sim.py --aid <aid> --out out/qrdrop --interval 1.5 --count 60 --serve 8899
```

- 两次端到端实录均为「第 1 次提交即 success」（folder 源 / 真机截屏源），全程无摄像头、无本人到场。
- 学生 cookie 取不到当前码（refreshQRCode 回「暂无权限」），学生侧只有「拿码 → 提交」这一半。
- 提示：抢签别套 `--stealth` 风控层（8 秒最小间隔会把 5 秒窗口拖没），qr_watch.py 默认裸发。
- 详见 [`docs/一键自动签到.md`](docs/一键自动签到.md) 第 17 章与 [`docs/报告-已解壳版.md`](docs/报告-已解壳版.md) 第 25 章。

## 没有教师账号、没有二维码时能做到什么（报告第 26 章）

| 签到类型 | 只有学生 cookie | 你需要准备的 |
|---|---|---|
| 普通签到 | ✅ 完全可签 | 什么都不用——activelist 会自己发现活动 |
| 位置签到 | ✅ 完全可签，人不用到场 | 什么都不用——地址文本活动里就有，距离预言机爬坡定位 |
| 二维码签到 | ⚠️ 需要 enc | 一张十秒内的码截图（静态码一张永久有效） |
| 签到码 / 手势 | ❌ | 必须有人把码告诉你（连错 6 次锁 1 小时，枚举不可行） |
| 拍照 / 人脸 | ❌ | 旧账（拍照专项 / 人脸章节） |

两个关键武器：**activelist 自动发现**（`/v2/apis/active/student/activelist`，一次 70+ 条活动，教师刚建的活动 1 秒入列）与 **距离预言机**（位置签到提交假坐标时服务端把真实距离写进错误文案，用「中心点 + 两个梯度探针」爬坡，2–3 轮落进 500 米范围，误差 ≈200 米）。

```bash
python3 scripts/stu_guard.py --cookie-file ck.txt --uid <puid> \
    --course-id <courseId> --class-id <classId> --interval 12 --log out/guard.log
```

实测一轮：新活动 11 个 → 普通 success、位置 3 步 success，二维码/签到码/手势/拍照自动归「需人工」`{"signed":5,"needs_secret":6,"fail":0}`。

## 反封号 / 反风控策略层（报告第 27 章，★ 2026-11-23）

四个写操作脚本（`stu_guard.py` / `video_task.py` / `cx_pipeline.py` / `qr_watch.py`）现在共用一个**账号级策略中心**
`scripts/risk_center.py`：写前过闸门（allow）、写后入账（observe）、全程脱敏审计。默认开启，`--no-risk-center` 关闭。

| 规则 | 管什么 |
|---|---|
| R1 只读先行 | 同域 5 分钟内必须有成功的只读探针，才允许写（缺了会自愈补一次真实 GET，不造假） |
| R2 单调进度 | 视频进度只增不跳，步长上限 = reportTimeInterval×3，触发 rollback 自动降速 |
| R3 目标上限 | 同一 activeId / jobId 最多写 3 次（爬坡探针 12 次），不来回轰炸同一个活动 |
| R4 双配额 | 按动作分档：sign 6/小时、sign_probe 30/小时、tch_write 30/小时、qr_sign 120/小时… |
| R5/R6 节奏 | 活跃窗 6–23（抢签豁免）、静默窗 1–6、真人抖动 + 每若干次插 3–12 分钟长停顿 |
| R7 分级熔断 | 限流 → 冷却 30 分；软信号累计 2 次 → 2 小时；登录失效/验证码/403 → HALT 24 小时 |
| R8/R9/R10 | 全审计（enc/token/cookie/uid 等打码）· 不伪造埋点 · 连续失败 3 次退避 15 分钟 |

```bash
python3 scripts/risk_center.py --status        # 还剩多少配额、是否熔断、探针是否有效
python3 scripts/risk_center.py --selftest      # 35 项策略回归
python3 scripts/risk_center.py --reset --hard  # 换 cookie / 解除 HALT
python3 scripts/risk_integration_test.py       # 17 项接线回归（离线，0.15 秒）
```

★ 抢签不再"裸奔"也不被拖慢：`qr_sign` 画像 0.5 秒 / 120 次每小时、豁免真人节奏与静默窗（旧 stealth 全局 6 次/小时会拖没 5 秒窗口）；
位置爬坡用 `sign_probe`。线上实证：教师侧 tch_write 闸门建活动 → 学生侧 sign_probe 闸门签成 success → 假 cookie 触发 HALT 立即停抢。

## 快速开始

```bash
pip install -r requirements.txt          # requests / opencv-python-headless

# 1) 一条二维码就签（内容文本 / 截图 / 都行）
python3 scripts/qr_sign_remote.py --qr '{"time":"1712000000","signId":"1234567890"}' \
        --uid <你的puid> --cookie-file ck.txt

# 2) 动态二维码：自动看屏（adb / macOS 截屏），解出即签
python3 scripts/qr_relay.py --source adb --serial emulator-5554 --submit \
        --uid <puid> --cookie-file ck.txt --interval 0.7 --stop-on-success

# 3) 没有二维码的活动：轮询 + 自动提交（--stealth 走 TLS 指纹 + 掩护流量 + 拟人延迟）
python3 scripts/autosign.py --uid <puid> --cookie-file ck.txt --name 张三 --fid 12345 --loop --interval 30 --stealth
python3 scripts/stealth_session.py --probe https://mobilelearn.chaoxing.com/   # 自检伪装层

# 4) 中继服务（把"看得见二维码的机器"和"握着 cookie 的机器"分开）
python3 scripts/qr_sign_remote.py --serve 8765 --uid <puid> --cookie-file ck.txt --token mysecret
```

cookie 三种来源：Frida `dumpcookie`（`scripts/frida_sign_hook.js`）、mitmproxy、浏览器 Copy as cURL。

## 拍照签到（ifPhoto=1）：纯 HTTP 打不通，为什么

- 拍照不是独立类型：otherId=1 被服务端拒，正确形态是 otherId=0 + 修饰位 ifPhoto=1。
- 提交由 WebView 的 H5 发出（/pptSign/stuSignajax），App 只贡献 UA 头 / cookie / deviceCode / objectId 四样，四样全部试过。
- 服务端闸门是「活动级 + 请求级凭证」：不带 objectId、不带 photoResult、不带 cookie、教师身份、任意参数形状 → 一律纯文本 photoAuthError_PCR007；普通活动带同样参数回「您已签到过了」；伪造 activeId 回 tengine 500。
- 已排除：UA、fid、name、deviceCode、photoResult 形状、preSign（含 ext）、行为分析回传、ifTiJiao、GET/POST、上传通道、图片随机化。
- 上传链纯 Python 可用：api/token/uservalid 取 _token → POST /upload?_from=mobilelearn&_token=…（multipart file+puid）→ objectId 内容寻址（resid / encryptedId 每次不同）。
- deviceCode 公式已还原：Base64_no_wrap(AES-ECB-PKCS5(OAID))，桥 CLIENT_DEVICE_FLAG；另有返回 {"uuid":…} 的 CLIENT_DEVICE_ID 桥。
- 运行态结论：梆梆 VMP 多级反调试（线程名扫描 + maps 扫描 + 反 inline hook 自毁 + /proc/version 触发自杀），去模拟器化改 property 过不去；真机路线见 docs/真机抓包作战清单.md 与 scripts/device/。
- 未闭合（需要一次真机抓包）：① 会话/设备绑定 ② 活动来源 ③ objectId 来源。

## 目录

```
docs/报告-已解壳版.md      完整报告（27 章，解壳 / 协议 / 人脸 / 动态二维码 / 遗漏审计 / 伪装层与风控层 / 视频任务点 / 模拟器实测 / 一键流水线 / 权威取码与人脸闸门 / 拍照签到专项 / 真机取证 / 扫码签到全链路 / 学生端纯远程能力矩阵 / ☆ 反封号策略层）
docs/拍照签到-PCR007-专项.md  ★ 拍照签到专项：闸门定界、上传链、deviceCode 还原、外部实现对照、全部变体矩阵
docs/真机抓包作战清单.md      ★ 真机 Android 抓包/复现路线（chrome://inspect → mitmproxy → root+frida）
docs/报告-静态初版.md      加固前的静态可达面分析（对照用）
docs/签到类型全表.md       ★ 不同课程的不同签到方式：判定方法 + 每类必需参数
docs/工装与环境.md         从零搭出可复现环境（AVD / frida / dump / droidasc）
docs/学生高频操作接口.md   ★ 签到之外：视频任务点 enc、作业考试、直播、成绩、活动体系全景
docs/隐身与风控.md         ★ 伪装层 v2 + 风控层：六维伪装、判级表、闸门与熔断、反模式、A/B 验证
docs/视频任务点协议.md     ★ 视频任务点：enc 公式、203/rollbackPoint 回退、frida 抓真值、命令速查
docs/低暴露抓取.md         ★ 取真值时怎么把风控暴露面压到最低（三条路排序 + 尺度纪律 + 模拟器最低暴露清单）
docs/一键自动签到.md       ★ 教师侧取码 → 学生侧提交：四段流水线、模式速查、诊断产物、故障排查表
scripts/                   139 个脚本（含 cx_pipeline.py 一键流水线、device/ 真机抓包工具包、emulator/ 去模拟器化道具）：解壳、协议重放、自动签到、视频任务点、Frida hook、抓屏中继、伪装/风控/回归、加固对抗
userscript/                油猴脚本：在渲染二维码的电脑上直接解码上报
evidence/                  证据：类清单、字符串、findrefs 结果、反编译源码、dex 校验
```

## 边界

- 本仓库只处理**本人账号**的考勤事务，不含任何他人数据、不含账号密码、不含 cookie。
- 所有脚本的 `--uid` / `--cookie-file` 都由使用者自己提供；仓库内没有任何凭据。
- 报告中的判定接口（`signDetail` 等）为服务端公开接口，仅用于识别签到类型。
