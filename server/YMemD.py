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
from server.Server import Server

BUFFER_SIZE = 2048
# dictionary to hold all of the members
members = {}



def parse_msg(data):
    msg = data.split()
    if len(msg) != 4 or msg[0] != 'HELO':
        raise Warning("received message with incorrect format")
        return
    name = msg[1]
    ip = msg[2]
    port = msg[3]
    member = Member(name,ip,port)
    return member


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("welcome_port", type=int)

    args = parser.parse_args()
    welcome_port = args.welcome_port
    server = Server(welcome_port)
    server.start()




if __name__ == "__main__":
    main()

