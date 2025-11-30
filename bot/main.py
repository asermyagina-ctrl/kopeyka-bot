import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK - Ultra Simple Server')
    
    def log_message(self, format, *args):
        print(f"Request: {format % args}")

def main():
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting ULTRA SIMPLE server on port {port}")
    
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print("✅ Server started successfully!")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped")

if __name__ == '__main__':
    main()
