#!/usr/bin/env python3
import argparse,json,ssl
from urllib import request,error
from pathlib import Path
from http.cookies import SimpleCookie
HEADERS=["strict-transport-security","content-security-policy","x-content-type-options","referrer-policy","x-frame-options"]
p=argparse.ArgumentParser();p.add_argument("url");p.add_argument("--output");a=p.parse_args()
ctx=ssl.create_default_context();ctx.check_hostname=False;ctx.verify_mode=ssl.CERT_NONE
req=request.Request(a.url,headers={"User-Agent":"Project-VITAL-Security-Baseline/1.0"})
try:
    with request.urlopen(req,context=ctx,timeout=10) as r: status,final_url,headers=r.status,r.geturl(),r.headers; r.read(4096)
except error.HTTPError as e: status,final_url,headers=e.code,e.geturl(),e.headers
hm={k.lower():v for k,v in headers.items()}
result={"requested_url":a.url,"final_url":final_url,"status":status,"selected_headers":{h:hm.get(h) for h in HEADERS},"set_cookie_observations":[]}
for raw in (headers.get_all("Set-Cookie") or []):
    c=SimpleCookie()
    try:c.load(raw)
    except Exception:continue
    for name,m in c.items(): result["set_cookie_observations"].append({"name":name,"secure":bool(m["secure"]),"httponly":bool(m["httponly"]),"samesite":m["samesite"] or None})
text=json.dumps(result,indent=2);print(text)
if a.output:
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text+"\n")
