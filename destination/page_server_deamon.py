import sys
import socket
import time
import subprocess



if(len(sys.argv) <2):
    #print("Usage port nr")
    exit(0)
s = socket.socket()
#print("Socket succesfully created")


port = int(sys.argv[1])

s.bind(('',port))
#print("socket binded to %s" %(port))

s.listen(5)



# cmd = 'sudo rm -rf '
# p1 = subprocess.run(cmd, shell=True)
# cmd = 'sudo mkdir '
# p1 = subprocess.run(cmd, shell=True)



while True:

    c, addr = s.accept()
    name = c.recv(1024).decode('ascii')
    #print(name)
    dirname = name.split(':')[0]
    prevdir = name.split(':')[1]



    # prev_dirname = c.recv(1024).decode('ascii')
    ##print(dirname)
    ##print(prevdir)

    if(prevdir == ""):
        page_server_cmd = "sudo criu page-server --auto-dedup -D "+dirname+" --port 4321"
    else:
        page_server_cmd = 'sudo criu page-server --auto-dedup -D ' +dirname+ ' --prev-images-dir ' +prevdir+ ' --port 4321'





    #print("Got connection from",addr)
    cmd = 'sudo mkdir -p '+dirname
    p1 = subprocess.run(cmd, shell=True)

    cmd = 'sudo chmod 777 '+dirname
    p1 = subprocess.run(cmd, shell=True)

    

    print(page_server_cmd)
    p1 = subprocess.run(page_server_cmd,shell=True)
    c.send("Executed..".encode())
    #print("Executed...")
    # c.send("thankyou".encode())



    #print((name.split(':')))
    if(len(name.split(':')) > 2 and name.split(':')[2] == "dump"):
        #print('final dump')
        #it is last dump break the while loop and then restore
        break
    c.close()

# s.close()


# Restoring process here

#wait for scp done

# time.sleep(1)
c, addr = s.accept()
name=c.recv(1024).decode('ascii')
print("name : "+name)

cmd = 'sudo criu ' + 'restore '+ ' --images-dir ' + dirname + ' --shell-job'
print(cmd)
p1 = subprocess.run(cmd,shell=True)

c.close()
s.close()

