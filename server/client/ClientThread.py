# thread class to spin off a new class for every client

import threading

from server.members.Member import Member


class ClientThread(threading.Thread):

    def __init__(self,conn,addr,buffer_size,get_members,add_member,remove_member):
        super(ClientThread, self).__init__()
        self.client_name = None
        self.socket = conn
        self.client_ip = addr[0]
        self.client_port = addr[1]
        self.buffer_size = buffer_size
        self.get_members = get_members
        self.add_member = add_member
        self.remove_member = remove_member
        self.shutdown = False

    def run(self):
        conn = self.socket
        with conn:
            while self.shutdown == False:
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
                except Exception as e:
                    raise Warning("Unable to receive from: " + self.client_ip)
                    print(e)
                self.parse_client_msg(msg_from_client)


    def parse_exit_message(self,msg):
        self.send_exit_msg()

    def parse_helo_message(self,msg):
        try:
            member = self.parse_new_member(msg)
        except Exception as e:
            # unable to parse the member, reject him
            self.socket.send("RJCT \n")
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
        if len(msg_from_client) < 4:
            raise Warning("received invalid message from client:{}".format(str(msg_from_client)))
            return
        if(msg_from_client == "EXIT"):
            self.parse_exit_message(msg_from_client)
        elif(msg_from_client[:4] == 'HELO'):
            self.parse_helo_message(msg_from_client)
        else:
            raise Warning("received invalid message from client:{}".format(str(msg_from_client)))
            return

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
            line = name + " " + ip + " " + str(port) + ":"
            msg += line
        # replace the last colon with a new line
        msg = msg[:-1] + '\n'
        msg = msg.encode()
        self.socket.send(msg)

    def send_exit_msg(self):
        if self.client_name:
            # the client left the chat
            self.remove_member(self.client_name)
            # have the thread stop itself
            self.shutdown = True;

    def parse_new_member(self,data):
        msg = data.split()
        if len(msg) != 4 or msg[0] != 'HELO':
            raise Warning("received message with incorrect format")
            return
        name = msg[1]
        self.client_name = name
        ip = msg[2]
        port = int(msg[3])
        member = Member(name,ip,port)
        return member

