import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stuonly_sign import Stu
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE, CLASS, STU = '269282723', '159926750', '493228247'
stu = Stu(cookie=open('ck.txt', encoding='utf-8').read().strip(), uid=STU, course_id=COURSE, class_id=CLASS)
APP_UA = 'Mozilla/5.0 (Linux; Android 11; MI 9) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.210 Mobile Safari/537.36'
V = [
    ('activelist+fid12', 'https://mobilelearn.chaoxing.com/ppt/activeAPI/courseactivelist?puid=%s&status=1&page=1&pageSize=50&fid=12' % STU, None),
    ('activelist+cpi', 'https://mobilelearn.chaoxing.com/ppt/activeAPI/courseactivelist?puid=%s&status=1&page=1&pageSize=50&courseId=%s&classId=%s' % (STU, COURSE, CLASS), None),
    ('activelist+type0', 'https://mobilelearn.chaoxing.com/ppt/activeAPI/courseactivelist?puid=%s&status=1&page=1&pageSize=50&type=0&flag=1' % STU, None),
    ('activelist+RoleStu', 'https://mobilelearn.chaoxing.com/ppt/activeAPI/courseactivelist?puid=%s&status=1&page=1&pageSize=50&role=1&uid=%s' % (STU, STU), None),
    ('taskactivelist+AppUA', 'https://mobilelearn.chaoxing.com/ppt/activeAPI/taskactivelist?courseId=%s&classId=%s&uid=%s' % (COURSE, CLASS, STU), APP_UA),
    ('backclazzdata+AppUA', 'https://mobilelearn.chaoxing.com/mycourse/backclazzdata?view=json&rss=1', APP_UA),
    ('jsonsignlist', 'https://mobilelearn.chaoxing.com/pptSign/refeashSignList4Json2?activeId=4000180999401&lastTime=0&lastId=0&pageNo=1&appType=15&type=1', None),
    ('activelist+AppUA', 'https://mobilelearn.chaoxing.com/ppt/activeAPI/courseactivelist?puid=%s&status=1&page=1&pageSize=50' % STU, APP_UA),
]
for tag, u, ua in V:
    h = {'User-Agent': ua, 'X-Requested-With': 'com.chaoxing.mobile'} if ua else None
    try:
        r = stu.s.get(u, timeout=25, headers=h)
        b = (r.text or '').strip().replace(chr(10), ' ')
        print('%-24s HTTP %s len=%d %s' % (tag, r.status_code, len(b), b[:150]), flush=True)
    except Exception as e:
        print('%-24s ERR %r' % (tag, e), flush=True)
    time.sleep(0.4)