#!/usr/bin/env python3
"""Create a tar with a simple text file."""
import tarfile
import io
import os

def create_text_tar():
    """Create tar with a .txt file."""
    text_content = b"Hello from extracted tar file!"
    
    with tarfile.open("text_payload.tar", "w") as tar:
        ti = tarfile.TarInfo("test.txt")
        ti.size = len(text_content)
        ti.mode = 0o644
        tar.addfile(ti, io.BytesIO(text_content))
    
    print("Created text_payload.tar")

if __name__ == "__main__":
    os.chdir(r"C:\Users\Alexandru Moga\Documents\first-gooogot-game\explo")
    create_text_tar()
