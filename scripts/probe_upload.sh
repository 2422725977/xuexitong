#!/bin/bash
cd .
CK="$(cat ck.txt)"
TOK=$(curl -s -m 20 "https://pan-yz.chaoxing.com/api/token/uservalid" -H "Cookie: $CK" -H "User-Agent: Mozilla/5.0" | /opt/anaconda3/bin/python3 -c "import sys,json;print(json.load(sys.stdin).get('_token',''))")
echo "token len=${#TOK}"
try() {
  echo "---- $1"
  shift
  curl -s -m 30 -X POST "https://pan-yz.chaoxing.com/upload" "$@" -F "puid=[学生PUID]" -F "_token=$TOK" -F "file=@out/sign_probe.png;type=image/png" | head -c 300
  echo; sleep 5
}
try "app-UA + X-Requested-With" -H "Cookie: $CK" -H "User-Agent: Mozilla/5.0 (Linux; Android 11; MI 9 Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.210 Mobile Safari/537.36" -H "X-Requested-With: com.chaoxing.mobile" -H "Referer: https://pan-yz.chaoxing.com/"
try "只有 Cookie 无 UA" -H "Cookie: $CK"
try "uid 字段代替 puid" -H "Cookie: $CK" -H "User-Agent: Mozilla/5.0"
try "带 _from=mobilelearn" -H "Cookie: $CK" -H "User-Agent: Mozilla/5.0" -F "_from=mobilelearn"
