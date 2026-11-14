#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
autosign.py - 学习通「绕过扫码」直接签到（无二维码 / 无相机 / 无在场）

思路（全部来自 6.7.8 解壳后的反编译 + 线上仍在用的教师/学生活动接口）:
  1) 列活动   https://mobilelearn.chaoxing.com/ppt/activeAPI/courseactivelist?puid=<uid>&status=1&page=1&pageSize=50
     兜底       https://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1
                https://mobilelearn.chaoxing.com/ppt/activeAPI/taskactivelist?courseId=<c>&classId=<cl>&uid=<uid>
  2) 取详情   https://mobilelearn.chaoxing.com/ppt/taskAPI/getActiveDataV2?activeId=<aid>
              https://mobilelearn.chaoxing.com/newsign/signDetail?activePrimaryId=<aid>&type=1
  3) 提交     https://mobilelearn.chaoxing.com/pptSign/stuSignajax?
                 activeId=<aid>&uid=<uid>&clientip=&useragent=&latitude=<lat>&longitude=<lon>
                 &appType=15&fid=<fid>&name=<name>[&address=<addr>]&ifTiJiao=1
              （位置签到才带 address 与 ifTiJiao=1；二维码签到服务端要求 enc，
               那种情况请用 qr_sign_remote.py 走二维码文本）

用法:
  # 单次：扫一遍所有进行中活动并签到
  python3 autosign.py --uid 12345678 --cookie-file cookies.txt --name 张三 --fid 12345

  # 常驻轮询（每 30 秒查一次）
  python3 autosign.py --uid 12345678 --cookie-file cookies.txt --name 张三 --fid 12345 \
      --loop --interval 30

  # 位置签到（伪造坐标）
  python3 autosign.py ... --lat 30.123456 --lon 120.123456 --address "XX大学XX楼"

  # 只列活动不提交
  python3 autosign.py --uid ... --cookie-file ... --list-only
"""
import argparse, json, os, sys, time, urllib.parse

try:
    import requests
except ImportError:
    sys.exit("need: pip install requests")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:                        # 伪装层：设备档案 / 完整头 / 拟人延迟 / 掩护流量
    from stealth_session import (make_session, Device, warmup, human_delay,
                                 explain as stealth_explain, HAVE_CFFI)
except Exception:           # 单文件运行也不至于挂
    make_session = warmup = human_delay = None
    Device = None
    HAVE_CFFI = False
    def stealth_explain(*a, **k):
        return ""

UA = ("Mozilla/5.0 (Linux; Android 13; SM-S9180 Build/TP1A.220624.014; wv) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/114.0.0.0 "
      "Mobile Safari/537.36 (schild:00000000) (device:SM-S9180) "
      "Language/zh-CN com.chaoxing.mobile/ChaoXingStudy_10946")

MOBILE = "https://mobilelearn.chaoxing.com/"
MOOC   = "https://mooc1-api.chaoxing.com/"


def load_cookie(arg_cookie, arg_file):
    if arg_cookie:
        return arg_cookie.strip()
    if not arg_file:
        return ""
    raw = open(arg_file, "r", encoding="utf-8", errors="ignore").read()
    if "\t" in raw and not raw.strip().startswith("{"):
        jar = []
        for line in raw.splitlines():
            if not line or line.startswith("#"):
                continue
            p = line.split("\t")
            if len(p) >= 7:
                jar.append("%s=%s" % (p[5], p[6]))
        if jar:
            return "; ".join(jar)
    return raw.strip()


def jget(r):
    try:
        return r.json()
    except ValueError:
        return None


def walk_active(obj, out):
    """活动列表 JSON 结构各版本不一，递归找带 activeId/id 的 dict"""
    if isinstance(obj, dict):
        aid = obj.get("activeId") or obj.get("id") or obj.get("activePrimaryId")
        if aid and (obj.get("signType") is not None or obj.get("otherId") is not None
                    or obj.get("name") is not None or obj.get("activeType") is not None):
            out.append(obj)
        for v in obj.values():
            walk_active(v, out)
    elif isinstance(obj, list):
        for v in obj:
            walk_active(v, out)


SIGN_TYPE_NAME = {0: "未知", 1: "拍照", 2: "普通", 3: "二维码", 5: "定位", 6: "手势", 7: "签到码"}


def active_type_from_detail(d):
    """signDetail 判定表（xxtSign 线上实证 + 本 APK otherId/ifPhoto 字段）:
        otherId==0 && ifPhoto==1 -> 1 拍照 | otherId==0 -> 2 普通 | otherId==2 -> 3 二维码
        otherId==3 -> 6 手势 | otherId==4 -> 5 定位 | otherId==5 -> 7 签到码 | 其它 -> 0"""
    if not isinstance(d, dict):
        return 0
    try:
        o = int(d.get("otherId", 0) or 0)
    except (TypeError, ValueError):
        o = 0
    try:
        ph = int(d.get("ifPhoto", 0) or 0)
    except (TypeError, ValueError):
        ph = 0
    if o == 0:
        return 1 if ph == 1 else 2
    return {2: 3, 3: 6, 4: 5, 5: 7}.get(o, 0)


def parse_backclazz(j, uid, urls):
    """mooc1 backclazzdata -> taskactivelist（只取 roletype==3 学生班），返回 (courseId,classId,cpi) 列表"""
    triples = []
    if not isinstance(j, dict):
        return triples
    for ch in (j.get("channelList") or []):
        content = ch.get("content") if isinstance(ch, dict) else None
        if not isinstance(content, dict):
            continue
        if str(content.get("roletype", 3)) != "3":
            continue
        class_id = content.get("id") or content.get("classId")
        cpi = content.get("cpi")
        course = content.get("course") or {}
        data = course.get("data") or []
        course_id = None
        if isinstance(data, list) and data and isinstance(data[0], dict):
            course_id = data[0].get("id") or data[0].get("courseId")
        if course_id and class_id:
            triples.append((course_id, class_id, cpi or ""))
            urls.append(MOBILE + "ppt/activeAPI/taskactivelist?courseId=%s&classId=%s&uid=%s&cpi=%s"
                        % (course_id, class_id, uid, cpi or ""))
    return triples


def list_activities(sess, uid, fid, dump=False):
    acts, idmap = [], {}
    urls = [
        MOBILE + "ppt/activeAPI/courseactivelist?puid=%s&status=1&page=1&pageSize=50" % uid,
    ]
    # 兜底：按课程/班级逐个查
    try:
        r = sess.get(MOOC + "mycourse/backclazzdata?view=json&rss=1", timeout=15)
        j = jget(r)
        if dump:
            print("[dump] backclazzdata:", json.dumps(j, ensure_ascii=False)[:1500])
        for t in parse_backclazz(j, uid, urls):
            if dump:
                print("[*] 学生班 courseId=%s classId=%s cpi=%s" % t)
    except Exception as e:
        print("[!] backclazzdata 失败（忽略）:", e)

    for u in urls:
        try:
            r = sess.get(u, timeout=15)
        except Exception as e:
            print("[!] GET 失败 %s : %s" % (u, e))
            continue
        j = jget(r)
        if dump:
            print("[dump] %s -> %s" % (u.split("?")[0], json.dumps(j, ensure_ascii=False)[:1200]))
        if j is None:
            print("[!] 非 JSON 响应 %s -> %s" % (u.split("?")[0], r.text[:200]))
            continue
        found = []
        # courseactivelist 真实结构: {"status":1,"message":"success","data":[...],"totalCount":n,...}
        if isinstance(j, dict) and isinstance(j.get("data"), list):
            found.extend([x for x in j["data"] if isinstance(x, dict)])
        if isinstance(j, dict) and isinstance(j.get("activeList"), list):
            found.extend([x for x in j["activeList"] if isinstance(x, dict)])
        walk_active(j, found)
        for a in found:
            aid = a.get("activeId") or a.get("id") or a.get("activePrimaryId")
            if aid and str(aid) not in idmap:
                idmap[str(aid)] = a
                acts.append(a)
    return acts


def detail(sess, aid, dump=False):
    out = {}
    for u in (MOBILE + "ppt/taskAPI/getActiveDataV2?activeId=%s" % aid,
              MOBILE + "newsign/signDetail?activePrimaryId=%s&type=1" % aid):
        try:
            r = sess.get(u, timeout=15)
            j = jget(r)
        except Exception as e:
            print("[!] detail 失败:", e)
            continue
        if dump:
            print("[dump] %s -> %s" % (u.split("?")[0], json.dumps(j, ensure_ascii=False)[:1200]))
        if isinstance(j, dict):
            out.update(j)
    return out


def submit(sess, aid, uid, fid, name, lat, lon, address="", dump=False, object_id=""):
    url = (MOBILE + "pptSign/stuSignajax?activeId=" + urllib.parse.quote(str(aid)) +
           "&uid=" + urllib.parse.quote(str(uid)) +
           "&clientip=&useragent=&latitude=" + str(lat) + "&longitude=" + str(lon) +
           "&appType=15&fid=" + urllib.parse.quote(str(fid)) +
           "&name=" + urllib.parse.quote(name))
    if object_id:
        url += "&objectId=" + urllib.parse.quote(str(object_id))
    if address:
        url += "&address=" + urllib.parse.quote(address) + "&ifTiJiao=1"
    print("[>] GET", url)
    r = sess.get(url, timeout=15)
    body = r.text.strip()
    print("[<]", r.status_code, body[:300])
    # 官方判定（xxtSign 线上实证）：响应体纯文本 "success"
    ok = (body.strip().lower() == "success") or ("签到成功" in body) or ('"status":1' in body)
    return ok, body


def main():
    ap = argparse.ArgumentParser(description="学习通绕过扫码直接签到")
    ap.add_argument("--uid", required=True, help="你的 puid")
    ap.add_argument("--cookie", help="Cookie 字符串")
    ap.add_argument("--cookie-file", help="Cookie 文件")
    ap.add_argument("--name", default="", help="真实姓名（提交必须）")
    ap.add_argument("--fid", default="0", help="学校/单位 fid，默认 0")
    ap.add_argument("--lat", default="-1")
    ap.add_argument("--lon", default="-1")
    ap.add_argument("--address", default="")
    ap.add_argument("--loop", action="store_true", help="常驻轮询")
    ap.add_argument("--interval", type=float, default=30.0)
    ap.add_argument("--object-id", default="", help="拍照签到用的云盘图片 objectId")
    ap.add_argument("--want-type", action="store_true", help="--list-only 时也拉详情判定签到类型")
    ap.add_argument("--list-only", action="store_true", help="只列活动不提交")
    ap.add_argument("--dump", action="store_true", help="打印原始 JSON（首次调试用）")
    ap.add_argument("--stealth", action="store_true",
                    help="伪装层：设备档案一致 + 完整头 + 拟人延迟 + 签到前掩护流量（推荐开）")
    ap.add_argument("--delay", default="3,30", help="拟人延迟区间 秒,秒（默认 3,30；0,0 关闭）")
    ap.add_argument("--phone-id", default=None, help="固定 phoneId（伪装层/通道 A 用）")
    ap.add_argument("--no-tls", action="store_true", help="关闭 curl_cffi 浏览器 TLS 指纹")
    a = ap.parse_args()

    ck = load_cookie(a.cookie, a.cookie_file)
    if a.stealth and make_session:
        dev = Device.load_or_create(uid=a.uid)
        if a.phone_id:
            dev.phone_id = a.phone_id
            dev.save()
        sess = make_session(cookie=ck, device=dev, uid=a.uid, tls=not a.no_tls)
        print("[stealth] phoneId=%s  TLS=%s" % (dev.phone_id, "curl_cffi" if getattr(sess, "_cx_tls", False) else "requests"))
        warmup(sess, uid=a.uid)
    else:
        sess = requests.Session()
        sess.headers.update({"User-Agent": UA, "Accept": "*/*",
                             "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "keep-alive"})
    if ck:
        sess.headers["Cookie"] = ck
    else:
        print("[!] 没给 cookie，几乎一定拿到未登录错误")

    done = set()
    while True:
        print("\n=== %s 轮询开始 ===" % time.strftime("%F %T"))
        acts = list_activities(sess, a.uid, a.fid, dump=a.dump)
        print("[*] 发现活动 %d 个" % len(acts))
        for ac in acts:
            aid = str(ac.get("activeId") or ac.get("id") or ac.get("activePrimaryId"))
            nm = ac.get("name") or ac.get("title") or ""
            st = ac.get("signType", ac.get("activeType"))
            print("  - activeId=%s signType=%s name=%s" % (aid, st, nm))
            d = detail(sess, aid, dump=a.dump) if (not a.list_only or a.want_type) else {}
            atype = active_type_from_detail(d) if d else 0
            if atype:
                print("    类型判定: %d %s" % (atype, SIGN_TYPE_NAME.get(atype, "?")))
                print("    详情:", json.dumps(d, ensure_ascii=False)[:300])
            if a.list_only or aid in done:
                continue
            if atype == 3:
                print("[!] activeId=%s 是二维码签到：服务端要 enc，本通道签不了 → "
                      "用 qr_sign_remote.py 塞二维码里解出的 enc" % aid)
                continue
            if atype == 1 and not a.object_id:
                print("[!] activeId=%s 是拍照签到：需 --object-id <云盘图 id>（或 frida 拿 oid）" % aid)
                continue
            if a.stealth and human_delay:
                try:
                    lo, hi = [float(x) for x in a.delay.split(",")]
                except Exception:
                    lo, hi = 3.0, 30.0
                if hi > 0:
                    human_delay(lo, hi)
            ok, body = submit(sess, aid, a.uid, a.fid, a.name, a.lat, a.lon,
                              a.address, a.dump, object_id=(a.object_id if atype == 1 else ""))
            if ok:
                print("[+] activeId=%s 签到成功" % aid)
                done.add(aid)
            else:
                print("[-] activeId=%s 未成功（二维码/拍照类需走 qr_sign_remote.py）" % aid)
        if not a.loop:
            return
        time.sleep(a.interval)


if __name__ == "__main__":
    main()
