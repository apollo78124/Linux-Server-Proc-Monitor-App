import json
import os
from datetime import datetime
from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qsl, urlparse

class WebRequestHandler1(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path == '/actions/getOpenConnections/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "connections": [
                    {"ip": "192.168.1.1", "port": 80, "status": "active"},
                    {"ip": "192.168.1.2", "port": 443, "status": "inactive"}
                ]
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        elif self.path == '/actions/getTime/':
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
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON."}).encode('utf-8'))


# 1. Bytes Sent and Received
def get_network_io(pid):
    net_dev_path = f'/proc/{pid}/net/dev'

    if not os.path.exists(net_dev_path):
        return None  # Process does not exist or does not have net/dev info

    try:
        with open(net_dev_path, 'r') as file:
            lines = file.readlines()

        # Skip the first two lines (header)
        data = {}
        for line in lines[2:]:
            # Split the line into interface name and stats
            parts = line.split(':')
            if len(parts) > 1:
                interface = parts[0].strip()
                stats = parts[1].strip().split()

                # Convert bytes sent and received to integers
                bytes_received = int(stats[0]) if len(stats) > 0 else 0
                bytes_sent = int(stats[8]) if len(stats) > 8 else 0

                data[interface] = {
                    "bytes_received": bytes_received,
                    "bytes_sent": bytes_sent
                }

        return data

    except Exception as e:
        print(f"Error reading network stats for PID {pid}: {e}")
        return None