# thread class to spin off a new class for every client

import threading

from server.members.Member import Member


class ClientThread(threading.Thread):

    def __init__(self,conn,addr,buffer_size,get_members,add_member):
        super(ClientThread, self).__init__()
        self.socket = conn
        self.client_ip = addr
        self.buffer_size = buffer_size
        self.get_members = get_members
        self.add_member = add_member

    def run(self):
        conn = self.socket
        with conn:
            conn.setblocking(False)
            while True:
                try:
                    buf = ' '
                    while buf[-1] != '\n':
                        msg = conn.recv(self.buffer_size)
                        if not msg:
                            # the client terminated the connection
                            # TODO: Check if this is the correct time to send exit
                            self.send_exit_msg()
                            break;
                        msg = msg.decode("utf-8")
                        buf += msg
                    msg_from_client = buf.strip()
                    self.parse_client_msg(msg_from_client)
                except Exception as e:
                    raise Warning("Unable to receive from: " + self.client_ip)


    def parse_exit_message(self,msg):
        #TODO: Figure out what to do here
        m = msg;

    def parse_helo_message(self,msg):
        member = self.parse_new_member(msg)
        members = self.get_members()
        names = members.keys()
        if member.name in names:
            # the screen_name is already in use
            self.send_reject_message(member)
        else:
            self.add_member(member)
            self.send_accept_message()


    # parse the message from the client
    def parse_client_msg(self,msg_from_client):
        # parse the exit message from the client
        if(msg_from_client == "EXIT\n"):
            self.parse_exit_message(msg_from_client)
        else:
            self.parse_helo_message(msg_from_client)

    # there is already a user with the same name, reject this client
    def send_reject_message(self,member):
        name = member.name
        msg = "RJCT " + name + "\n"
        msg = msg.encode()
        self.socket.send(msg)

    # the client was accepted. send the accept message
    def send_accept_message(self):
        members = self.get_members()
        msg = "ACPT "
        for name,member in members.items():
            ip = member.ip
            port = member.port
            line = name + " " + ip + " " + port + ":"
            msg += line
        # replace the last colon with a new line
        msg = msg[:-1] + '\n'
        msg = msg.encode()
        self.socket.send(msg)

    def send_exit_msg(self):
        msg = "EXIT\n"
        msg = msg.encode()
        self.socket.send(msg)

    def parse_new_member(self,data):
        msg = data.split()
        if len(msg) != 4 or msg[0] != 'HELO':
            raise Warning("received message with incorrect format")
            return
        name = msg[1]
        ip = msg[2]
        port = msg[3]
        member = Member(name,ip,port)
        return member
