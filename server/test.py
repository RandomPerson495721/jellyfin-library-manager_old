from threading import Thread
import asyncio
import os
import subprocess

# use subprocess to execute a bash command to get ffmpeg path and format it to be used in code
print(subprocess.check_output("which ffmpeg", shell=True).decode("utf-8").strip("\n"))
