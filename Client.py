#!/usr/bin/python3
from pickle import TRUE
import socket
import sys
import subprocess
import json


HEADER = 64
PORT = 5052
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

def Sys_Call_Photo(file):
    print("#Testing print")
    file = open(file, 'rb')
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

def update_json():
    print('+')
    metadata = {'sensor_id': 122, 'date': 'xx/xx/xx', 'time': '12:23:43', 'Board_id': 32, 'location': 'bedroom', 'path': 'fes/fse/sef', 'file_type': '.ods', 'action': 'add to this'}
    metadata_str = json.dumps(metadata)
    file_type = "jsontest.txt"
    instruction = 1
    print('+')
    result = subprocess.run(['python3', '/home/david/Desktop/Backend/jrw.py', file_type, str(instruction), metadata_str], stdout=subprocess.PIPE)
    print(result.stdout.decode())
    print(')))))')

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
            Sys_Call_Photo("Json.txt")
            Sys_Call_Photo("calc.ods")
        if sys_call == 2:
            send_message("Test the world")
        if sys_call == 7:
            update_json()

Sys_Call_Request()
