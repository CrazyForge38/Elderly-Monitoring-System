#!/usr/bin/python3

from pickle import TRUE
import socket 
import threading

HEADER = 64
PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client_photo(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            file = open("try.jpg", "ab")
            file.write(msg)
            conn.send("Msg received".encode(FORMAT))

            file.close()
    conn.close()
        
def handle_client_message(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()

def connection_test(conn, addr):
    client_counter = 0
    new_client_id = client_counter
    send_message(new_client_id, conn)#no need for addr
    msg = recv_message(conn, addr)
    if msg == client_counter:
        send_message(TRUE)
        client_counter += 1
        handling_client(conn, addr, new_client_id)

def handling_client(conn, addr,client_id): # this whole thing in a while loop
    print("We are waiting for the client to send us commands")
    sys_call = recv_message(conn, addr)

    #check to see if its a numner, if not a loop

    match sys_call:
        case 0:
            print(1)
        case 0:
            print(1)
        case 0:
            print(1)
        case 0:
            print("wrong")

def send_message(msg, conn): #no need fot addr
    conn.send(msg.encode(FORMAT))
    print("# Sent: {msg}")

def recv_message(conn, addr):
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
        conn, addr = server.accept() #waits for a connection
        thread = threading.Thread(target=connection_test, args=(conn, addr))
        thread.start() 
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
