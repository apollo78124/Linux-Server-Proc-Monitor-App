import json
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler
from BytesCount import get_network_io
from activetcp import get_active_tcp_connections
from activeudp import get_active_udp_connections
from networkinterfaceusage import get_network_interface_usage
from listeningports import get_listening_ports

class WebRequestHandler1(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/actions/getTime/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.wfile.write(current_time.encode('utf-8'))
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("index.html", "rb") as file:
                self.wfile.write(file.read())
        else:
            try:
                file_to_open = open(self.path[1:]).read()
                self.send_response(200)
            except:
                file_to_open = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_POST(self):
        try:
            # Get the content length
            content_length = int(self.headers['Content-Length'])
            # Read the body of the POST request
            post_data = self.rfile.read(content_length)
            # Parse the JSON data
            data = json.loads(post_data)
            pid = data.get('pid')
            # 1. Bytes Sent and Received
            if self.path == '/actions/task1/':
                network_io = get_network_io(pid)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = network_io if network_io is not None else {
                    "error": "No data found for the given PID or process does not exist."}
                self.wfile.write(json.dumps(response).encode('utf-8'))
            # 2. Active TCP connections
            elif self.path == '/actions/task2/':
                tcpcons = get_active_tcp_connections(pid)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = tcpcons if tcpcons is not None else {
                    "error": "No data found for the given PID or process does not exist."}
                self.wfile.write(json.dumps(response).encode('utf-8'))
            # 3. Active UDP connections
            elif self.path == '/actions/task3/':
                udpcons = get_active_udp_connections(pid)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = udpcons if udpcons is not None else {
                    "error": "No data found for the given PID or process does not exist."}
                self.wfile.write(json.dumps(response).encode('utf-8'))
            # 4. Network Interface Usage
            elif self.path == '/actions/task4/':
                udpcons = get_network_interface_usage(pid)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = udpcons if udpcons is not None else {
                    "error": "No data found for the given PID or process does not exist."}
                self.wfile.write(json.dumps(response).encode('utf-8'))
            # 5. Listening Ports
            elif self.path == '/actions/task5/':
                listeningports = get_listening_ports(pid)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = listeningports if listeningports is not None else {
                    "error": "No data found for the given PID or process does not exist."}
                self.wfile.write(json.dumps(response).encode('utf-8'))
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON."}).encode('utf-8'))