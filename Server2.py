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
PORT = 5052
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
EMPTY_BYTE = "b'!DISCONNECT'"

client_counter = 0


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client_photo(conn, addr):
    #print(f"[NEW CONNECTION] {addr} connected.")
    print("Hanbdling photo")

    connected = True
    while connected:
        print("[+] in photo while loop")
        msg_length = conn.recv(HEADER)#
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)#
            if msg == DISCONNECT_MESSAGE.encode(FORMAT):
                connected = False
                print(f"[{addr}] Client disconnected")
                #conn.close()
                return 

            print(f"[{addr}] {msg}")
            file = open("calc.ods", "ab")
            file.write(msg)
            conn.send("Msg received".encode(FORMAT))
            file.close()
    conn.close()
    return

def read_json(conn, addr, board_path):
    file_path = os.path.join(board_path, "json.txt")
    with open(file_path) as f:
        #json_metadata = f.readline()
        json_metadata = json.load(f)
        metadata = json.loads(json_metadata)
        print(metadata)
        return metadata
        #json_metadata = json.load(f) ### we dont need thisd here, should go into setup
        sensor_id = metadata['sensor_id']
        location = metadata['location']
        file_type = metadata['file_type']
        print(sensor_id, location, file_type)
        print("[+] Returning from reading from jrw.py")
        print("[++++++++++++++++++++++++++++]")

def recv_local_json(conn, addr, board_path):
    file_path = os.path.join(board_path, "json.txt")
    file = open(file_path, "w") ### I will need a mutex!!!!
    file.close()
    print("Hanbdling file")

    connected = True
    while connected:
        print("[+] in while loop")
        msg_length = conn.recv(HEADER)#
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)#
            if msg == DISCONNECT_MESSAGE.encode(FORMAT):
                connected = False
                print(f"[{addr}] Client disconnected")
                #conn.close()
                return 

            print(f"[{addr}] {msg}")
            file = open(file_path, "ab")
            file.write(msg)
            conn.send("Msg received".encode(FORMAT))
            file.close()
    conn.close()
    return

def handle_client_photo(conn, addr):
    #print(f"[NEW CONNECTION] {addr} connected.")
    print("Hanbdling photo")

    connected = True
    while connected:
        print("[+] in photo while loop")
        msg_length = conn.recv(HEADER)#
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)#
            if msg == DISCONNECT_MESSAGE.encode(FORMAT):
                connected = False
                print(f"[{addr}] Client disconnected")
                #conn.close()
                return 

            print(f"[{addr}] {msg}")
            file = open("calc.ods", "ab")
            file.write(msg)
            conn.send("Msg received".encode(FORMAT))
            file.close()
    conn.close()
    return

def set_and_read_file(conn, addr, board_path, metadata):
    print("@@@@@@@@@@@@@@@@@@@@@@@@")
    print(metadata)
    file_type = metadata['file_type'] # need to append path to it
    path = str(board_path) + str(file_type)
    print("##########################")
    print(file_type)
    file_path = os.path.join(board_path, file_type)
    #file = open(file_path, "w") ### I will need a mutex!!!!
    #recv_message(conn, addr)
    input()

    connected = True
    while connected:
        print("[+] in file tpoye area")
        msg_length = conn.recv(HEADER)#
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)#
            if msg == DISCONNECT_MESSAGE.encode(FORMAT):
                connected = False
                print(f"[{addr}] Client disconnected")
                #conn.close()
                return 

            print(f"[{addr}] {msg}")
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
    print(board_path)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print(f"are we making a directory {dir_name}")
    print(f"We are waiting for the client{id} to send us commands")
    while TRUE:
        send_message("Waiting for a sys call", conn, addr)
        sys_call = recv_message(conn, addr)
        sys_call = int(sys_call)
        #check to see if its a numner, if not a loop

        if sys_call == 1: # getting file
            print(3333)
            print("we are waiting for start")
            input()
            recv_local_json(conn, addr, board_path)
            metadata = read_json(conn, addr, board_path)
            print("!!!!!!!!!!!!!!!!!!!")
            print("we are waiting for adter reciving json")
            input()
            print(metadata)
            print("we are waiting for set and read new file")
            input()
            set_and_read_file(conn, addr, board_path, metadata)

            # grab values
            # set file up and recv file


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
        #print(f"[ACTIVE CONNECTIONS] {idount() - 1}")
        thread.start() 
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()
