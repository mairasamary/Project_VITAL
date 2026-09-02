#!/usr/bin/env python3
import http.client, sys

def req(path):
    c=http.client.HTTPConnection("127.0.0.1",8765,timeout=5); c.request("GET",path); r=c.getresponse()
    body=r.read().decode("utf-8",errors="replace"); h={k.lower():v for k,v in r.getheaders()}; s=r.status; c.close(); return s,h,body

def require(ok,msg):
    print(("PASS: " if ok else "FAIL: ")+msg)
    if not ok: sys.exit(1)

s,h,_=req("/")
require(s==200,"fixture root returns 200")
require(h.get("x-content-type-options","").lower()=="nosniff","X-Content-Type-Options is nosniff")
require("default-src" in h.get("content-security-policy",""),"Content-Security-Policy is present")
require(h.get("x-frame-options","").upper() in ("DENY","SAMEORIGIN"),"frame protection is present")
cookie=h.get("set-cookie","")
require("HttpOnly" in cookie,"session cookie is HttpOnly")
require("SameSite=Strict" in cookie,"session cookie uses SameSite=Strict")
s,h,_=req("/protected")
require(s in (301,302,303,307,308,401,403),"unauthenticated protected resource is not returned as 200")
if s in (301,302,303,307,308): require(h.get("location")=="/login","protected resource redirects to login")
print("SECURITY CI CHECKS PASSED")
