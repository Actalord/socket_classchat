import sys
import select
from socket import *

PORT = 12000
HOST = ""

#Ipv4 and TCP
server = socket(AF_INET, SOCK_STREAM)

#AI Debug/ ReuseAddr
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind((HOST, PORT))

#server listening (up to 5 clients waiting)
server.listen(5)
print(f"Server is listening on port {PORT}")

#client socket -> client address
sockets_list = [server, sys.stdin]
clients = {}

print("Type a message to send it to all clients (type 'exit' to stop the server):")
print("You>> ", end="", flush=True)  #AI Debug/ prompt

running = True  #AI Debug/ used to leave both loops on 'exit'
while running:
    ready, _, _ = select.select(sockets_list, [], [])

    for sock in ready:

        #new client
        if sock is server:
            conn, addr = server.accept()
            sockets_list.append(conn)
            clients[conn] = addr
            conn.send("Connected to ClassChat".encode())
            print("\r", end="")  #AI Debug/ prompt
            print(f"{addr} is connected")
            print("You>> ", end="", flush=True)  #AI Debug/ prompt

        #server send to every clients
        elif sock is sys.stdin:
            line = sys.stdin.readline()
            if line == "":  #AI Debug/ window closed
                running = False
                break
            server_keyboard = line.strip()
            if not server_keyboard:
                print("You>> ", end="", flush=True)  #AI Debug/ prompt
                continue
            if server_keyboard == "exit":
                running = False
                break
            for c in clients:
                c.send(server_keyboard.encode("utf-8", errors="replace"))  #AI Debug/ special characters
            print("You>> ", end="", flush=True)  #AI Debug/ prompt

        #client sent a message or left
        else:
            try:
                usermessage = sock.recv(1024).decode("utf-8", errors="replace")  #AI Debug/ special characters
            except ConnectionResetError:
                usermessage = ""
            print("\r", end="")  #AI Debug/ prompt
            if usermessage == "exit" or not usermessage:
                print(f"{clients[sock]} left the chat.")
                sockets_list.remove(sock)
                del clients[sock]
                sock.close()
            else:
                print(f"{clients[sock]}>>{usermessage}")
            print("You>> ", end="", flush=True)  #AI Debug/ prompt


#every client is leaving
for c in clients:
    c.send("exit".encode())
    c.close()
server.close()
print("\nServer stopped.")