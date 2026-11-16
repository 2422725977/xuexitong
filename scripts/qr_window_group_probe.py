# -*- coding: utf-8 -*-
"""qr_window_group_probe.py — ① 5秒刷新二维码的 enc 有效窗口 ② 学生端能否实时取 enc ③ 班群消息接口能否读到签到活动。"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cx_pipeline import TeacherSide
from stuonly_sign import Stu
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(os.path.dirname(HERE))
MOBILE = 'https://mobilelearn.chaoxing.com'
COURSE, CLASS, STU, TCH = '269282723', '159926750', '[学生PUID]', '[教师PUID]'
stu = Stu(cookie=open('ck.txt', encoding='utf-8').read().strip(), uid=STU, course_id=COURSE, class_id=CLASS)
tch = TeacherSide(open('ck_tch.txt', encoding='utf-8').read().strip(), TCH, ua_mode='h5',
                  max_writes_per_hour=60, min_interval=0, per_day=200)
HEX = re.compile(r'\b([0-9A-Fa-f]{16,64})\b')
def mk(tag):
    a = tch.create_sign(COURSE, CLASS, other_id='2', face='0', time_long='1800000', title='探针-'+tag,
                        if_refresh_ewm='1', ewm_refresh_time='5', verbose=False)
    print('[fixture]', tag, a, flush=True)
    return a

# ---------- ① enc 有效窗口：t0 取 enc，等 W 秒提交 ----------
for W in (8, 12, 22):
    a = mk('窗口%d' % W)
    e0 = (tch.refresh_qrcode(a) or {}).get('enc', '')
    time.sleep(W)
    e1 = (tch.refresh_qrcode(a) or {}).get('enc', '')
    res = stu.do_qr(a, e0)
    print('  等待 %2ds 后用 t0 的 enc 提交 -> %s   （t0=%s, 当前=%s）' % (W, res[1][:40], e0[:12], e1[:12]), flush=True)
    time.sleep(1)

# ---------- ② 学生 cookie 能否拿到实时 enc ----------
qa = mk('学生取码')
cur = (tch.refresh_qrcode(qa) or {}).get('enc', '')
print('  当前真实 enc =', cur[:20], flush=True)
CANDS = [
 ('v2/apis/sign/refreshQRCode', '%s/v2/apis/sign/refreshQRCode?activeId=%s&time=%d' % (MOBILE, qa, int(time.time()*1000))),
 ('pptSign/refreshQRCode', '%s/pptSign/refreshQRCode?activeId=%s&appType=15' % (MOBILE, qa)),
 ('newsign/refreshQRCode', '%s/newsign/refreshQRCode?activePrimaryId=%s' % (MOBILE, qa)),
 ('v2/apis/sign/getSignCode', '%s/v2/apis/sign/getSignCode?activeId=%s' % (MOBILE, qa)),
 ('pcStuSignController/getSignCode', '%s/widget/sign/pcStuSignController/getSignCode?activeId=%s' % (MOBILE, qa)),
 ('widget/sign/getEwm', '%s/widget/sign/getEwm?activeId=%s' % (MOBILE, qa)),
 ('widget/sign/e(无enc)', '%s/widget/sign/e?id=%s&c=0&enc=&DB_STRATEGY=PRIMARY_KEY&STRATEGY_PARA=id' % (MOBILE, qa)),
 ('widget/sign/e(真enc)', '%s/widget/sign/e?id=%s&c=0&enc=%s&DB_STRATEGY=PRIMARY_KEY&STRATEGY_PARA=id' % (MOBILE, qa, cur)),
 ('pptSign/gotasksign', '%s/pptSign/gotasksign?courseId=%s&classId=%s&uid=%s&activePrimaryId=%s&appType=15' % (MOBILE, COURSE, CLASS, STU, qa)),
]
for tag, u in CANDS:
    try:
        r = stu.s.get(u, timeout=25)
        b = (r.text or '').strip()
        list(dict.fromkeys(HEX.findall(b)))[:3]
        print('  %-30s HTTP %s len=%4d hex=%s | %s' % (tag, r.status_code, len(b), hit, b.replace(chr(10),' ')[:110]), flush=True)
    except Exception as e:
        print('  %-30s ERR %r' % (tag, e), flush=True)

# ---------- ③ 班群消息接口（学生 cookie） ----------
MSGC = [
 ('apis/message/unreadCount', '%s/apis/message/unreadCount?uid=%s' % (MOBILE, STU)),
 ('apis/message/messageList', '%s/apis/message/messageList?uid=%s&page=1&size=20' % (MOBILE, STU)),
 ('apis/message/messageList2', '%s/apis/message/messageList?uid=%s&pageNo=1&pageSize=20&status=0' % (MOBILE, STU)),
 ('apis/message/menus', '%s/apis/message/menus?uid=%s' % (MOBILE, STU)),
 ('ppt/groupAPI/groupList', '%s/ppt/groupAPI/groupList?uid=%s' % (MOBILE, STU)),
 ('ppt/groupAPI/getGroupList', '%s/ppt/groupAPI/getGroupList?uid=%s' % (MOBILE, STU)),
 ('groupweb chatlist', 'https://groupweb.chaoxing.com/api/chat/list?uid=%s' % STU),
 ('mobilelearn chat msg', '%s/chat/message/list?uid=%s&chatId=330606364917761' % (MOBILE, STU)),
 ('v2/apis/chat/list', '%s/v2/apis/chat/list?uid=%s' % (MOBILE, STU)),
]
for tag, u in MSGC:
    try:
        r = stu.s.get(u, timeout=25)
        b = (r.text or '').strip().replace(chr(10), ' ')
        print('  %-26s HTTP %s len=%4d %s' % (tag, r.status_code, len(b), b[:150]), flush=True)
    except Exception as e:
        print('  %-26s ERR %r' % (tag, e), flush=True)
print('fixture aids: 窗口8/12/22 + 学生取码，见上；结束前用 endSign 清场', flush=True)