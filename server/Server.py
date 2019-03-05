import threading

from server.client.Broadcaster import Broadcaster
from server.client.ClientThread import ClientThread
from server.welcome.WelcomeSocket import WelcomeSocket


class Server:
    BUFFER_SIZE = 2048

    def __init__(self,welcome_port):
        self.port = welcome_port
        # dictionary to hold all of the members
        self.members = {}
        self.members_lock = threading.Lock()
        #TODO: should welcome socket be blocking = false
        self.welcome_socket = WelcomeSocket(welcome_port)

    def start(self):
        while True:
            try:
                conn,addr = self.welcome_socket.accept()
                # get a new thread to connect with the client
                clientThread = ClientThread(conn, addr, Server.BUFFER_SIZE, self.get_members,self.add_member,self.remove_member)
                clientThread.start()
            except Exception as e:
                # Close the connections
                conn.close()
                self.welcome_socket.close()
                exit(1)

    def remove_member(self,name):
        self.members_lock.acquire()
        try:
            self.members.pop(name)
        except KeyError as e:
            # the key did not exist in the dictionary
            raise Warning("{} asked to leave, but was not part of members list".format(name))
        self.members_lock.release()
        self.broadcast_exit_msg(name)

    def broadcast_msg(self,msg):
        broadcaster = Broadcaster(msg,self.get_members())
        broadcaster.start()

    # inform all the chatters that someone new joined
    def broadcast_join_msg(self, member):
        name = member.name
        ip = member.ip
        port = member.port
        msg = "JOIN " + name + " " + ip + " " + str(port) + "\n"
        self.broadcast_msg(msg)

    # inform all the chatters that someone left
    def broadcast_exit_msg(self, name):
        msg = "EXIT " + name + "\n"
        self.broadcast_msg(msg)

    def add_member(self,member):
        self.members_lock.acquire()
        name = member.name
        self.members[name] = member
        self.members_lock.release()
        self.broadcast_join_msg(member)

    def get_members(self):
        self.members_lock.acquire()
        members = self.members
        self.members_lock.release()
        return members


