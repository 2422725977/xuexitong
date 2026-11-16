import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stuonly_sign import Stu
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
stu = Stu(cookie=open('ck.txt', encoding='utf-8').read().strip(), uid='[学生PUID]', course_id='269282723', class_id='159926750')
for aid in ('4000180999407', '4000180999405'):
    d = stu.detail(aid)
    print('=== signDetail', aid, 'keys:', len(d), flush=True)
    print(json.dumps(d, ensure_ascii=False)[:1200], flush=True)
    print('  含 location/addr 字段:', [k for k in d if 'ocat' in k.lower() or 'addr' in k.lower()], flush=True)