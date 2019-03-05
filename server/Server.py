import threading

from server.listen.ClientThread import ClientThread
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
        #TODO: should welcome socket be blocking = false
        self.welcome_socket = WelcomeSocket(welcome_port)

    def start(self):
        conn,addr = self.welcome_socket.accept()
        # get a new thread to connect with the client
        clientThread = ClientThread(conn, addr, Server.BUFFER_SIZE, self.get_members,self.add_member)
        clientThread.start()

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


