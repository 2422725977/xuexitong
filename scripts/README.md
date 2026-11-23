# scripts 索引

共 143 个脚本（含 device/、emulator/ 子目录）。带 ★ 的是日常主用；其余是解壳/取证过程中留下的工具，保留以便复现。

| 脚本 | 说明 |
|---|---|
| `anti_anti.js` | 反反调试（ptrace 检测对抗） |
| `api_atlas.py` | 端点图谱（全 App URL 归类） |
| `autosign.py` | ★ 免二维码直签 + 轮询（列表→类型判定→按类型提交） |
| `cx_pipeline.py` | ★ 一键流水线：教师侧取码 → 学生侧提交（四段自动 + **refreshQRCode 权威取码** + 双路抽取 + 候选评分 + 人脸/captcha 闸门识别 + 白名单 guard_scope + 自动重登 + 落盘诊断） |
| `dex_strings.py` | 从解壳 dex 提取全量字符串池 |
| `extract_dex.py` | 从内存快照按 dex magic+校验切出真 dex |
| `frida_face_puppet.js` | Frida：伪造活体状态位 + 注入指定人脸图 |
| `frida_sign_hook.js` | ★ Frida：hook SignInfoActivity/enc/扫码分发/volley/cookie 导出/人脸桥 |
| `frida_video_hook.js` | ★ Frida：视频上报抓真值（enc 明文/密文对、完整 reportUrl、203 回退判定） |
| `mk_apk.py` | 把解壳 dex 重新打成可被静态工具消费的 apk |
| `native_unpack_probe.py` | native 加固探针（VMP 标记/加密符号表） |
| `qr_relay.py` | ★ 自动看屏中继（adb/macOS 截屏/目录）→ 解码 → 直签或转发 |
| `qr_sign_remote.py` | ★ 四通道签到：单次/--watch 目录/--serve 中继/--stdin |
| `qr_watch.py` | ★ 扫码签到抢签器：folder/screen/adb/camera/http/text 六源 → 解码 → 立即提交（--stop-on-success/--append-log） |
| `qr_screen_sim.py` | ★ 教师大屏二维码模拟器：轮询 refreshQRCode 渲染真实二维码 PNG/网页，复现 5 秒动态码 |
| `sign_evidence.py` | 签到模块字符串/类/端点证据汇总 |
| `video_task.py` | ★ 视频任务点：干跑/按真实节奏上报/--verify-capture/--selftest，内接伪装与风控 |
| `snap3.sh` | 冻结进程后直读 /proc/<pid>/mem 全 rw 段 |
| `api_table.py` | Dump the mobilelearn API template table + hunt the student sign-in submit endpoint. |
| `dbg_magic.py` | — |
| `dbg_magic2.py` | — |
| `dbg_mem.sh` | — |
| `dex_layout.py` | Layout + entropy map of classes.dex (stub vs payload) and asset blob census. |
| `dump_and_mine.sh` | dump_and_mine.sh — 对 frida-dexdump 产物做批量分析（droidasc 链路） |
| `dump_bangcle.py` | — |
| `endpoints.py` | Whole-APK endpoint census: chaoxing hosts and API paths in every readable entry. |
| `fdscan.sh` | — |
| `fsd.sh` | ★ 低暴露启停 frida-server（非默认端口 39042、听 127.0.0.1、抓完自动清痕迹） |
| `gate_children.py` | — |
| `getclass_batch2.sh` | — |
| `getclass_batch3.sh` | — |
| `h5_schedule.py` | Inspect the unsealed H5 schedule/attendance bundle inside assets. |
| `h5_schedule2.py` | — |
| `hunt_signin.py` | Hunt the 签到/attendance surface across every readable entry of the APK. |
| `killchild.sh` | — |
| `maps.sh` | — |
| `masquerade.js` | masquerade.js v2 - hide emulator/frida fingerprints for Bangcle DexHelper + full crash diagnostics. |
| `mine_strings.py` | Mine the readable string surface inside the sealed classes.dex; build the 学习通/签到 class + API map. |
| `params.py` | Recover sign-request parameter constants near the sign code region. |
| `patch_odm.sh` | — |
| `patch_props.sh` | — |
| `patch_props2.sh` | — |
| `patch_props3.sh` | — |
| `payload_map.py` | Fine-grained map of the sealed payload inside classes.dex + zlib/ELF magic census. |
| `probe_env.js` | — |
| `probe_env2.js` | — |
| `prop_fix.js` | — |
| `recon_dex.py` | chaoxing apk recon: dex headers, entry census, packer markers. |
| `refs_batch.sh` | — |
| `refs_batch2.sh` | — |
| `refs_batch3.sh` | — |
| `refs_batch4.sh` | — |
| `refs_batch5.sh` | — |
| `refs_batch6.sh` | — |
| `refs_batch7.sh` | — |
| `refs_batch8.sh` | — |
| `scan_dex.py` | — |
| `scan_hdr.py` | — |
| `scan_magic2.py` | — |
| `scan_strings.py` | — |
| `sign_client.py` | 学习通 6.7.8 扫码签到复现客户端（占位符版）。 |
| `sign_window.py` | Window dump around the sign-in endpoints: recover nearby string-pool constants. |
| `snap.sh` | usage: snap.sh <delay_ms> <mode: dry/dump> <outdir> |
| `snap2.sh` | — |
| `strings_payload.py` | Extract the readable class/string surface from the sealed classes.dex, focused on the sign module. |
| `unseal_probe.py` | Attempt static recovery inside the sealed payload: embedded zips, zlib/deflate streams, single-byte-xor dex. |
| `stealth_session.py` | ★ 伪装层 v2 + 风控层核心：六维伪装（身份/指纹/头/时序/流量/审计）+ 判级闸门熔断（其他脚本加 --stealth 即可用） |
| `risk_guard.py` | ★ 风控层 CLI：判级语料回归 18 条 / 响应判级 / 模拟处置 / 审计监视 / 状态重置 |
| `risk_center.py` | ★★ 反封号策略层：R1 只读先行 / R2 单调进度 / R3 目标上限 / R4 双配额 / R5+R6 节奏 / R7 三档熔断 / R8 全审计 / R9 不伪造埋点 / R10 失败退避；按动作分档（sign、sign_probe、qr_sign、tch_write、video_report、work_*、exam），CLI --status/--explain/--plan/--selftest(35 项)/--reset/--optin |
| `risk_integration_test.py` | ★ 接线回归 17 项（离线假 session）：stu_guard 的 R1/计数/R3/HALT/审计、video_task 的 allow→observe→rollback→R2、cx_pipeline StudentSide 的 R1 自愈→配额→R3→HALT |
| `cdp_login_capture.py` | 电脑路线取 mooc 会话：专用 Chrome 配置目录 + CDP 明文 cookie（绕过 v10 加密与钥匙串），登录成功自动落盘 mooc.txt；--launch-only / --watch / --once / --selftest |
| `browser_cookie_lift.py` | 直读本机 Chromium cookie 库（Chrome/Edge/Brave），v10 值用 PBKDF2+AES 解密（需要钥匙串里的 Safe Storage 密钥；本机缺失故当前不可用） |
| `mooc_cookie_pull.py` | 手机路线拉 App WebView cookie 库（adb shell su -c 读 sqlite → Netscape），备用 |
| `brush_course.py` | ★ 刷课总管：backclazzdata → studentcourse 取章节 → cards → 任务点递归上报，复用 video_task 与 risk_center；--list-courses / --dry-run / --only-unfinished / --pace real|jitter |
| `selftest.py` | ★ 全量回归测试 43 项（判级器 + 闸门熔断 + 调用方熔断 + 审计脱敏），不联网 |
| `autosign.py` / `qr_sign_remote.py` | 已接入熔断：命中风控打印 [STOP]/[WAIT] 并停手；支持 --max-writes-per-hour / --min-interval / --quiet-hours |
| `tch_qr_probe.py` | ★ 教师侧二维码探针：用教师登录态反复拉教师端签到页，抽取当前 `widget/sign/e?id&c&enc`、候选 enc/signCode 与跨轮变化（拿到即可不再依赖真人扫码） |
| `cx_login.py` | ★ 网页端登录（手机号+密码，AES(transferKey) 提交 passport2/fanyalogin）→ 导出 ck.txt / ck.json（学生或教师通用） |
| `cx_tch_login.py` | ★ 教师端短信验证码登录（三模式 send/login/auto，POST passport2/fanyaloginbycode）→ 导出 ck_tch.txt |
| `cx_pipeline.py` | ★ 一键流水线：教师侧 refreshQRCode 权威取码 → 学生侧提交；`--mode create` 可先新建**不扫脸**签到（`POST /pptSign/newTaskSign`，`--create-type/--no-face/--sign-address/--time-long/--auto-create`）；位置类自动带 `location`+`locationResult`（`--geo/--lat/--lon/--address`）；含闸门识别（checkFace_/validate_）、白名单 guard_scope、诊断落盘 |
| `flip_attend_status.py` | ★ 教师侧状态改写：把 **迟到(9)** 改回 **已签(1)**（或 5 缺勤 / 10 早退 / 7、8、12 请假 / 2 代签 / 39331-39334 实习实训免修参赛）。自动并四条名单查询定位 attendId（迟到行在未签名单里 status=9），`GET /pptSign/updateSignStatus` 返回 success，改完自动复核；不受活动是否结束影响 |
| `ewm_watch.py` | 轮询 signDetail 监视 isOver/isBegins/status/signCode/attendNum 变化，可在窗口打开瞬间自动提交（验证旧 enc 是否可用） |
| `probe_reporturl_entry.py` | 无 cookie 探测两跳入口（knowledge/cards → ananas/job）的鉴权行为，用于判定 reportUrl 是否必须登录态 |

- ★ scripts/stuonly_sign.py —— **只有学生 cookie 时**的全类型签到（普通/手势/签到码/位置/二维码，自动判型 + 本地二维码图片解码）
 ★ scripts/stu_guard.py —— **只有学生 cookie 的常驻守护**：activelist 自动发现新签到 → 普通直接签 / 位置用「距离预言机」爬坡自动签，二维码/签到码/手势自动归「需人工」


## 拍照签到专项（2026-11-17 新增，结果见 docs/拍照签到-PCR007-专项.md）

| 脚本 | 说明 |
|---|---|
| device/（目录） | ★ 真机抓包工具包：android_check.sh 环境自检 / mitm_capture.sh USB 代理抓包 / webview_console.js chrome://inspect 取证 / frida_android_capture.js 真机 frida 抓请求 / CAPTURE-ANDROID.md 作战清单 |
| photo_sign_matrix.py … photo_sign_matrix8.py | 拍照提交矩阵 v1–v8：UA / deviceCode / photoResult / fid / preSign / ext / 真名 / 外层对象形状 / 四大外部配方逐字复刻 |
| photo_sign_matrix16.py、photo_sign_matrix17.py | 上传上下文矩阵（上传带 activeId / courseId+classId / CRC 预检 / Referer）；端点存在性探测 + 只保存活动启动 + validate 空值 |
| photo_probe2.py、photo_probe_v9.py … photo_probe_v15.py | 闸门顺序探针：不带 objectId / 不带 cookie / 教师身份 / 伪造 aid / 普通活动对照 / 群聊路径 |
| photo_activity_forensics.py、photo_activity_config.py | 活动侧取证：signDetail 全字段、pptActiveInfo 全字段、教师页内容 |
| probe_upload.sh | 上传通道探测（带/不带 _from 与 _token） |
| hide_env.js | ★ 梆梆 SecNeo 伪装层：属性改写 + /proc 读缓冲替换 + 路径屏蔽 + strstr 屏蔽（模拟器实测把存活从 0.0s 拉到 12.7s） |
| run_hide.py、run_frida.py | spawn 驱动（run_frida 支持多脚本注入 + adb forward 连 remote device） |
| frida_probe2.js、frida_min.js、frida_crash_trace.js | 崩溃现场诊断（Process.setExceptionHandler + /proc 路径重定向 + libDexHelper 采样） |
| frida_app_probe.js/.py、frida_app_scan_sim.js、frida_attach_probe.py | App 运行态探针 |
| emu_sanitize.sh + emulator/ | 去模拟器化道具：build.prop 伪装（system/vendor/odm/product）、假 /proc/version 与 /proc/cpuinfo、su 隐藏、挂载 |

- 拍照/人脸的完整结论与全部变体矩阵见 docs/拍照签到-PCR007-专项.md；真机取证流程见 docs/真机抓包作战清单.md。


## 只有学生端时的能力边界探针（2026-11-17，见报告第 23 章）

| 脚本 | 说明 |
|---|---|
| stuonly_caps.py | 学生 cookie 调 refreshQRCode（暂无权限）/ preSign 页信息面 / 位置真值面 / 五类提交 |
| stuonly_caps2.py | 位置 range 真校验（成都↔北京 1525491.0 米）+ checkSignCode 锁阈值（第 6 次锁 1 小时）+ 10 个活动列表接口 |
| stuonly_caps3.py | 列表接口变体（fid/cpi/type/role/App UA）复测 |
| stuonly_caps4.py | 学生页面（newsign/preSign、pptSign/preSign、widget/sign/e）能否带出坐标 |
| stuonly_caps5.py | signDetail 全字段（62 个，无 location/address） |
| stuonly_caps6/7.py | getActiveDataV2 等活动内容接口（只有元数据，无坐标） |


## 二维码刷新模式 / 群消息 探针（2026-11-17，见报告第 24 章）

| 脚本 | 说明 |
|---|---|
| qr_refresh_probe.py | 5 秒刷新二维码：enc 是否轮换（6 个/36 秒）+ 旧 enc 提交结果 |
| qr_static_probe.py | 对照：ifRefreshEwm=0 时 enc 固定、35 秒后旧 enc 仍 success |
| qr_window_group_probe.py | enc 有效窗口（8/12/22 秒全部失效）+ 10 个群聊/消息接口尝试 |
| stu_enc_fetch_probe.py | 学生 cookie 抢实时 enc 的 11 条候选路径（全否） |
 stu_remote_discover.py | 学生 cookie 自己发现活动：/v2/apis/active/student/activelist（一次 70+ 条，新活动 1 秒入列） |
 stu_oracle_walk.py / stu_remote_location.py | 位置签到纯远程：地址文本 → 起点，用「距离预言机」中心 + 两个梯度探针爬坡 |
 stu_trilaterate.py | 三边几何解析解（失败路线：探针点距目标 35-40km 时病态，反解偏 17.9km） |
 stu_lock_test.py | 签到码/手势锁定阈值：第 6 次错码锁 1 小时（按账号+活动，换 session 无效） |
 stu_read_secret.py / stu_read_secret2.py | 学生 preSign 页能否带出码值/坐标（只有变量名，无真值） |
 qr_construct_probe.py | 二维码 enc 能否构造：8 次采样 32 位 hex 每 5.3 秒换，md5 试算全否 |
| im_history_probe*.py | im.chaoxing.com/apis/message/getHistory 真实参数（803003）+ 变体 |
| dump_sign_e_page.py | widget/sign/e 大屏页真实返回（1165 B「链接已失效」提示页） |


## 扫码签到抢签（2026-11-23 真机实测，见报告第 25 章）

| 脚本 | 说明 |
|---|---|
| qr_watch.py | ★ 六源抢签：--source folder/screen/adb/camera/http/text，内容哈希去重、成功即停、--append-log JSONL |
| qr_screen_sim.py | ★ 大屏模拟器：--aid 轮询 refreshQRCode → 渲染二维码 PNG（--serve PORT 起网页大屏） |
| qr_sign_remote.py | 老牌四通道（含中继 HTTP 服务，适合让在场同学把截图 POST 过来） |
| qr_relay.py | 看屏中继（adb 截屏 / macOS 截屏 / 目录）→ 解码 → 直签或转发 |

实测：动态码（5 秒轮换）截图约 10 秒内仍可签、>14 秒必废；静态码 25 秒后仍 success。端到端两次均「第 1 次提交即 success」（folder 源 13:30:30、真机 adb 截屏源 13:38:05）。
