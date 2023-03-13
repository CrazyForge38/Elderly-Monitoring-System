#!/usr/bin/python3

#from asyncio.windows_events import NULL
#from pickle import FALSE, TRUE
from ctypes.wintypes import BYTE
from pickle import TRUE
import socket
#import sys 
import threading

HEADER = 64
PORT = 5051
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


def handling_client(conn, addr): # this whole thing in a while loop
    print("We are waiting for the client to send us commands")
    while TRUE:
        send_message("Waiting for a sys call", conn, addr)
        sys_call = recv_message(conn, addr)
        sys_call = int(sys_call)
        #check to see if its a numner, if not a loop

        if sys_call == 1:
            print(f"[{addr}] sys_call1: {sys_call}")
            handle_client_photo(conn, addr)
        if sys_call == 2:
            print(f"[{addr}] sys_call2: {sys_call}")
            recv_message(conn, addr)
        if sys_call == 3:
            print(f"[{addr}] sys_call3: {sys_call}")
        if sys_call == 4:
            print("wrong")


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
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept() #waits for a connection and this is where I should do the nnummber thing  
        thread = threading.Thread(target=handling_client, args=(conn, addr))
        thread.start() 
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
