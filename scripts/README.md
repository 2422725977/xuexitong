# scripts 索引

共 72 个脚本。带 ★ 的是日常主用；其余是解壳/取证过程中留下的工具，保留以便复现。

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
| `selftest.py` | ★ 全量回归测试 43 项（判级器 + 闸门熔断 + 调用方熔断 + 审计脱敏），不联网 |
| `autosign.py` / `qr_sign_remote.py` | 已接入熔断：命中风控打印 [STOP]/[WAIT] 并停手；支持 --max-writes-per-hour / --min-interval / --quiet-hours |
| `tch_qr_probe.py` | ★ 教师侧二维码探针：用教师登录态反复拉教师端签到页，抽取当前 `widget/sign/e?id&c&enc`、候选 enc/signCode 与跨轮变化（拿到即可不再依赖真人扫码） |
| `cx_login.py` | ★ 网页端登录（手机号+密码，AES(transferKey) 提交 passport2/fanyalogin）→ 导出 ck.txt / ck.json（学生或教师通用） |
| `cx_tch_login.py` | ★ 教师端短信验证码登录（三模式 send/login/auto，POST passport2/fanyaloginbycode）→ 导出 ck_tch.txt |
| `cx_pipeline.py` | ★ 一键流水线：教师侧 refreshQRCode 权威取码 → 学生侧提交；`--mode create` 可先新建**不扫脸**签到（`POST /pptSign/newTaskSign`，`--create-type/--no-face/--sign-address/--time-long/--auto-create`）；位置类自动带 `location`+`locationResult`（`--geo/--lat/--lon/--address`）；含闸门识别（checkFace_/validate_）、白名单 guard_scope、诊断落盘 |
| `flip_attend_status.py` | ★ 教师侧状态改写：把 **迟到(9)** 改回 **已签(1)**（或 5 缺勤 / 10 早退 / 7、8、12 请假 / 2 代签 / 39331-39334 实习实训免修参赛）。自动并四条名单查询定位 attendId（迟到行在未签名单里 status=9），`GET /pptSign/updateSignStatus` 返回 success，改完自动复核；不受活动是否结束影响 |
| `ewm_watch.py` | 轮询 signDetail 监视 isOver/isBegins/status/signCode/attendNum 变化，可在窗口打开瞬间自动提交（验证旧 enc 是否可用） |
| `probe_reporturl_entry.py` | 无 cookie 探测两跳入口（knowledge/cards → ananas/job）的鉴权行为，用于判定 reportUrl 是否必须登录态 |
