#! /usr/bin/python
#--------------------------------#
# Implementation of YaChat server
# EE 382N, Spring 2019
#--------------------------------#import argparse

import argparse
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),  ".."))
from server.welcome import WelcomeSocket

BUFFER_SIZE = 2048

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("welcome_port",type=int)

    args = parser.parse_args()
    welcome_port = args.welcome_port
    # socket listening on the welcome port for new clients
    welcome_socket = WelcomeSocket(welcome_port,BUFFER_SIZE)
    welcome_socket.listen()




if __name__ == "__main__":
    main()

