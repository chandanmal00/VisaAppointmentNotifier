import os
import shutil
from datetime import datetime
from datetime import timedelta
import time
import random
import VisaAppointmentConstants

#"D:\data\data\debug.log",
files = ["D:\data\data\store.log", "D:\data\data\debug.log"]

def logMover():
    for name in files:
        dt1 = (datetime.now() + timedelta(hours=-3)).strftime(VisaAppointmentConstants.DT_FORMAT)
        dt2 = (datetime.now() + timedelta(hours=-4)).strftime(VisaAppointmentConstants.DT_FORMAT)
        dt3 = (datetime.now() + timedelta(hours=-5)).strftime(VisaAppointmentConstants.DT_FORMAT)
        dt4 = (datetime.now() + timedelta(hours=-6)).strftime(VisaAppointmentConstants.DT_FORMAT)
        for dt in [dt1, dt2, dt3, dt4]:
            for file_delete in [name + "_" + dt, name + "." + dt]:
                #shutil.move(name, name+"_"+dt)
                print("file to be deleted: {}".format(file_delete))
                try:
                    if os.path.exists(file_delete):
                        os.remove(file_delete)
                        print("Deleted file {}".format(file_delete))
                except Exception as e:
                    print("unable to move the file {}".format(file_delete))

while True:
    logMover()
    r = random.randint(2,12)
    time.sleep(3600 + r) #sleep for 1 hour
