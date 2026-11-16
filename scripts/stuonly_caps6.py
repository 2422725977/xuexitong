import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stuonly_sign import Stu
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE, CLASS, STU, AID = '269282723', '159926750', '[学生PUID]', '4000180999407'
stu = Stu(cookie=open('ck.txt', encoding='utf-8').read().strip(), uid=STU, course_id=COURSE, class_id=CLASS)
U = [
  ('getActiveDataV2', 'https://mobilelearn.chaoxing.com/ppt/taskAPI/getActiveDataV2?activeId=%s' % AID),
  ('getActiveDataV2+uid', 'https://mobilelearn.chaoxing.com/ppt/taskAPI/getActiveDataV2?activeId=%s&uid=%s&courseId=%s&classId=%s' % (AID, STU, COURSE, CLASS)),
  ('getActiveData', 'https://mobilelearn.chaoxing.com/ppt/activeAPI/getActiveData?activeId=%s' % AID),
  ('signDetail+content', 'https://mobilelearn.chaoxing.com/newsign/signDetail?activePrimaryId=%s&type=1' % AID),
  ('teaActiveView', 'https://mobilelearn.chaoxing.com/widget/active/teaActiveView?DB_STRATEGY=COURSEID&STRATEGY_PARA=courseId&courseId=%s&classId=%s&uid=%s&appType=15' % (COURSE, CLASS, STU)),
  ('stuSignView', 'https://mobilelearn.chaoxing.com/widget/active/stuActiveView?courseId=%s&classId=%s&uid=%s&appType=15' % (COURSE, CLASS, STU)),
]
for tag, u in U:
    try:
        r = stu.s.get(u, timeout=25)
        b = (r.text or '')
        hit = [k for k in ('locationLatitude', 'locationText', '30.71142', '39.9042', '116.4074', '103.868') if k in b]
        print('%-22s HTTP %s len=%d 命中=%s %s' % (tag, r.status_code, len(b), hit, b.strip().replace(chr(10), ' ')[:120]), flush=True)
    except Exception as e:
        print('%-22s ERR %r' % (tag, e), flush=True)