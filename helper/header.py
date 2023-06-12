import os, subprocess
from helper.text import text

def header(main: bool=False, path: str = ""):
    cmd = "clear" if os.name == "posix" else "cls"
    output = subprocess.getoutput(cmd)

    print(output)
    text(main, path)