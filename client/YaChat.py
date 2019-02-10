#! /usr/bin/python
#--------------------------------#
# Implementation of YaChat client for first Iteration
# EE 382N, Spring 2019
#--------------------------------#

import argparse
import socket
import time

BUFFER_SIZE = 2048
# members in chatroom
chatters = None


# returns a tcp socket at the given host and port
def get_tcp_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if s:
        try:
            server_address = (host, port)
            s.connect(server_address)
        except Exception as e:
            print(e)
            raise e
    return s


def get_udp_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to a port
    server_address = (host, port)
    if sock:
        try:
            sock.bind(server_address)
        except Exception as e:
            print(e)
            raise e
    return sock


def get_ip_address():
    # TODO: Fix implemenation
    return "127.0.1.1"


def get_helo_msg(screen_name, udp_port):
    msg = "HELO "
    msg += screen_name
    msg += " "
    ip_address = get_ip_address()
    msg += ip_address
    msg += " "
    msg += str(udp_port)
    msg +="\n"
    return msg


def populate_chatroom(msg):
    # Trim the "ACPT " form the message
    msg = msg[5:]
    # split the string on ":"
    records = msg.split(':')
    for i in range(len(records)):
        # split the records by whitespace
        values = records[i].split(' ')
        name = values[0]
        ip = values[1]
        port = values[2]



def parse_server_response(msg):
    # the server accepted us
    if(msg.find("ACPT ") != -1):
        populate_chatroom(msg)
    # the server rejected us
    elif(msg.find("RJCT ") != -1):
        raise Exception("Client is rejected. Username already exists in chatroom")
    else:
        raise Exception("Error: Wrong format for response")


# Initialize the connection with the server
def init_connection(screen_name, host_name, tcp_port):
    # create a tcp socket to connect to the server
    tcp_socket = get_tcp_socket(host_name, tcp_port)
    if not tcp_socket:
        raise Exception("Unable to initialize tcp connection with server at {}:{}".format(host_name,tcp_port))
    # create a udp socket to listen for messages.
    # Pass in 0 as the port to let the OS pick the port
    udp_socket = get_udp_socket(host_name, 0)
    if not udp_socket:
        raise Exception("Unable to initialize udp connection with server at {}".format(host_name))

    # Get the HELO msg to send to the server
    helo_msg = get_helo_msg(screen_name, udp_socket.getsockname()[1])

    if helo_msg:
        try:
            tcp_socket.send(helo_msg.encode())
        except Exception as e:
            print(e)
            raise(e)
    # TODO: Getting partial response from the server.
    # Sleeping to avoid this. Need to figure out how to correct this
    time.sleep(1)
    msg_from_server = tcp_socket.recv(BUFFER_SIZE)
    print(msg_from_server)
    parse_server_response(msg_from_server)
    tcp_socket.close()



# main method
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("screen_name", help="Your screen name")
    parser.add_argument("host_name", help="The server's hostname")
    parser.add_argument("tcp_port", help="The server's welcome tcp port",type=int)

    # parse the arguments
    args = parser.parse_args()
    # remove whitespace from screen name
    screenName = args.screen_name.strip()
    hostName = args.host_name
    tcpPort = args.tcp_port

    # Initialize the connection
    init_connection(screenName,hostName,tcpPort)


