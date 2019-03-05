# thread class to spin off a new class for every client

import threading

from server.Server import Server


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
                    raise Warning("Unable to receive from: " + self.buffer_size)

    # parse the message from the client
    def parse_client_msg(self,msg_from_client):
        member = Server.parse_new_member(msg_from_client)
        members = self.get_members()
        if member.name in members:
            # the screen_name is already in use
            self.send_reject_message(member)
        else:
            self.add_member(member)
            self.send_accept_message()

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
        for member in members:
            name = member.name
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

