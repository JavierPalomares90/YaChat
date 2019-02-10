import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = input("Port to connect to: ")
server_address = ('localhost', port)
msg = raw_input("Type message: ")

try:

    # Send data
    print >>sys.stderr, 'sending "%s"' % msg
    sent = sock.sendto(msg, server_address)

    # Receive response
    print >>sys.stderr, 'waiting to receive'
    data, server = sock.recvfrom(4096)
    print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()