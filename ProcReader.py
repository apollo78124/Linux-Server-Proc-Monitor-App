import os
from time import sleep

def getMemoryStatus():
    pid = os.getpid()
    status_file = open("/proc/{}/status".format(pid), "r")
    for line in status_file:
        if "VmData" in line:
            print(line)
    status_file.close()