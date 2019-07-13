import os
import gzip

dir_list = os.listdir("/home/AIWolfPy/pre_logs/gat2017_15")

for dir in dir_list:
    file_list = os.listdir("/home/AIWolfPy/pre_logs/gat2017_15/"+dir)
    for i in range(100):
        file_name = str(i).zfill(3)+".log"
        if file_name not in file_list:
            print("dir: ",dir,"file_name: ",file_name)
            if str(i).zfill(3)+".log.gz" in file_list:
                print("find zip file",str(i).zfill(3)+".log.gz")
                wf = open("/home/AIWolfPy/pre_logs/gat2017_15/"+dir+"/"+str(i).zfill(3)+".log","w")
                wf.write("broken\n")
