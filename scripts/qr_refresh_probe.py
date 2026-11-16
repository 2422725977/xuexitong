# -*- coding: utf-8 -*-
"""qr_refresh_probe.py — 5 秒刷新二维码：enc 是否轮换 / 旧 enc 是否还能签成。"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cx_pipeline import TeacherSide
from stuonly_sign import Stu
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(os.path.dirname(HERE))
COURSE, CLASS, STU_UID, TCH_UID = '269282723', '159926750', '493228247', '401537379'
stu = Stu(cookie=open('ck.txt', encoding='utf-8').read().strip(), uid=STU_UID, course_id=COURSE, class_id=CLASS)
tch = TeacherSide(open('ck_tch.txt', encoding='utf-8').read().strip(), TCH_UID, ua_mode='h5',
                  max_writes_per_hour=60, min_interval=0, per_day=200)
aid = tch.create_sign(COURSE, CLASS, other_id='2', face='0', time_long='1800000',
                      title='探针-二维码5秒刷新', if_refresh_ewm='1', ewm_refresh_time='5', verbose=False)
print('aid =', aid, flush=True)
if not aid:
    sys.exit(1)
encs = []
for i in range(7):
    q = tch.refresh_qrcode(aid) or {}
    e = q.get('enc', '')
    encs.append(e)
    print('  第%d次 refreshQRCode (t+%2ds) enc=%s c=%s refresh=%s' % (i + 1, i * 6, e[:24], q.get('c'), q.get('refresh')), flush=True)
    if i < 6:
        time.sleep(6)
uniq = list(dict.fromkeys(encs))
print('enc 去重后 %d 个: %s' % (len(uniq), [u[:16] for u in uniq]), flush=True)
print('--- 用最早的 enc（已过 %d 秒 ≈ %d 个刷新周期）提交 ---' % (36, 36 // 5), flush=True)
print('最早 enc 提交 ->', stu.do_qr(aid, encs[0]), flush=True)
print('（若上面不是 success，再用最新 enc）最新 enc 提交 ->', stu.do_qr(aid, encs[-1]), flush=True)
json.dump({'aid': aid, 'encs': encs}, open('out/qr_refresh_probe.json', 'w'), ensure_ascii=False, indent=1)