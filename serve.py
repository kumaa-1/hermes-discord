#!/usr/bin/env python3
"""
Simple HTTP server for Discord verification endpoints
Serves static files from the hermes-discord-static directory
"""
import http.server
import socketserver
import os
import json
from urllib.parse import urlparse, parse_qs

PORT = 5000
DIRECTORY = r"C:\Users\Admin\hermes-discord-static"

class DiscordVerificationHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def do_GET(self):
        # Parse URL
        parsed = urlparse(self.path)
        
        # Handle verification endpoint
        if parsed.path == '/verify-user':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Get user_id from query params
            query_params = parse_qs(parsed.query)
            user_id = query_params.get('user_id', ['unknown'])[0]
            
            response = {
                "verified": True,
                "user_id": user_id,
                "roles": ["verified_user"],
                "message": "User verification successful"
            }
            self.wfile.write(json.dumps(response).encode())
            return
        
        # Serve static files for other paths
        super().do_GET()

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", PORT), DiscordVerificationHandler) as httpd:
        print("=" * 60)
        print("⚡ Hermes Discord Bot - Static Server")
        print("=" * 60)
        print()
        print(f"Serving at http://localhost:{PORT}")
        print()
        print("Available endpoints:")
        print(f"  • http://localhost:{PORT}/")
        print(f"  • http://localhost:{PORT}/verify-user")
        print(f"  • http://localhost:{PORT}/terms-of-service.html")
        print(f"  • http://localhost:{PORT}/privacy-policy.html")
        print()
        print("Press Ctrl+C to stop")
        print("=" * 60)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
