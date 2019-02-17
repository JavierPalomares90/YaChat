#! /usr/bin/python
#--------------------------------#
# Implementation of YaChat client for first Iteration
# EE 382N, Spring 2019
#--------------------------------#

import argparse
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),  ".."))
from client.chatter.Chatter import Chatter
from client.receive.ReceiveThread import ReceiveThread
from client.send.SendThread import SendThread

BUFFER_SIZE = 2048
# members in chatroom
chatters = None


def main():
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

    chatter = Chatter(screenName, hostName, tcpPort, BUFFER_SIZE)
    chatter.init_connection()
    receive = ReceiveThread(chatter, BUFFER_SIZE)
    send = SendThread(chatter)

    receive.start()
    send.start()


# main method
if __name__ == "__main__":
    main()





