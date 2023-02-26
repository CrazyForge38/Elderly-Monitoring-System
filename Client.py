#!/usr/bin/python3
import socket

HEADER = 64
PORT = 5051
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
print(SERVER)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    if type(msg) is bytes:
        message = msg
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.sendall(msg)
    else:
        print(msg)
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
    print(client.recv(2048).decode(FORMAT))
 
#file = open("thatonephoto.jpg", 'rb')
#image_data = file.read(2048)
#while image_data:
#    send(image_data)
#    image_data = file.read(2048)
#file.close()   
input() 
send("Hello World!")
input()
send("Hello everyone")
input()
#send("hello Tim")
#send(DISCONNECT_MESSAGE) 
