#!/usr/bin/python3
from pickle import TRUE
import socket
import sys

HEADER = 64
PORT = 5053
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
print(SERVER)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send_message(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(f"[Sending] {message.decode(FORMAT)}")

def recv_message():
    print(f"[clinet ID: #] {client.recv(2048).decode(FORMAT)}")
    #print(client.recv(2048).decode(FORMAT))

def send_Raw_Data(msg):
    if type(msg) is bytes:
        message = msg
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.sendall(msg)
        print(client.recv(2048).decode(FORMAT))

def Sys_Call_Photo():
    print("#Testing print")
    file = open("testimage.PNG", 'rb')
    image_data = file.read(2048)
    #print(image_data)
    print()
    print()
    while image_data:
        send_Raw_Data(image_data)
        image_data = file.read(2048)
    file.close() 
    print("[+] closed File")
    send_message(DISCONNECT_MESSAGE)

def Sys_Call_Request():
    while TRUE:
        recv_message()
        print("Enter a sys call: ", end='')
        #read = input()
        sys_call = input()
        send_message(sys_call)
        print("After first msg sent")
        sys_call = int(sys_call)
        if sys_call == 1:
            print("phjto call")
            Sys_Call_Photo()
        if sys_call == 2:
            send_message("Test the world")

Sys_Call_Request()
