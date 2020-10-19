import socket
import argparse

HOST = '127.0.0.1'
PORT = 8000
parser = argparse.ArgumentParser()
parser.add_argument("port", nargs='?', default=PORT)
args = parser.parse_args()
PORT = int(args.port)

addr = (HOST,PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.connect((HOST, PORT))
_client.connect((HOST, PORT))
method = "TCP"
rn = 0
while True:
    message = str(input("% "))
    if message.split(' ')[0] == "register" or message == "whoami":
        if message == "whoami":
            message += " " + str(rn)
            _client.sendto(message.encode(),(HOST,PORT))
        else:
            _client.sendto(message.encode(),(HOST,PORT))
        method = "UDP"
    else:
        client.send(message.encode())
        method = "TCP"
    if method == "TCP":
        serverMessage = str(client.recv(1024), encoding='utf-8')
        if serverMessage.split(' ')[0] == "Welcome,":
            rn = str(client.recv(1024), encoding='utf-8')
    else:
        serverMessage,_addr = _client.recvfrom(1024)
        serverMessage = serverMessage.decode()
    if serverMessage != "exit":
        print(serverMessage)
    else:
        break
client.close()