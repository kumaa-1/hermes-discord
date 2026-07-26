#!/usr/bin/env python3
"""
Start Discord verification server with ngrok tunnel
"""
import subprocess
import sys
import time
import os

# Configuration
NGROK_AUTHTOKEN = "3H2YU7Nd0yGyiqCWUxR2hhNilgd_6dxCc6FNw5aP1yWSAjARF"
PORT = 5000
SCRIPT_DIR = r"C:\Users\Admin\hermes-discord-static"

def main():
    print("=" * 60)
    print("⚡ Hermes Discord Bot - Server + Ngrok Tunnel")
    print("=" * 60)
    print()
    
    # Start the HTTP server in background
    print("Starting HTTP server...")
    server_process = subprocess.Popen(
        [sys.executable, os.path.join(SCRIPT_DIR, "serve.py")],
        cwd=SCRIPT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )
    
    time.sleep(2)
    print(f"✓ HTTP server started (PID: {server_process.pid})")
    
    # Configure and start ngrok
    print("\nStarting ngrok tunnel...")
    try:
        from pyngrok import ngrok, conf
        
        # Set authtoken
        conf.get_default().auth_token = NGROK_AUTHTOKEN
        conf.get_default().region = "us"  # Change if needed
        
        # Start tunnel
        public_url = ngrok.connect(PORT, "http")
        
        print(f"✓ Ngrok tunnel established!")
        print()
        print("=" * 60)
        print("🌐 PUBLIC URLs FOR DISCORD DEVELOPER PORTAL")
        print("=" * 60)
        print()
        print("Linked Roles Verification URL:")
        print(f"  {public_url}/verify-user")
        print()
        print("Terms of Service URL:")
        print(f"  {public_url}/terms-of-service.html")
        print()
        print("Privacy Policy URL:")
        print(f"  {public_url}/privacy-policy.html")
        print()
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Go to https://discord.com/developers/applications")
        print("2. Enable 'Message Content Intent' in Bot settings")
        print("3. Paste the URLs above into the appropriate fields")
        print()
        print("Press Ctrl+C to stop both server and tunnel")
        print("=" * 60)
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nStopping...")
            ngrok.disconnect(public_url)
            server_process.terminate()
            server_process.wait()
            print("✓ Server and tunnel stopped")
            
    except ImportError:
        print("✗ pyngrok not available")
        print("\nAlternative: Use ngrok manually:")
        print(f"  1. Download ngrok from https://ngrok.com/download")
        print(f"  2. Run: ngrok config add-authtoken {NGROK_AUTHTOKEN}")
        print(f"  3. Run: ngrok http {PORT}")
        server_process.terminate()
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error starting ngrok: {e}")
        print("\nServer is still running on http://localhost:5000")
        print("You can use another tunneling service (cloudflared, localtunnel, etc.)")
        print("\nPress Ctrl+C to stop the server")
        try:
            server_process.wait()
        except KeyboardInterrupt:
            server_process.terminate()

if __name__ == "__main__":
    main()
