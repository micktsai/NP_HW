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
client.connect((HOST, PORT))
while True:
    message = str(input("% "))
    if message.split(' ')[0] == "register" or message == "whoami" or message:
        client.sendto(message.encode(),addr)
    else:
        client.sendto(message.encode())
    serverMessage = str(client.recv(1024), encoding='utf-8')
    if serverMessage != "exit":
        print(serverMessage)
    else:
        break
client.close()