#!/usr/bin/python3

#from asyncio.windows_events import NULL
#from pickle import FALSE, TRUE
#from ctypes.wintypes import BYTE
from pickle import TRUE
import socket
#import sys 
import threading
import subprocess
import json
import os

HEADER = 64
PORT = 5053
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
EMPTY_BYTE = "b'!DISCONNECT'"

client_counter = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def read_json(conn, addr, board_path):
    file_path = os.path.join(board_path, "json.txt")
    with open(file_path) as f:
        json_metadata = json.load(f)
        metadata = json_metadata
        return metadata

def recv_local_json(conn, addr, board_path):
    file_path = os.path.join(board_path, "json.txt")
    file = open(file_path, "w") ### I will need a mutex!!!!
    file.close()

    connected = True
    while connected:
        msg_length = conn.recv(HEADER)#
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)#
            if msg == DISCONNECT_MESSAGE.encode(FORMAT):
                connected = False
                print(f"[{addr}] file recived")
                return 
            file = open(file_path, "ab")
            file.write(msg)
            conn.send("Msg received".encode(FORMAT))
            file.close()
    conn.close()
    return

def handle_client_file(conn, addr, file_path):
    connected = True
    while connected:
        msg_length = conn.recv(HEADER)#
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)#
            if msg == DISCONNECT_MESSAGE.encode(FORMAT):
                connected = False
                print(f"[{addr}] file recived")
                return 
            file = open(file_path, "ab")
            file.write(msg)
            conn.send("Msg received".encode(FORMAT))
            file.close()
    conn.close()
    return

def set_and_read_file(conn, addr, board_path, metadata):
    file_type = metadata['file_type'] # need to append path to it
    print(file_type)
    path = str(board_path) + str(file_type)
    file_path = os.path.join(board_path, file_type)
    handle_client_file(conn, addr, file_path)

    connected = True
    while connected:
        msg_length = conn.recv(HEADER)#
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)#
            if msg == DISCONNECT_MESSAGE.encode(FORMAT):
                connected = False
                print(f"[{addr}] file recived")
                return 
            file = open(file_path, "ab")
            file.write(msg)
            conn.send("Msg received".encode(FORMAT))
            file.close()
    conn.close()
    return

def handling_client(conn, addr, id): # this whole thing in a while loop
    dir_name = "mainboard" + str(id)
    generic_file_path = "/home/david/Desktop/Backend/"
    board_path = str(generic_file_path) + (dir_name) # board specific path

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print(f"are we making a directory {dir_name}")

    print(f"We are waiting for the client{id} to send us commands")
    while TRUE:
        send_message("Waiting for a sys call", conn, addr)
        sys_call = recv_message(conn, addr)
        sys_call = int(sys_call)

        if sys_call == 1: # getting file
            recv_local_json(conn, addr, board_path)
            metadata = read_json(conn, addr, board_path)
            set_and_read_file(conn, addr, board_path, metadata)
        if sys_call == 2:
            recv_message(conn, addr)

def send_message(msg, conn, addr): #no need fot addr
    conn.send(msg.encode(FORMAT))
    print(f"[{addr}] {msg}")

def recv_message(conn, addr):
    print("[+] Recieving message", end='')
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
         msg_length = int(msg_length)
         msg = conn.recv(msg_length).decode(FORMAT)
         if msg == DISCONNECT_MESSAGE:
            connected = False

         print(f"[{addr}] {msg}")
    return msg

def start():
    id = 0
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        id =+ 1
        conn, addr = server.accept() #waits for a connection and this is where I should do the nnummber thing  
        thread = threading.Thread(target=handling_client, args=(conn, addr, threading.active_count() - 1))
        thread.start() 
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()
