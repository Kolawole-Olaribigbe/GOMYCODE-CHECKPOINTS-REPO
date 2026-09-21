from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        message = b"Hello from the networking test app!"

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(message)))
        self.end_headers()
        self.wfile.write(message)


server = HTTPServer(("0.0.0.0", 5000), Handler)
print("Server running on port 5000")
server.serve_forever()
