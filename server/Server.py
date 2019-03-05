import threading

from server.members.Member import Member
from server.welcome.WelcomeSocket import WelcomeSocket


class Server:
    BUFFER_SIZE = 2048
    # dictionary to hold all of the members

    @staticmethod
    def parse_new_member(data):
        msg = data.split()
        if len(msg) != 4 or msg[0] != 'HELO':
            raise Warning("received message with incorrect format")
            return
        name = msg[1]
        ip = msg[2]
        port = msg[3]
        member = Member(name,ip,port)
        return member

    def __init__(self,welcome_port):
        self.port = welcome_port
        self.members = {}
        self.members_lock = threading.Lock()
        self.welcome_socket = WelcomeSocket(welcome_port,Server.BUFFER_SIZE)

    def start(self):
        msg = self.welcome_socket.accept()
        member = Server.parse_new_member(msg)
        namesInServer = self.get_members()
        if member.name in namesInServer:
            # the screen_name is already in use
            self.welcome_socket.send_reject_message(member)
        else:
            # add the member to the list and send the accept message
            self.add_member(member)
            self.welcome_socket.send_accept_message(self.members)

    def add_member(self,member):
        self.members_lock.acquire()
        name = member.name
        self.members[name] = member
        self.members_lock.release()

    def get_members(self):
        self.members_lock.acquire()
        names = self.members.keys()
        self.members_lock.release()
        return names


