import subprocess
import shutil
import os

if os.path.exists("dist"):
    shutil.rmtree("dist")
subprocess.run("python -m build", shell=True)
