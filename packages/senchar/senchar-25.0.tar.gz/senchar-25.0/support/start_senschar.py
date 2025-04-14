"""
Python process start file
"""

import subprocess

OPTIONS = ""
CMD = (
    f"ipython --ipython-dir=/data/ipython --profile senchar -i -m senchar -- {OPTIONS}"
)

p = subprocess.Popen(
    CMD,
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)
