from socket import *

HOST = "127.0.0.1"
PORT = 12000

#Ipv4 and TCP
user = socket(AF_INET, SOCK_STREAM)

#send connection 
user.connect((HOST,PORT))

#ack
ack = user.recv(1024).decode()
print(ack)

#loop if the user type 'exit' or the serv close the cmd
while True:
    usermessage = input("Client>>")
    user.send(usermessage.encode())
    if usermessage == "exit":
        break
    servreply = user.recv(1024).decode()
    if not servreply:
        break
    print(f"Server>>{servreply}")

user.close()