import socket
import sys

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
port = input("Port to create server on: ")
serversocket.bind(("127.0.0.1", port))
# become a server socket
serversocket.listen(5)

while True:
    # accept connections from outside
    (clientsocket, address) = serversocket.accept()
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
    msg = clientsocket.recv(2048)
    print("Received from Client: "+msg)
    capitalized = msg.upper()
    clientsocket.send(capitalized)
    clientsocket.close()