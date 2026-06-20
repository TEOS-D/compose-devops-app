from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import socket
import os
import time

APP_NAME = os.getenv("APP_NAME", "docker-devops-app")
APP_VERSION = os.getenv("APP_VERSION", "1.0")
PORT = int(os.getenv("PORT", "3000"))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = "OK\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
            return
        if self.path == "/api/slow":
            time.sleep(10)
            body = "slow response\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
            return

        body = f"""
        <html>
        <head><title>Docker DevOps App</title></head>
        <body>
            <h1>Hello from Docker Python app</h1>
            <p>App: {APP_NAME}</p>
	    <p>Version: {APP_VERSION}</p>
            <p>Hostname: {socket.gethostname()}</p>
            <p>Path: {self.path}</p>
            <p>Time: {datetime.now()}</p>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body.encode("utf-8"))))
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def do_HEAD(self):
        if self.path == "/health":
            body = "OK\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body.encode("utf-8"))))
            self.end_headers()
            return

        body = ""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", "0")
        self.end_headers()

server = HTTPServer(("0.0.0.0", PORT), Handler)
print(f"{APP_NAME} is running on 0.0.0.0:{PORT}")
server.serve_forever()
