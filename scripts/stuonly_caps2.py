#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""stuonly_caps2.py — 第二轮：位置 range 是否真校验 / 签到码错误锁阈值 / 学生端如何发现活动。"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cx_pipeline import TeacherSide
from stuonly_sign import Stu
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(os.path.dirname(HERE))
COURSE, CLASS = '269282723', '159926750'
STU_UID, TCH_UID = '[学生PUID]', '[教师PUID]'
sck = open('ck.txt', encoding='utf-8').read().strip()
tck = open('ck_tch.txt', encoding='utf-8').read().strip()
stu = Stu(cookie=sck, uid=STU_UID, course_id=COURSE, class_id=CLASS)
tch = TeacherSide(tck, TCH_UID, ua_mode='h5', max_writes_per_hour=60, min_interval=0, per_day=200)
R = {}
def P(k, v):
    R[k] = v; print('%-30s %s' % (k, v), flush=True)

# ============ A. 位置 range 是否真校验 ============
BJ = {'address': '北京市-东城区-东长安街 天安门', 'latitude': '39.9042', 'longitude': '116.4074', 'range': '500米'}
a1 = tch.create_sign(COURSE, CLASS, other_id='4', face='0', ifopen_address='1', time_long='1800000',
                     title='探针-位置(北京500米)A', location=BJ, verbose=False)
P('A_位置活动A', a1)
time.sleep(9)
a2 = tch.create_sign(COURSE, CLASS, other_id='4', face='0', ifopen_address='1', time_long='1800000',
                     title='探针-位置(北京500米)B', location=BJ, verbose=False)
P('B_位置活动B', a2)
CD = {'lat': '30.71142640936642', 'lon': '103.868397592583', 'addr': '成都市-温江区-惠民路211号 四川农业大学(成都校区)'}
P('A_用成都坐标签北京500米活动', str(stu.do_location(a1, CD['lat'], CD['lon'], CD['addr'])))
P('B_用(1.0,1.0)签北京500米活动', str(stu.do_location(a2, '1.0', '1.0', 'unknown')))

# ============ B. 签到码/手势 错误尝试的锁定阈值 ============
g = tch.create_sign(COURSE, CLASS, other_id='3', face='0', time_long='1800000',
                    title='探针-手势锁阈值', code='147258', verbose=False)
P('B_手势活动', g)
lock = None
for i in range(1, 41):
    rsp = stu.check_sign_code(g, '%06d' % (900000 + i))
    s = json.dumps(rsp, ensure_ascii=False)
    if i <= 3 or '次数' in s or '锁' in s or '频繁' in s or '验证码' in s or rsp.get('result') != 0:
        print('  第%02d 次 checkSignCode 错码 -> %s' % (i, s[:120]), flush=True)
    if '次数' in s or '锁' in s or '频繁' in s:
        lock = i; break
    time.sleep(0.25)
P('B_锁阈值', ('第 %d 次出现锁定提示' % lock) if lock else '40 次错码未出现锁定提示')
P('B_锁定后提交真码', str(stu.do_code(g, '147258')))

# ============ C. 学生端如何发现'有新签到' ============
EPS = [
    ('backclazzdata', 'https://mobilelearn.chaoxing.com/mycourse/backclazzdata?view=json&rss=1'),
    ('courseactivelist_s1', 'https://mobilelearn.chaoxing.com/ppt/activeAPI/courseactivelist?puid=%s&status=1&page=1&pageSize=50' % STU_UID),
    ('courseactivelist_s2', 'https://mobilelearn.chaoxing.com/ppt/activeAPI/courseactivelist?puid=%s&status=2&page=1&pageSize=50' % STU_UID),
    ('courseactivelist_nostatus', 'https://mobilelearn.chaoxing.com/ppt/activeAPI/courseactivelist?puid=%s&page=1&pageSize=50' % STU_UID),
    ('personalActiveLibraryV2', 'https://mobilelearn.chaoxing.com/ppt/activeAPI/personalActiveLibraryV2?puid=%s&page=1&pageSize=50' % STU_UID),
    ('classTaskCount', 'https://mobilelearn.chaoxing.com/ppt/activeAPI/classTaskCount?courseId=%s&classId=%s&uid=%s' % (COURSE, CLASS, STU_UID)),
    ('courseactivecount', 'https://mobilelearn.chaoxing.com/ppt/activeAPI/courseactivecount?courseId=%s&classId=%s&uid=%s' % (COURSE, CLASS, STU_UID)),
    ('taskactivelist', 'https://mobilelearn.chaoxing.com/ppt/activeAPI/taskactivelist?courseId=%s&classId=%s&uid=%s' % (COURSE, CLASS, STU_UID)),
    ('groupActiveCount', 'https://mobilelearn.chaoxing.com/ppt/groupAPI/getActiveCount?uid=%s' % STU_UID),
    ('phoneactivehistory', 'https://mobilelearn.chaoxing.com/phoneactivehistory/phonetimelist?courseId=%s&classId=%s&from=0' % (COURSE, CLASS)),
]
for tag, u in EPS:
    try:
        r = stu.s.get(u, timeout=25)
        b = (r.text or '').strip()
        n = b.count('activePrimaryId') + b.count('activeId')
        P('C_%-22s' % tag, 'HTTP %s len=%d activeHits=%d %s' % (r.status_code, len(b), n, b[:90].replace(chr(10), ' ')))
    except Exception as e:
        P('C_%-22s' % tag, 'ERR %r' % (e,))

# ============ D. 学生端直接按班级遍历活动（教师页不行的替代） ============
u = ('https://mobilelearn.chaoxing.com/v2/apis/sign/getLastSignForXd')
r = stu.s.get(u, timeout=20); P('D_getLastSignForXd', 'HTTP %s %s' % (r.status_code, (r.text or '')[:120]))

json.dump(R, open('out/stuonly_caps2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('-> out/stuonly_caps2.json')