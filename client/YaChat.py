#! /usr/bin/python
#--------------------------------#
# Implementation of YaChat client for first Iteration
# EE 382N, Spring 2019
#--------------------------------#
# TODO: Add requirements file

import argparse
parser = argparse.ArgumentParser()
parser.parse_args()






# main method
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("screen_name", help="Your screen name")
    parser.add_argument("host_name", help="The server's hostname")
    parser.add_argument("tcp_port", help="The server's welcome tcp port")

    args = parser.parse_args()
    screen_name = args.screen_name
    host_name = args.host_name
    tcp_port = args.tcp_port


