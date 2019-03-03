#! /usr/bin/python
#--------------------------------#
# Implementation of YaChat server
# EE 382N, Spring 2019
#--------------------------------#import argparse

import argparse
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),  ".."))
from server.members.Member import Member
from server.welcome.WelcomeSocket import WelcomeSocket

BUFFER_SIZE = 2048
'HELO javier 192.168.86.229 57479'
# dictionary to hold all of the members
members = {}

def accept_member(member):
    name = member.name
    namesInServer = members.keys()
    if list(namesInServer).

def parse_helo(data):
    msg = data.split()
    if len(msg) != 4 or msg[0] != 'HELO':
        raise Warning("received message with incorrect format")
        return
    name = msg[1]
    ip = msg[2]
    port = msg[3]
    member = Member(name,ip,port)
    accept_member(member)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("welcome_port", type=int)

    args = parser.parse_args()
    welcome_port = args.welcome_port
    # socket listening on the welcome port for new clients
    welcome_socket = WelcomeSocket(welcome_port,BUFFER_SIZE)
    data = welcome_socket.listen()
    parse_helo(data)




if __name__ == "__main__":
    main()

