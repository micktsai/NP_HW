import socket
import argparse
import random
import threading
import time

HOST = '127.0.0.1'
PORT = 8000
parser = argparse.ArgumentParser()
parser.add_argument("-host","--host", nargs='?', default=HOST)
parser.add_argument("-port","--port", nargs='?', default=PORT)
args = parser.parse_args()
PORT = int(args.port)
HOST = args.host
clients = []

class client():
    def __init__(self, name, password, email, login = False, now = False):
        self.name = name
        self.password = password
        self.login = login
        self.email = email
        self.number = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
_server.bind((HOST, PORT))
server.listen(10)

def generate():
    global clients
    a = client("andy","123","andy@aaa.com")
    b = client("ben","123","ben@aaa.com")
    c = client("cena","123","cena@aaa.com")
    d = client("deny","123","deny@aaa.com")
    e = client("eve","123","eve@aaa.com")
    f = client("froggy","123","froggy@aaa.com")
    g = client("gina","123","gina@aaa.com")
    h = client("horn","123","horn@aaa.com")
    i = client("ichiro","123","ichiro@aaa.com")
    j = client("john","123","john@aaa.com")
    clients = [a,b,c,d,e,f,g,h,i,j]

now = []
#login = False

def TCP_react(cmsg,login,number):
    global usr,now,clients
    #login reaction
    if cmsg[0] == "login" and len(cmsg) == 3:
        if login == False:
            for item in clients:
                if cmsg[1] == item.name and item.login == False:
                    if cmsg[2] == item.password:
                        rn = random.randrange(1,1000)
                        item.login = True
                        #login = True
                        now[number] = item
                        smsg = "Welcome, " + item.name+"."
                    else:
                        smsg = "Login failed."
                    break
                elif cmsg[1] == item.name and item.login == True:
                    smsg = "Please logout first"
                    break
        elif login == True:
            smsg = "Please logout first"
        else:
            smsg = "Login failed."
    elif cmsg[0] == "login" and len(cmsg) < 3:
        smsg = "Usage: login <username> <password>"
    #logout
    elif cmsg[0] == "logout" and login == True:
        smsg = "Bye, " + now[number].name +"."
        now[number] .login = False
        usr.remove(now[number] )
        now[number]  = None
        login = False
    elif cmsg[0] == "logout" and login == False:
        smsg = "Please login first."
    #list
    elif cmsg[0] == "list-user":
        smsg = "Name            Email"
        for item in clients:
            smsg += "\n"+item.name+"     "+item.email
    #exit 
    elif cmsg[0] == "exit":
        smsg = "exit"
    else:
        smsg = 'wrong method'
    return smsg

def UDP_react(cmsg,number):
    #rigister
    if cmsg[0] == "register" and len(cmsg) ==4:
        for item in clients:
            exist = False
            if cmsg[1] == item.name:
                smsg = "Username already used."
                exist = True
                break
        if exist == False:
            temp = client(cmsg[1],cmsg[3],cmsg[2])
            clients.append(temp)
            smsg = "Register successfully."
    elif cmsg[0] == "register" and len(cmsg) < 4:
        smsg = "Usage: register <username> <email> <password>"
    #whoami
    elif cmsg[0] == "whoami" :
        if cmsg[-1] == str(0):
            smsg = "Please login first."
        else:
            for item in clients:
                if str(item.number) == cmsg[-1]:
                    smsg = item .name
                    break
    return smsg

def TCP(connect,number):
    rn = 0
    login = False
    while True:
        cmsg = str(connect.recv(1024), encoding='utf-8').split(' ')
        print('Client message is:', cmsg)
        smsg = TCP_react(cmsg,login,number)
        if smsg.split(' ')[0] == "Welcome,":
            login = True
            rn = random.randrange(1,1000)
            for item in clients:
                if item.login== True:
                    item.number = rn
            connect.send(smsg.encode())
            time.sleep(0.1)
            connect.send(str(rn).encode())
        elif smsg.split(' ')[0] == "Bye,":
            login = False
            connect.send(smsg.encode())
        elif smsg == "exit":
            connect.send(smsg.encode())
            break
        else:
            connect.send(smsg.encode())
def UDP(number):
    while True:
        cmsg,addr = _server.recvfrom(1024)
        cmsg = cmsg.decode().split(' ')
        print('Client message is:', cmsg)
        smsg = UDP_react(cmsg,number)
        _server.sendto(smsg.encode(),addr)
def listen(connect,number):
    login = False
    TCP_thread = threading.Thread(target=TCP,args=(connect,number,))
    TCP_thread.start()
def main():
    global now
    number = 0
    UDP_thread = threading.Thread(target=UDP,args=(number,))
    UDP_thread.start()
    while True:
        (connect, addr) = server.accept()
        print(addr)
        _thread = threading.Thread(target=listen,args=(connect,number,))
        number +=1
        now.append(None)
        _thread.start()
    connect.close()

if __name__ == "__main__":
    generate()
    main()