
import socket
import sys


class WelcomeSocket:

    def __init__(self, port, buffer_size):
        self.buffer_size = buffer_size
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

    def listen(self):
        self.tcp_socket.listen()
        conn, addr = self.tcp_socket.accept()
        with conn:
            while True:
                try:
                    buf = ' '
                    while buf[-1] != '\n':
                        msg = conn.recv(self.buffer_size)
                        msg = msg.decode("utf-8")
                        buf += msg
                    msg_from_client = buf.strip()
                    return msg_from_client
                except Exception as e:
                    raise Warning("Unable to receive from: " + addr)

    def parse_helo(self,data):
        d = data


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


