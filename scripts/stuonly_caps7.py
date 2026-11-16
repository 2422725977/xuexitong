import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stuonly_sign import Stu
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
stu = Stu(cookie=open('ck.txt', encoding='utf-8').read().strip(), uid='493228247', course_id='269282723', class_id='159926750')
for tag, u in [('V2', 'https://mobilelearn.chaoxing.com/ppt/taskAPI/getActiveDataV2?activeId=4000180999407'),
               ('V2-qr', 'https://mobilelearn.chaoxing.com/ppt/taskAPI/getActiveDataV2?activeId=4000180999399')]:
    r = stu.s.get(u, timeout=25)
    print('===', tag, r.status_code, len(r.text), flush=True)
    print(r.text, flush=True)