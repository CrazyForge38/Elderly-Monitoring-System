#!/usr/bin/python3
from pickle import TRUE
import socket
import sys
import subprocess
import json


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
    print(f"[+][Sending] {message.decode(FORMAT)}")

def recv_message():
    print(f"[+][clinet ID: #] {client.recv(2048).decode(FORMAT)}")

def send_Raw_Data(msg):
    if type(msg) is bytes:
        message = msg
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.sendall(msg)

def send_file(file):
    path = '/home/david/Desktop/Backend/' + file
    file = open(path, 'rb')
    image_data = file.read(2048)
    while image_data:
        send_Raw_Data(image_data)
        image_data = file.read(2048)
    file.close() 
    print("[+] closed File")
    send_message(DISCONNECT_MESSAGE)

def update_json(): # some of the metadata will be board specific
    metadata = {'sensor_id': 78787, 'date': 'xx/xx/xx', 'time': '12:23:43', 'Board_id': 32, 'location': 'bedroom', 'path': 'fes/fse/sef', 'file_type': 'excel1.ods', 'action': 'add to this'}
    with open('/home/david/Desktop/Backend/Json.txt', 'r+') as f:
            f.truncate()
            f.seek(0)
            json.dump(metadata, f)
            print("[+] updated Json")

def Sys_Call_Request():
    while TRUE:
        recv_message()
        print("Enter a sys call: ", end='')
        sys_call = input()
        send_message(sys_call)
        sys_call = int(sys_call)

        if sys_call == 1:
            #update_json()
            print("[+]sending jsona and file")
            #send_file("Json.txt")
            send_file("Json.txt")
            send_file("calc.ods")
        if sys_call == 2:
            user_input = input("[+]Enter a message: ")
            send_message(user_input)


Sys_Call_Request()
