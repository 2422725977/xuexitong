import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stuonly_sign import Stu
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE, CLASS, STU, LOC_AID = '269282723', '159926750', '493228247', '4000180999407'
stu = Stu(cookie=open('ck.txt', encoding='utf-8').read().strip(), uid=STU, course_id=COURSE, class_id=CLASS)
URLS = [
    ('newsign/preSign', 'https://mobilelearn.chaoxing.com/newsign/preSign?courseId=%s&classId=%s&activePrimaryId=%s&uid=%s&role=1&appType=15&isTeacherViewOpen=0' % (COURSE, CLASS, LOC_AID, STU)),
    ('pptSign/preSign', 'https://mobilelearn.chaoxing.com/pptSign/preSign?activePrimaryId=%s&sys=1&chatId=&general=&ls=1&appType=15&classId=%s&uid=%s' % (LOC_AID, CLASS, STU)),
    ('pptSign/preSign+src1', 'https://mobilelearn.chaoxing.com/pptSign/preSign?activePrimaryId=%s&sys=1&general=&appType=15&classId=%s&uid=%s&source=1&isTeachingCalendar=1&showSaveBtn=0&hideBeginButton=1' % (LOC_AID, CLASS, STU)),
    ('widget/sign/e', 'https://mobilelearn.chaoxing.com/widget/sign/e?id=%s&c=0&enc=&DB_STRATEGY=PRIMARY_KEY&STRATEGY_PARA=id' % LOC_AID),
]
PAT = {'addr': r'["\']address["\']\s*:\s*["\']([^"\']{4,60})', 'lat_lon': r'latitude["\']?\s*[:=]\s*["\']?(-?\d+\.\d{3,})',
       'locationResult': r'locationResult', 'signCode_val': r'id="signCode"[^>]*value="([^"]*)"',
       'enc': r'[?&"]enc=([0-9A-Fa-f]{16,64})', 'geoFix': r'(getLocation|geolocation|wx\.getLocation|baidu|amap)'}
for tag, u in URLS:
    try:
        r = stu.s.get(u, timeout=25)
        h = r.text or ''
        out = {'HTTP': r.status_code, 'len': len(h)}
        for k, p in PAT.items():
            m = list(dict.fromkeys(re.findall(p, h)))[:2]
            if m: out[k] = m
        print('%-20s %s' % (tag, json.dumps(out, ensure_ascii=False)[:340]), flush=True)
    except Exception as e:
        print('%-20s ERR %r' % (tag, e), flush=True)