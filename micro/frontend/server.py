#!/usr/bin/env python3
"""
Simple HTTP server for the frontend
Serves static files and allows CORS
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os


class CORSHTTPRequestHandler(SimpleHTTPRequestHandler):
    """HTTP request handler with CORS support"""
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle preflight requests"""
        self.send_response(200)
        self.end_headers()


def run(port=8000):
    """Start the HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSHTTPRequestHandler)
    
    print(f"""
    ========================================
       Frontend Server Started!
    ========================================
    
    📱 URL: http://localhost:{port}
    
    Pages available:
    - Home/Catalog: http://localhost:{port}/index.html
    - Login: http://localhost:{port}/login.html
    - Register: http://localhost:{port}/register.html
    - Cart: http://localhost:{port}/cart.html
    
    Make sure the backend services are running:
    - Customer Service: http://localhost:8001
    - Book Service: http://localhost:8002
    - Cart Service: http://localhost:8003
    
    Press Ctrl+C to stop the server
    ========================================
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        httpd.shutdown()


if __name__ == '__main__':
    # Change to the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    run(8000)
