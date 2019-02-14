# Class to send message on udp port
import threading


class SendThread(threading.Thread):

    def __init__(self, chatter):
        threading.Thread.__init__(self)
        self.chatter = chatter

    def run(self):
        while True:
            msg = self.chatter.get_input()
            self.chatter.send_to_all(msg)

