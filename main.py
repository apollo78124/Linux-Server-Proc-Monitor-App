#!/usr/bin/python
import http.server
import socketserver
from http.server import BaseHTTPRequestHandler
from WebRequestHandler import WebRequestHandler1

PORT=8003
with socketserver.TCPServer(("localhost", PORT), WebRequestHandler1) as httpd:
    print(f"serving at port {PORT}")
    httpd.serve_forever()

# while (True) :
#     os.system('cls')
#     getMemoryStatus()
#     sleep(0.5)


