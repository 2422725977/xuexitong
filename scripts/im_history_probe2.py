import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stuonly_sign import Stu
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CK = open('ck.txt', encoding='utf-8').read().strip()
stu = Stu(cookie=CK, uid='493228247', course_id='269282723', class_id='159926750')
CH = '330606364917761'
U = [
  ('tuid+chat_man_id', 'https://im.chaoxing.com/apis/message/getHistory?tuid=493228247&chat_man_id=%s&msg_status=0&last_msg_time=&pageSize=20' % CH),
  ('+msg_status=1', 'https://im.chaoxing.com/apis/message/getHistory?tuid=493228247&chat_man_id=%s&msg_status=1&last_msg_time=&pageSize=20' % CH),
  ('+last_msg_time=now', 'https://im.chaoxing.com/apis/message/getHistory?tuid=493228247&chat_man_id=%s&msg_status=0&last_msg_time=%d&pageSize=20' % (CH, int(time.time()*1000))),
  ('裸 chat_man_id', 'https://im.chaoxing.com/apis/message/getHistory?chat_man_id=%s&msg_status=0&pageSize=20' % CH),
]
for tag, u in U:
    r = stu.s.get(u, timeout=25)
    b = (r.text or '').strip()
    print('%-20s HTTP %s len=%5d %s' % (tag, r.status_code, len(b), b.replace(chr(10),' ')[:400]), flush=True)
    time.sleep(0.5)