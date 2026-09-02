#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import argparse

class Handler(BaseHTTPRequestHandler):
    def security_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Frame-Options", "DENY")

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.security_headers()
            self.send_header("Set-Cookie", "PVSESSION=controlled; Path=/; HttpOnly; SameSite=Strict")
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Project VITAL controlled security fixture")
        elif self.path == "/protected":
            self.send_response(302)
            self.security_headers()
            self.send_header("Location", "/login")
            self.end_headers()
        elif self.path == "/login":
            self.send_response(200)
            self.security_headers()
            self.end_headers()
            self.wfile.write(b"Controlled login page")
        else:
            self.send_response(404)
            self.security_headers()
            self.end_headers()

    def log_message(self, fmt, *args):
        pass

if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("--port",type=int,default=8765); a=p.parse_args()
    HTTPServer(("127.0.0.1",a.port),Handler).serve_forever()
