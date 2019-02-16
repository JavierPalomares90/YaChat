# Class to receive messages on udp port

import threading


class ReceiveThread(threading.Thread):

    def __init__(self, chatter, bufferSize):
        threading.Thread.__init__(self)
        self.chatter = chatter
        self.BUFFER_SIZE = bufferSize

    def run(self):
        while True:
            msg, address = self.chatter.udp_socket.recvfrom(self.BUFFER_SIZE)
            if self.chatter.isEnabled():
                msg = msg.decode("utf-8")
                if msg.startswith("MESG"):
                    self.chatter.parse_msg(msg)
                elif msg.startswith("JOIN"):
                    self.chatter.parse_server_join(msg)
                elif msg.startswith("EXIT"):
                    self.chatter.parse_server_exit(msg)
                else:
                    raise Exception("Unknown message: {}".format(msg))
                self.chatter.print_prompt()
            else:
                exit()

