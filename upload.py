import os
import subprocess

import time
import shutil

if not subprocess.call(("fuser", "/dev/ttyUSB0")):
    print("Something is using the port")
    exit(1)

mpy_cross = "~/git_clones/micropython/mpy-cross/mpy-cross"
files = []

shutil.rmtree("cache", ignore_errors=True)
os.makedirs("cache", exist_ok=True)
for dir, subfolders, subfiles in os.walk("."):
    if ".idea" in dir or "cache" in dir:
        continue
    for sfile in subfiles:
        if not sfile.startswith(".") and "upload.py" not in sfile:
            files.append(os.path.join(dir, sfile)[2:])
    os.makedirs(os.path.join("cache", dir), exist_ok=True)
t1 = time.time()
for f in files:
    if f in ("main.py", "boot.py") or not f.endswith(".py"):
        shutil.copy(f, os.path.join("cache", f))
        continue
    args = (mpy_cross, f, "-o", os.path.join("cache", "{}.mpy".format(f[:-3])))
    subprocess.call(args)
t2 = time.time()
print("Took {:.2f} seconds to compile".format(t2 - t1))
subprocess.call(("ampy", "-p", "/dev/ttyUSB0", "put", "cache", "/"))
t3 = time.time()
print("Took {:.2f} seconds to upload".format(t3 - t2))
shutil.rmtree("cache")
print("DONE")
