
import json, requests, sys
UA = "Mozilla/5.0 (Linux; U; Android 11; zh-cn; Pixel 4 Build/RQ3A.210805.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
H = {"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9"}
probes = {
 "cards": "https://mooc1-api.chaoxing.com/knowledge/cards?clazzid=1&courseid=1&knowledgeid=1&num=0&isPhone=1&control=1&cpi=1",
 "job":   "https://mooc1-api.chaoxing.com/ananas/job?jobid=1&knowledgeid=1&courseid=1&clazzid=1&jtoken=1",
 "cards_noauth": "https://mooc1-api.chaoxing.com/knowledge/cards?clazzid=1&courseid=1&knowledgeid=1",
}
for k,u in probes.items():
    try:
        r = requests.get(u, headers=H, timeout=12, allow_redirects=False)
        body = r.text.strip().replace("\n"," ")[:260]
        print("[%s] HTTP %s len=%d ct=%s" % (k, r.status_code, len(r.content), r.headers.get("Content-Type","")))
        print("    set-cookie:", "; ".join(sorted({c.split("=")[0] for c in r.headers.get("Set-Cookie","").split(",") if "=" in c})) or "-")
        print("    body:", body)
    except Exception as e:
        print("[%s] ERR %s" % (k, e))
