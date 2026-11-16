#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""stuonly_caps.py — 实战只有学生端 cookie 时，签到相关能力边界实测探针。
只用学生 cookie 发起所有'取信息 + 签名'动作；教师 cookie 仅用于创建 fixture 活动。
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cx_pipeline import TeacherSide
from stuonly_sign import Stu

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(HERE))  # chaoxing/
COURSE, CLASS = '269282723', '159926750'
STU_UID, TCH_UID = '[学生PUID]', '[教师PUID]'
sck = open('ck.txt', encoding='utf-8').read().strip()
tck = open('ck_tch.txt', encoding='utf-8').read().strip()
stu = Stu(cookie=sck, uid=STU_UID, course_id=COURSE, class_id=CLASS)
tch = TeacherSide(tck, TCH_UID, ua_mode='h5', max_writes_per_hour=60, min_interval=0, per_day=200)
R = {}

def P(k, v):
    R[k] = v
    print('%-28s %s' % (k, v), flush=True)

# ---------- fixture：教师建 4 个活动 ----------
geo = tch.activity_geo('4000180722358', COURSE, CLASS) or {}
loc = {'address': geo.get('address') or '成都市-温江区-惠民路211号 四川农业大学(成都校区)',
       'latitude': geo.get('latitude') or '30.71142640936642',
       'longitude': geo.get('longitude') or '103.868397592583',
       'range': geo.get('range') or '500米'}
print('fixture 位置真值:', json.dumps(loc, ensure_ascii=False), flush=True)
TL = '1800000'
qr_aid  = tch.create_sign(COURSE, CLASS, other_id='2', face='0', time_long=TL, title='探针-二维码', verbose=False)
time.sleep(1)
code_aid = tch.create_sign(COURSE, CLASS, other_id='5', face='0', time_long=TL, title='探针-签到码', code='246810', verbose=False)
time.sleep(1)
gest_aid = tch.create_sign(COURSE, CLASS, other_id='3', face='0', time_long=TL, title='探针-手势', code='147258', verbose=False)
time.sleep(1)
loc_aid  = tch.create_sign(COURSE, CLASS, other_id='4', face='0', ifopen_address='1', time_long=TL,
                           title='探针-位置', location=loc, verbose=False)
aids = {'qr': qr_aid, 'code': code_aid, 'gesture': gest_aid, 'location': loc_aid}
P('fixture_aids', aids)
if not all(aids.values()):
    print('fixture 创建不全，终止', flush=True); sys.exit(1)

# 教师侧真值（对照用，不算学生能力）
t_enc = (tch.refresh_qrcode(qr_aid) or {}).get('enc', '')
P('teacher_enc_对照', t_enc[:16])

# ---------- P1/P2 学生 cookie 调教师取码接口 ----------
for tag, aid in (('qr', qr_aid), ('code', code_aid)):
    u = ('https://mobilelearn.chaoxing.com/v2/apis/sign/refreshQRCode?activeId=%s&time=%d' % (aid, int(time.time()*1000)))
    r = stu.s.get(u, timeout=25)
    P('P1_stu_refreshQRCode_%s' % tag, 'HTTP %s %s' % (r.status_code, (r.text or '').strip()[:160]))

# ---------- P3 学生 preSign 页信息面 ----------
PATS = {'enc': r'enc=([0-9A-Fa-f]{16,64})', 'widget_e': r'widget/sign/e\?[^"\'<> ]{0,120}',
        'locationInfo': r'locationInfo[^,;}]{0,200}', 'signCode_val': r'id="signCode"[^>]*value="([^"]*)"',
        'reportUrl': r'reportUrl["\']?\s*[:=]\s*["\']([^"\']{0,120})', 'objectId': r'objectId[^,;}]{0,80}',
        'photoAuth': r'photoAuth[a-zA-Z_]*["\']?\s*[:=]\s*["\']?([^"\',;}]{0,60})',
        'signToken': r'signToken["\']?\s*[:=]\s*["\']?([^"\',;}]{0,60})'}
def page_scan(tag, aid):
    html = stu.pre_sign(aid) or ''
    out = {'len': len(html)}
    for k, p in PATS.items():
        hits = list(dict.fromkeys(re.findall(p, html)))[:3]
        if hits:
            out[k] = hits
    P('P3_preSign_%s' % tag, json.dumps(out, ensure_ascii=False)[:420])
    return html
h_qr = page_scan('qr', qr_aid)
h_loc = page_scan('location', loc_aid)
h_code = page_scan('code', code_aid)

# ---------- P4 位置真值是否出现在学生页 ----------
m = re.search(r'locationInfo\s*[:=]\s*(\{[^}]{0,300}\})', h_loc)
P('P4_stu_page_locationInfo', (m.group(1)[:260] if m else 'NOT FOUND'))

# ---------- P5 签到码枚举可行性（checkSignCode） ----------
real = stu.check_sign_code(code_aid, '246810')
P('P5_checkSignCode_真码', json.dumps(real, ensure_ascii=False)[:200])
t0 = time.time(); wrongs = []
for i, c in enumerate(['111111','222222','333333','246811','654321','000000','444444','555555']):
    r = stu.check_sign_code(code_aid, c)
    wrongs.append({'code': c, 'resp': json.dumps(r, ensure_ascii=False)[:90]})
    time.sleep(0.3)
P('P5_checkSignCode_错码8连', '耗时 %.2fs' % (time.time()-t0))
for w in wrongs[:4]:
    P('  错码 %s' % w['code'], w['resp'])

# ---------- P6 学生端能看到哪些活动 ----------
acts = stu.list_active()
P('P6_list_active_count', len(acts))
ident = []
for a in acts[:12]:
    if isinstance(a, dict):
        ident.append({'aid': a.get('activePrimaryId') or a.get('id') or a.get('activeId'),
                      'type': a.get('activeType') or a.get('otherId'), 'title': (a.get('name') or a.get('title') or '')[:14]})
P('P6_list_active_sample', json.dumps(ident, ensure_ascii=False)[:400])

# ---------- P7 学生端 signDetail 是否带位置真值 ----------
d = stu.detail(loc_aid)
P('P7_signDetail_位置类', json.dumps({k: d.get(k) for k in ('activePrimaryId','otherId','ifPhoto','ifopenAddress','status','latitude','longitude','ifGetRange')}, ensure_ascii=False)[:300])

# ---------- P8 学生 cookie 能否读教师活动页 ----------
u = ('https://mobilelearn.chaoxing.com/widget/active/teaActiveView?DB_STRATEGY=COURSEID&STRATEGY_PARA=courseId'
     '&courseId=%s&classId=%s&uid=%s&appType=15' % (COURSE, CLASS, STU_UID))
r = stu.s.get(u, timeout=25)
body = (r.text or '')
P('P8_stu_teaActiveView', 'HTTP %s len=%d 含locationLatitude=%s 含无权限=%s' % (
    r.status_code, len(body), ('locationLatitude' in body), ('无权限' in body or '没有权限' in body or '请先登录' in body)))

# ---------- P9 学生端能不能真正签成（学生 cookie 独占） ----------
r1 = stu.do_code(code_aid, '246810')
P('P9_submit_签到码', str(r1))
r2 = stu.do_location(loc_aid, loc['latitude'], loc['longitude'], loc['address'])
P('P9_submit_位置', str(r2))
r3 = stu.do_qr(qr_aid, t_enc)
P('P9_submit_二维码', str(r3))
r4 = stu.do_code(gest_aid, '147258')
P('P9_submit_手势', str(r4))

json.dump(R, open('out/stuonly_caps.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('-> out/stuonly_caps.json', flush=True)