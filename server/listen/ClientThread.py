# thread class to spin off a new class for every client

import threading

from server import Server


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
                            break;
                        msg = msg.decode("utf-8")
                        buf += msg
                    msg_from_client = buf.strip()
                    self.parse_client_msg(msg_from_client)
                except Exception as e:
                    raise Warning("Unable to receive from: " + self.buffer_size)

    def parse_client_msg(self,msg_from_client):
        member = Server.parse_new_member(msg_from_client)
        members = self.get_members()
        if member.name in members:
            # the screen_name is already in use
            self.send_reject_message(member)
        else:
            self.add_member(member)



    #TODO: Need to let the client thread


