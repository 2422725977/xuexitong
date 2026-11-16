import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stuonly_sign import Stu
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
stu = Stu(cookie=open('ck.txt', encoding='utf-8').read().strip(), uid='493228247', course_id='269282723', class_id='159926750')
CH = '330606364917761'
U = [
  ('getHistory GET 基本', 'https://im.chaoxing.com/apis/message/getHistory?chatId=%s&uid=493228247&pageNo=1&pageSize=20' % CH),
  ('getHistory+startTime', 'https://im.chaoxing.com/apis/message/getHistory?chatId=%s&uid=493228247&pageNo=1&pageSize=20&startTime=0&endTime=0' % CH),
  ('getHistory+puid', 'https://im.chaoxing.com/apis/message/getHistory?chatId=%s&puid=493228247&page=1&size=20' % CH),
  ('getHistory+groupId', 'https://im.chaoxing.com/apis/message/getHistory?groupId=%s&uid=493228247&pageNo=1&pageSize=20' % CH),
  ('getHistory 裸', 'https://im.chaoxing.com/apis/message/getHistory'),
  ('getChatAttachmentList', 'https://im.chaoxing.com/apis/message/getChatAttachmentList?chatId=%s&uid=493228247' % CH),
]
for tag, u in U:
    try:
        r = stu.s.get(u, timeout=25)
        print('%-24s HTTP %s len=%4d %s' % (tag, r.status_code, len(r.text or ''), (r.text or '').strip().replace(chr(10),' ')[:200]), flush=True)
    except Exception as e:
        print('%-24s ERR %r' % (tag, e), flush=True)
print('--- POST getHistory ---', flush=True)
try:
    r = stu.s.post('https://im.chaoxing.com/apis/message/getHistory', data={'chatId': CH, 'uid': '493228247', 'pageNo': '1', 'pageSize': '20'}, timeout=25)
    print('POST', r.status_code, (r.text or '')[:200].replace(chr(10),' '), flush=True)
except Exception as e:
    print('POST ERR %r' % (e,), flush=True)