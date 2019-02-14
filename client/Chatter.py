## Chatter class

import socket


class Chatter:


    def __init__(self, screen_name, host_name, tcp_port,buffer_size):
        self.screen_name = screen_name
        self.host_name = host_name
        self.tcp_port = tcp_port
        self.tcp_socket = self.get_tcp_socket()
        self.udp_socket, self.udp_port = self.get_udp_socket()
        self.peers = {}
        self.BUFFER_SIZE = buffer_size

    def __del__(self):
        if self.tcp_socket:
            self.tcp_socket.close()
        if self.udp_socket:
            self.udp_socket.close()

    def get_tcp_socket(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = (self.host_name, self.tcp_port)
        sock.connect(server_address)
        return sock

    def get_udp_socket(self, port=0):
        # port=0 tells the OS to pick a port
        # Create a UDP/IP socket -> DGRAM
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket to a port of OS's choosing
        server_address = (self.host_name, port)
        sock.bind(server_address)
        # To find what port the OS picked, call getsockname()
        return sock, sock.getsockname()[1]

    def get_ip_address(self):
        # TODO: Fix this
        # socket.gethostbyname(udp_socket.gethostname())
        return "127.0.1.1"

    def get_msg_helo(self):
        ip_address = self.get_ip_address()
        msg = "HELO "
        msg += self.screen_name
        msg += " "
        msg += ip_address
        msg += " "
        msg += str(self.udp_port)
        msg +="\n"
        return msg

    def parse_acpt_response(self, msg):
        msg = msg[5:].replace('\n', '')
        records = msg.split(':')
        for record in records:
            name, ip, port = record.split(' ')
            self.peers[name] = (ip, int(port))
            if name != self.screen_name:
                print("{} is in the chatroom".format(name))

    def parse_server_response_helo(self, msg):
        # the server accepted us
        if msg.find("ACPT ") != -1:
            self.parse_acpt_response(msg)
        # the server rejected us
        elif msg.find("RJCT ") != -1:
            raise Exception("Client is rejected. Username already exists in chatroom")
        else:
            raise Exception("Error: Wrong format for response")

    def parse_server_acpt(self, msg):
        msg = msg[5:].replace('\n', '')
        records = msg.split(':')
        for record in records:
            name, ip, port = record.split(' ')
            self.peers[name] = (ip, int(port))
            if name != self.screen_name:
                print("{} is in the chatroom".format(name))

    def parse_server_join(self, msg):
        msg = msg[5:].replace('\n', '')
        name, ip, port = msg.split(' ')
        if name == self.screen_name:
            print("{} accepted to the chatroom".format(name))
        if name not in self.peers:
            self.peers[name] = (ip, int(port))

    def parse_server_exit(self, msg):
        name = msg[5:].replace('\n', '')
        print("{} has left the chatroom".format(name))
        self.peers.pop(name, None)

    def init_connection(self):
        # create a tcp socket to connect to the server
        tcp_socket = self.tcp_socket
        if not tcp_socket:
            raise Exception("Unable to initialize tcp connection with server at {}:{}".format(self.host_name,self.tcp_port))
        # create a udp socket to listen for messages.
        # Pass in 0 as the port to let the OS pick the port
        udp_socket = self.udp_socket
        if not udp_socket:
            raise Exception("Unable to initialize udp connection with server at {}".format(self.host_name))

        # Get the HELO msg to send to the server
        helo_msg = self.get_msg_helo()
        if helo_msg:
            try:
                tcp_socket.send(helo_msg.encode())
                # To fix getting partial response from the server.
                msgAdd = ' '
                while msgAdd[-1] != '\n':
                    msg = tcp_socket.recv(self.BUFFER_SIZE)
                    msg = msg.decode("utf-8")
                    msgAdd += msg
                msg_from_server = msgAdd.strip()
                self.parse_server_response_helo(msg_from_server)
            except Exception as e:
                print(e)
                raise(e)
        else:
            tcp_socket.close()

    #@staticmethod
    def parse__msg(msg):
        #TODO: Check format of MSG. May need to get chatter's name
        print(msg[5:])

    def get_input(self):
        msg = input(self.screen_name + ": ")
        return "MESG " + self.screen_name + ": " + msg + "\n"
        # TODO how to let user Ctrl+C to exit the chat?
        # handle emit EXIT message and can keep use that terminal?

    # send a message to all chatters
    def send_to_all(self, msg):
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = msg.encode()
        try:
            for name in self.peers:
                server_address = self.peers[name]
                sock.sendto(data, server_address)
        except Exception as e:
            print("Unable to send message")
            print(e)
        finally:
            sock.close()

