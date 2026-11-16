# -*- coding: utf-8 -*-
"""qr_static_probe.py — 对照实验：关闭「二维码刷新」(ifRefreshEwm=0) 时 enc 是否固定、旧 enc 是否仍可签。"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cx_pipeline import TeacherSide
from stuonly_sign import Stu
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(os.path.dirname(HERE))
COURSE, CLASS, STU, TCH = '269282723', '159926750', '493228247', '401537379'
stu = Stu(cookie=open('ck.txt', encoding='utf-8').read().strip(), uid=STU, course_id=COURSE, class_id=CLASS)
tch = TeacherSide(open('ck_tch.txt', encoding='utf-8').read().strip(), TCH, ua_mode='h5',
                  max_writes_per_hour=60, min_interval=0, per_day=200)
a = tch.create_sign(COURSE, CLASS, other_id='2', face='0', time_long='1800000', title='探针-二维码不刷新',
                    if_refresh_ewm='0', ewm_refresh_time='0', verbose=False)
e0 = (tch.refresh_qrcode(a) or {}).get('enc', '')
print('fixture aid=%s ifRefreshEwm=0  t0 enc=%s' % (a, e0[:20]), flush=True)
time.sleep(10)
e1 = (tch.refresh_qrcode(a) or {}).get('enc', '')
time.sleep(5)
e2 = (tch.refresh_qrcode(a) or {}).get('enc', '')
print('  +10s enc=%s  相同=%s' % (e1[:20], e1 == e0), flush=True)
print('  +15s enc=%s  相同=%s' % (e2[:20], e2 == e1), flush=True)
time.sleep(20)
print('  +35s 用 t0 的 enc 提交 ->', stu.do_qr(a, e0), flush=True)
print('  aid %s 供清场' % a, flush=True)