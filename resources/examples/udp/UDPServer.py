import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
port = input("Port to create server on: ")
server_address = ('localhost', port)
sock.bind(server_address)
#Messages are read from the socket using recvfrom(), which returns the data as well as the address of the client from which it was sent.

while True:
    data, address = sock.recvfrom(4096)
    if data:
        sent = sock.sendto(data.upper(), address)
        print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)