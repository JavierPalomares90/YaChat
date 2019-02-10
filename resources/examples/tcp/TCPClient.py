import socket
import sys

# create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# now connect to the web server on port 80 - the normal http port
port = input("Port to connect to: ")
s.connect(("127.0.0.1", port))
msg = raw_input("Type message: ")
s.send(msg)
msgFromServer = s.recv(2048)

print("FROM SERVER: "+msgFromServer)