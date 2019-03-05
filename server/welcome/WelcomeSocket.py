
import socket
import sys


class WelcomeSocket:

    def __init__(self, port):
        self.ip_address = self.get_ip_address()
        self.port = port
        self.tcp_socket = self.get_tcp_socket()

    def get_tcp_socket(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        address = (self.ip_address,self.port)
        try:
            s.bind(address)
        except Exception as e:
            raise Exception("Unable to start welcome socket at port {}".format(self.tcp_port))
        return s

    def accept(self):
        self.tcp_socket.listen()
        conn, addr = self.tcp_socket.accept()
        return conn,addr

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
            return ip_address
        except Exception as e:
            # Unable to get WLAN ip address. Try over loopback
            ip_address = socket.gethostbyname(self.client_hostname)
            return ip_address
        return None


    def send_accept_message(self, members):
        msg = "ACPT "
        for member in members:
            name = member.name
            ip = member.ip
            port = member.port
            line = name + " " + ip + " " + port + ":"
            msg += line
        # replace the last colon with a new line
        msg = msg[:-1] + '\n'
        msg = msg.encode()
        self.tcp_socket.send(msg)
