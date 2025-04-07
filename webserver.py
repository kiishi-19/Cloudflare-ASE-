#!/usr/bin/env python3
# A web server to echo back a request's headers and data.
#
# Usage: ./webserver
#        ./webserver 0.0.0.0:5000

from http.server import HTTPServer, BaseHTTPRequestHandler
from sys import argv

BIND_HOST = "localhost"
PORT = 8080


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.write_response(b"")

    def do_POST(self):
        content_length = int(self.headers.get("content-length", 0))
        body = self.rfile.read(content_length)

        self.write_response(body)

    def write_response(self, content):
    # Start by adding method and HTTP version
        request_line = f"{self.command} {self.path} {self.request_version}\n"

        # Add headers
        headers_str = "Request Headers:\n"
        for key, value in self.headers.items():
            headers_str += f"{key}: {value}\n"

        # Add body
        body_str = "\nRequest Body:\n" + content.decode("utf-8")

        # Full output
        output = request_line + headers_str + body_str

        # Send to client
        encoded = output.encode("utf-8")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(encoded)

        # Also print to server
        print(output)




if len(argv) > 1:
    arg = argv[1].split(":")
    BIND_HOST = arg[0]
    PORT = int(arg[1])

print(f"Listening on http://{BIND_HOST}:{PORT}\n")

httpd = HTTPServer((BIND_HOST, PORT), SimpleHTTPRequestHandler)
httpd.serve_forever()
