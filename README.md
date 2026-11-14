# ClassChat

A command-line chat application in Python using TCP sockets.
A central server relays messages between clients: private messages, group chats and server broadcasts.

## Requirements

- Python 3 (standard library only, nothing to install)
- Linux, macOS or WSL

> [!WARNING]
> **On Windows, you must run ClassChat inside WSL (Windows Subsystem for Linux).**
> It does not work in a native Windows terminal (cmd or PowerShell), because the client and server use `select()` on the keyboard, which Windows does not support.

## Files

- `server.py` : the ClassChat server
- `client.py` : the ClassChat client

## How to run

1. Start the server first:

   ```bash
   python3 server.py
   ```

   The server listens on port 12000.

2. In another terminal, start a client and enter your name:

   ```bash
   python3 client.py
   ```

   ```text
   Your name: User1
   ```

3. Repeat step 2 in other terminals to connect more clients (User2, User3...).

By default the client connects to `127.0.0.1` (same machine).
To connect from another machine, change `HOST` in `client.py` to the server's IP address.

## How to use

| Command | Effect |
|---|---|
| `@<name> <message>` | Send a private message to a user (names are not case-sensitive) |
| `/create <group> @<member1> @<member2> ...` | Create a group; the creator is added automatically, and all members must be online |
| `#<group> <message>` | Send a message to every member of a group |
| `exit` | Leave the chat |

On the server side, any line typed in the server terminal is sent to all connected clients, and `exit` stops the server.

## Examples

```text
@User2 Hello
/create friends @User2 @User3
#friends Hello everyone
```

The server answers with an error if:
- the receiver is not online;
- the group does not exist, or the sender is not a member of it;
- a group member is not online when the group is created.

## Message format

Client-to-client messages are sent as JSON, one message per line:

```json
{"status": "message", "sender": "User1", "receiver": "User2", "text": "Hello"}
```
