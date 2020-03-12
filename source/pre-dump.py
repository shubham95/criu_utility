import subprocess
import sys
import shlex
import time
import datetime
import socket


#print(len(sys.argv))
if len(sys.argv) < 5:
    #print("USAGE : process_id, destination_ip, port, iterations, interval, dest_path\n")
    exit(0)


current_milli_time = lambda: int(round(time.time() * 1000))


#print(len(sys.argv))
#print('process_id : '+sys.argv[1])
#print('destination_ip : '+sys.argv[2])
#print('port : '+sys.argv[3])
#print('iterations : '+sys.argv[4])
#print('interval : '+sys.argv[5])
#print('dest_path : '+sys.argv[6])






port = int(sys.argv[3])
ip = sys.argv[2]
dest_path = sys.argv[6]
dest_name = 'destination@'+ip+':'



def pre_dump(pid,itr,interval):
    
    prefix = "dump"
    count = 1
    dirname = prefix + "_" + str(pid) + "_" + str(count)
    
    
    subprocess.run(['rm','-rf',dirname])
    subprocess.run(['mkdir','-p',dirname])
    

    #print("Started .."+ dirname)
    #print(current_milli_time())




   # ##print(subprocess.run(date_cmd,shell=True))


    #open page server command
    #page_server = 'ssh sudo criu page-server -D /tmp/dump --port 4321; cp -r dump'

    # run pageserver on destination

    name = dirname+':'
    s = socket.socket()
    s.connect((ip,port))
    s.send(name.encode())
    time.sleep(1)
    # print("Here")
    # s.recv(100).decode()

    # first pre-dump so no prev_dir
    cmd = 'sudo criu ' + 'pre-dump ' + '--tree ' + str(pid) +  ' --page-server --address '+ ip +' --port 4321 --images-dir ' + dirname + ' --track-mem'
    print(cmd)
    p1 = subprocess.run(cmd,shell=True)
    s.close()

    # Merging dir to destination
    cmd = 'scp -r '+ dirname + '/* '+dest_name+dest_path + dirname +"/"
    #print(cmd)
    (subprocess.run(cmd,shell=True))
    

    #print('Completed... '+ dirname)
    #print(current_milli_time())


    #print("Size of Directory.."+ dirname+"\n")
    cmd = 'du -hs --apparent-size '+ dirname
    #print(subprocess.run(cmd,shell=True))
    

    # start of pre-dumping process
    for i in range(1,itr):
        #interval for next dump
        time.sleep(interval)
        prevdir = "../"+dirname
        count+=1
        dirname = prefix + "_" + str(pid) + "_" + str(count)
        subprocess.run(['rm','-rf',dirname])
        subprocess.run(['mkdir','-p',dirname])

        #print("Started .."+ dirname)
        #print(current_milli_time())


        #cmd = 'criu ' + 'pre-dump ' + '--tree ' + str(pid) +  ' --page-server --address '+ ip +' --port 4321 --images-dir ' + dirname + ' --prev-images-dir ' + prevdir + ' --track-mem'
        cmd = 'sudo criu ' + 'pre-dump ' + '--tree ' + str(pid) +  ' --page-server --address '+ ip +' --port 4321 --images-dir ' + dirname + ' --prev-images '+ prevdir +' --track-mem'
        print(cmd)

        s = socket.socket()
        s.connect((ip,port))
        name = dirname+":"+prevdir
        s.send(name.encode('ascii'))
        time.sleep(1)
        # s.recv(100)
        # s.send(prevdir.encode('ascii'))
        p1 = subprocess.run(cmd,shell=True)
        s.close()
        #print(p1)

        # Merging dir to destination
        cmd = 'scp -r '+ dirname + '/* '+dest_name+dest_path + dirname +"/"
        #print(cmd)
        (subprocess.run(cmd,shell=True))

        #print('Completed... '+ dirname)
        #print(current_milli_time())



        #printing Directory size
        #print("Size of Directory.."+ dirname+"\n")
        cmd = 'du -hs --apparent-size '+ dirname
        #print(subprocess.run(cmd,shell=True))

    
    
    
    #Taking Final Dump
    time.sleep(interval)
    prevdir = "../"+dirname
    count+=1
    dirname = prefix + "_" + str(pid) + "_" + str(count)
    subprocess.run(['rm','-rf',dirname])
    subprocess.run(['mkdir','-p',dirname])
    cmd = 'sudo criu ' + 'dump ' + '--tree ' + str(pid) +' --page-server --address '+ ip +' --port 4321 --images-dir ' + dirname + ' --prev-images-dir ' + prevdir +' --shell-job'
    #cmd = 'criu ' + 'dump ' + '--tree ' + str(pid) +' --page-server --address '+ ip +' --port 4321 --images-dir ' + dirname + ' --shell-job'
        
    #print(cmd)


    s = socket.socket()
    s.connect((ip,port))
    name = dirname+":"+prevdir+":dump"
    s.send(name.encode('ascii'))
    # s.recv(100)
    time.sleep(1)
    p1 = subprocess.run(cmd,shell=True)
    s.close()

    # Merging dir to destination
    cmd = 'scp -r '+ dirname + '/* '+dest_name+dest_path + dirname +"/"
    # (subprocess.run(cmd,shell=True))

    #send message restore on server

    p1 = subprocess.run(cmd,shell=True)
    s = socket.socket()
    s.connect((ip,port))
    name = "scp complete"
    s.send(name.encode('ascii'))
    s.close()



    #print("Size of Directory.."+ dirname+"\n")
    cmd = 'du -hs --apparent-size '+ dirname
    #print(subprocess.run(cmd,shell=True))
    

    #Restoring process
    # #print("Sleeping for 5 Seconds then i will restore the process")
    # time.sleep(5)
    # cmd = './criu/criu/criu ' + 'restore '+ '--shell-job  ' + '--images-dir ' + dirname 
    # p1 = subprocess.run(cmd,shell=True)









pre_dump(int(sys.argv[1]),int(sys.argv[4]),float(sys.argv[5]))