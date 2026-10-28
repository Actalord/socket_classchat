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

#server listening (max 1 user)
server.listen(1)
print(f"Server is listening on port {PORT}")

#accepting connection
conn, addr = server.accept()
print(f"{addr} is connected")

#ack
conn.send("Connected to ClassChat".encode())

print("Type your messages (type 'exit' to quit):")
print("You>> ", end="", flush=True)  #AI Debug/ prompt


while True:
    #wait untill keyboard or socket is ready
    ready, _, _ = select.select([sys.stdin, conn], [], [])

    #a message arrived from the client 
    if conn in ready :
        usermessage = conn.recv(1024).decode("utf-8", errors="replace")  #AI Debug/ special characters
        if usermessage == "exit" or not usermessage:
            print("\r", end="")  #AI Debug/ prompt
            print("Client left the chat.")
            break
        print("\r", end="")
        print(f"Client>>{usermessage}")
        print("You>> ", end="", flush=True)

    #the server typed a line
    if sys.stdin in ready :
        line = sys.stdin.readline()
        if line == "":
            break
        server_keyboard = line.strip()
        if not server_keyboard:
            print("You>> ", end="", flush=True)
            continue
        conn.send(server_keyboard.encode("utf-8", errors="replace"))  #AI Debug/ special characters
        if server_keyboard == "exit":
            break
        print("You>> ", end="", flush=True)

conn.close()
server.close()