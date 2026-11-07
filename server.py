import sys
import select
import json
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

#variable sockets clients names groups
sockets_list = [server, sys.stdin]
clients = {}
names = {}

#groups and set of numbers
groups = {}
def send_json(s, d):
    s.send((json.dumps(d) + "\n").encode("utf-8", errors="replace"))

print("Type a message to send it to all clients (type 'exit' to stop the server):")
print("You>> ", end="", flush=True)

running = True
while running:
    ready, _, _ = select.select(sockets_list, [], [])

    for sock in ready:

        #new client
        if sock is server:
            conn, addr = server.accept()
            username=conn.recv(1024).decode("utf-8", errors="replace")
            names[username.lower()] = conn #stock usernames
            sockets_list.append(conn)
            clients[conn] = username
            
            #waiting notification
            if len(names) == 1:
                conn.send("Connected to ClassChat\nWaiting for other users...".encode())
            else:
                conn.send("Connected to ClassChat".encode())
                for c in clients:
                    if c is not conn:
                        info = {"status": "info", "sender": "Server", "receiver": clients[c], "text": f"{username} joined the chat"}
                        c.send((json.dumps(info) + "\n").encode("utf-8", errors="replace"))

            print("\r", end="")
            print(f"{username} is connected")
            print("You>> ", end="", flush=True)

        #server send to every clients
        elif sock is sys.stdin:
            line = sys.stdin.readline()
            if line == "":  #AI Debug/ window closed
                running = False
                break
            server_keyboard = line.strip()
            if not server_keyboard:
                print("You>> ", end="", flush=True)
                continue
            if server_keyboard == "exit":
                running = False
                break
            for c in clients:
                c.send(server_keyboard.encode("utf-8", errors="replace"))  #AI Debug/ special characters
            print("You>> ", end="", flush=True)

        #client sent a message or left
        else:
            try:
                usermessage = sock.recv(1024).decode("utf-8", errors="replace")  #AI Debug/ special characters
            except ConnectionResetError:
                usermessage = ""
            print("\r", end="")
            if usermessage == "exit" or not usermessage:
                print(f"{clients[sock]} left the chat.")
                sockets_list.remove(sock)
                del names[clients[sock].lower()]
                del clients[sock]
                sock.close()
            else:
                #one JSON message per line
                for msg in usermessage.split("\n"):
                    if not msg:
                        continue
                    try:
                        msg = json.loads(msg)
                    except ValueError:
                        continue

                    #Create a group
                    if msg["status"] == "create":
                        group = msg["receiver"].lower()
                        members = {m.lower().lstrip("@") for m in msg["text"].split()}
                        members.add(msg["sender"].lower())
                        
                        #AI Debug/ group chat: every member must be online
                        unknown = [m for m in members if m not in names]
                        if unknown:
                            send_json(sock, {"status": "error", "sender": "Server", "receiver": msg["sender"], "text": f"{', '.join(unknown)} not online, group not created"})
                            continue
                        
                        groups[group] = members
                        for m in members:
                            if m in names:
                                send_json(names[m], {"status": "info", "sender": "Server", "receiver": m, "text": f"{msg['sender']} created group #{group} with {', '.join(sorted(members))}"})
                        print(f"{msg['sender']} created group #{group}: {', '.join(sorted(members))}")
                        continue

                    #Message to a group
                    if msg["status"] == "group":
                        group = msg["receiver"].lower()
                        if group not in groups:
                            send_json(sock, {"status": "error", "sender": "Server", "receiver": msg["sender"], "text": f"group #{group} does not exist"})
                        elif msg["sender"].lower() not in groups[group]:
                            send_json(sock, {"status": "error", "sender": "Server", "receiver": msg["sender"], "text": f"you are not in group #{group}"})
                        else:
                            for m in groups[group]:
                                if m in names and m != msg["sender"].lower():
                                    send_json(names[m], msg)
                            print(f"{msg['sender']} -> #{group}: {msg['text']}")
                        continue

                    receiver = msg["receiver"]

                    if receiver.lower() in names:
                        names[receiver.lower()].send((json.dumps(msg) + "\n").encode("utf-8", errors="replace")) #AI Debug/ json format and errors
                        print(f"{msg['sender']} -> {receiver}: {msg['text']}")
                    else:
                        error = {"status": "error", "sender": "Server", "receiver": msg["sender"], "text": f"{receiver} is not online"}
                        sock.send((json.dumps(error) + "\n").encode("utf-8", errors="replace"))
                        print(f"{msg['sender']} -> {receiver}: not online")
            print("You>> ", end="", flush=True)


#every client is leaving
for c in clients:
    c.send("exit".encode())
    c.close()
server.close()
print("\nServer stopped.")