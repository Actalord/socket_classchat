from socket import *

PORT = 12000
HOST = ""

#Ipv4 and TCP
server = socket(AF_INET, SOCK_STREAM)

#AI help debug n1
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

#loop if the user type 'exit' or close the cmd
while True:
    usermessage = conn.recv(1024).decode()
    if usermessage == "exit" or not usermessage :
        break
    print(f"Client>>{usermessage}")
    reply = input("Server>>")
    conn.send(reply.encode())

conn.close()
server.close()