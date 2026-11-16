import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stuonly_sign import Stu
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
stu = Stu(cookie=open('ck.txt', encoding='utf-8').read().strip(), uid='493228247', course_id='269282723', class_id='159926750')
u = 'https://mobilelearn.chaoxing.com/widget/sign/e?id=4000180999425&c=0&enc=&DB_STRATEGY=PRIMARY_KEY&STRATEGY_PARA=id'
r = stu.s.get(u, timeout=25)
print(r.text, flush=True)