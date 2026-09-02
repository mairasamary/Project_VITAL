#!/usr/bin/env python3
import argparse,ssl
from urllib import request,error
class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl): return None
p=argparse.ArgumentParser();p.add_argument("url");a=p.parse_args()
ctx=ssl.create_default_context();ctx.check_hostname=False;ctx.verify_mode=ssl.CERT_NONE
opener=request.build_opener(NoRedirect(),request.HTTPSHandler(context=ctx));req=request.Request(a.url,headers={"User-Agent":"Project-VITAL-Unauth-Check/1.0"})
try:r=opener.open(req,timeout=10);status,loc=r.status,r.headers.get("Location");body=r.read(512).decode("utf-8",errors="replace")
except error.HTTPError as e:status,loc=e.code,e.headers.get("Location");body=e.read(512).decode("utf-8",errors="replace")
print("Requested:",a.url);print("Status:",status);print("Location:",loc or "(none)");print("Body preview:",repr(body[:160]))
if status==200:print("REVIEW REQUIRED: verify whether protected content was actually returned.")
elif status in (301,302,303,307,308,401,403):print("Expected access-control pattern observed.")
else:print("Unexpected response; investigate before drawing a conclusion.")
