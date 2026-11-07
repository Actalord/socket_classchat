from socket import *
import sys
import select
import json

HOST = "127.0.0.1"
PORT = 12000

#Ipv4 and TCP
user = socket(AF_INET, SOCK_STREAM)

#send connection 
user.connect((HOST,PORT))
username = input("Your name: ")
user.send(username.encode()) #send the username to the client

#ack
ack = user.recv(1024).decode("utf-8", errors="replace")  #AI Debug/ special characters
print(ack)

print("Type your messages (type 'exit' to quit):")
print("Format: @<name> <message>")
print("You>> ", end="", flush=True)

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
        
        for msg_line in servreply.split("\n"):
            if not msg_line:
                continue
            try:
                msg = json.loads(msg_line)
            except ValueError:
                print(f"Server>>{msg_line}")
                continue
            if msg["status"] == "error":
                print(f"Error>>{msg['text']}")
            else:
                print(f"{msg['sender']}>>{msg['text']}")
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
        if client_keyboard == "exit":
            user.send(client_keyboard.encode("utf-8", errors="replace"))  #AI Debug/ special characters
            break
        
        #JSON format 
        parts = client_keyboard.split(" ", 1)
        if len(parts) < 2 or not parts[0].startswith("@"):
            print("Format: @<name> <message>")
            print("You>> ", end="", flush=True)
            continue

        msg = {"status": "message", "sender": username, "receiver": parts[0][1:], "text": parts[1]}
        user.send((json.dumps(msg) + "\n").encode("utf-8", errors="replace")) #AI Debug/ JSON format and errors
        print("You>> ", end="", flush=True)

user.close()