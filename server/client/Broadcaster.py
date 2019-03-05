
import socket
import threading


class Broadcaster(threading.Thread):

    def __init__(self,msg,members):
        super(Broadcaster, self).__init__()
        self.msg = msg
        self.members = members

    def run(self):
        # send the message to all of the members
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for name,member in self.members:
            ip = member.ip
            port = member.port
            address = (ip,port)
            s.sendto(self.msg.encode(),address)
        s.close()


