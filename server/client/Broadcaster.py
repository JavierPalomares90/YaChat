
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
        data = self.msg.encode()
        try:
            for name,member in self.members.items():
                ip = member.ip
                port = member.port
                address = (ip,port)
                s.sendto(data,address)
        except Exception as e:
            raise Warning("unable to broadcast msg" + self.msg)
        finally:
            s.close()


