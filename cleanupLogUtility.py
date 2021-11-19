import os
import shutil
from datetime import datetime
import time
dt = datetime.today().strftime("%Y%m%d")
files = ["D:\data\data\debug.log", "D:\data\data\store.log"]

def logMover():
    for name in files:
        dt = datetime.today().strftime("%Y%m%d%H")
        try:
            shutil.move(name, name+"_"+dt)
        except Exception as e:
            print("unable to move the file")

while True:
    logMover()
    time.sleep(3600) #sleep for 1 hour
