from socket import *
import sys
import select

HOST = "127.0.0.1"
PORT = 12000

#Ipv4 and TCP
user = socket(AF_INET, SOCK_STREAM)

#send connection 
user.connect((HOST,PORT))

#ack
ack = user.recv(1024).decode("utf-8", errors="replace")  #AI Debug/ special characters
print(ack)

print("Type your messages (type 'exit' to quit):")
print("You>> ", end="", flush=True)  #AI Debug/ prompt

while True:
    #wait untill keyboard or socket is ready
    ready, _, _ = select.select([sys.stdin, user], [], [])

    #a message arrived from the server
    if user in ready:
        servreply = user.recv(1024).decode("utf-8", errors="replace")  #AI Debug/ special characters
        if servreply == "exit" or not servreply :
            print("\r", end="")
            print("Server left the chat.")
            break
        print("\r", end="")
        print(f"Server>>{servreply}")
        print("You>> ", end="", flush=True)

    #the user typed a line
    if sys.stdin in ready:
        line = sys.stdin.readline()
        if line == "":
            break
        client_keyboard = line.strip()
        if not client_keyboard:
            print("You>> ", end="", flush=True)
            continue
        user.send(client_keyboard.encode("utf-8", errors="replace"))  #AI Debug/ special characters
        if client_keyboard == "exit":
            break
        print("You>> ", end="", flush=True)

user.close()