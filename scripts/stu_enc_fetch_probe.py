# -*- coding: utf-8 -*-
"""stu_enc_fetch_probe.py — 学生 cookie 能否拿到二维码活动的「当前 enc」（5秒刷新场景的关键）。"""
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
HEX = re.compile(r'[0-9A-Fa-f]{16,64}')
qa = tch.create_sign(COURSE, CLASS, other_id='2', face='0', time_long='1800000', title='探针-学生实时取码',
                     if_refresh_ewm='1', ewm_refresh_time='5', verbose=False)
cur = (tch.refresh_qrcode(qa) or {}).get('enc', '')
print('fixture aid=%s 当前真值 enc=%s' % (qa, cur), flush=True)
CANDS = [
 ('v2/apis/sign/refreshQRCode', '%s/v2/apis/sign/refreshQRCode?activeId=%s&time=%d' % (MOBILE, qa, int(time.time()*1000))),
 ('pptSign/refreshQRCode', '%s/pptSign/refreshQRCode?activeId=%s&appType=15' % (MOBILE, qa)),
 ('newsign/refreshQRCode', '%s/newsign/refreshQRCode?activePrimaryId=%s' % (MOBILE, qa)),
 ('v2/apis/sign/getSignCode', '%s/v2/apis/sign/getSignCode?activeId=%s' % (MOBILE, qa)),
 ('pcStuSignController/getSignCode', '%s/widget/sign/pcStuSignController/getSignCode?activeId=%s' % (MOBILE, qa)),
 ('pcTeaSignController/getSignCode', '%s/widget/sign/pcTeaSignController/getSignCode?activeId=%s' % (MOBILE, qa)),
 ('widget/sign/getEwm', '%s/widget/sign/getEwm?activeId=%s' % (MOBILE, qa)),
 ('widget/sign/e(空enc)', '%s/widget/sign/e?id=%s&c=0&enc=&DB_STRATEGY=PRIMARY_KEY&STRATEGY_PARA=id' % (MOBILE, qa)),
 ('widget/sign/e(真enc)', '%s/widget/sign/e?id=%s&c=0&enc=%s&DB_STRATEGY=PRIMARY_KEY&STRATEGY_PARA=id' % (MOBILE, qa, cur)),
 ('pptSign/gotasksign', '%s/pptSign/gotasksign?courseId=%s&classId=%s&uid=%s&activePrimaryId=%s&appType=15' % (MOBILE, COURSE, CLASS, STU, qa)),
 ('pptSign/preSign', '%s/pptSign/preSign?activePrimaryId=%s&sys=1&general=&ls=1&appType=15&classId=%s&uid=%s&source=1' % (MOBILE, qa, CLASS, STU)),
]
for tag, u in CANDS:
    try:
        r = stu.s.get(u, timeout=25)
        b = (r.text or '').strip()
        hs = [h for h in dict.fromkeys(HEX.findall(b)) if h != cur][:3]
        got = cur[:14] in b
        print('  %-32s HTTP %s len=%5d 含当前enc=%s 其它hex=%s | %s' % (tag, r.status_code, len(b), got, hs, b.replace(chr(10),' ')[:90]), flush=True)
    except Exception as e:
        print('  %-32s ERR %r' % (tag, e), flush=True)
print('aid %s (供清场)' % qa, flush=True)