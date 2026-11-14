# 证据清单

| 文件 | 内容 | 体量 |
|---|---|---|
| `classes_readable.txt` | 解壳后从 11 个 dex 提取的类描述符（97,576 条记录 / 约 48,788 唯一） | 2.3 MB |
| `dumped_all_classes.txt` | `droidasc listclass` 全量类名（83,944 类） | 3.5 MB |
| `dumped_strings.txt.gz` | 全量字符串池（388,486 唯一串） | 2.4 MB gz |
| `classes_strings.txt.gz` | 加固载荷中的可打印串（570,502 条，未解壳时的静态可达面） | 4.7 MB gz |
| `sign_evidence.txt` | 签到模块字符串证据（关键词命中 + 端点 + 文案） | 24 KB |
| `sign_module_classes.txt` | 签到相关类清单（mobile/sign、office punch、beacon、attendance） | 48 KB |
| `strings_signish.txt` / `paths_signish.txt` | 含 sign/签到/二维码 的字符串与路径 | 60 KB |
| `api_atlas_core.txt` / `api_paths.txt` / `urls_readable.txt` | 端点图谱（含 mobilelearn / fanyappfy 全域签到接口） | 130 KB |
| `chaoxing_hostpaths.txt` / `cx_descriptors.txt` | com.chaoxing.* 主机路径与类描述符 | 92 KB |
| `cls_sign.txt` / `cls_punch.txt` / `sign_windows.txt` | 签到类 / 打卡类 / 签到窗口候选 | 60 KB |
| `manifest.xml` | 完整 AndroidManifest（854 activity / 69 service / 19 provider / 22 receiver） | 196 KB |
| `refs/` | droidasc 引用点查询结果（signId / rcode / SIGNIN: / studentsign / ctype=stusign / activePrimaryId / `ifTiJiao` / 定位类 / beacon / 蓝牙 / 人脸 verify …） | — |
| `decompiled/` | 关键类反编译源码：SignInfoActivity(`src`)、人脸栈(`src3`,`src4`,`src9_faceverify`)、H5 桥(`src5` 引用点) | — |
| `logs/` | 解壳过程中的门禁/探针日志 | 12 KB |
| `dexes.sha256` | 11 个解壳 dex 的 sha256 校验 | 1 KB |

未入库（体积原因）：原 APK（263 MB）、解壳 dex（121 MB）、`unpacked.apk`（116 MB）、内存快照（1.9 GB）。
