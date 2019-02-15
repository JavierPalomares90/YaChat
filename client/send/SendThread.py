# Class to send message on udp port
import threading


class SendThread(threading.Thread):

    def __init__(self, chatter):
        threading.Thread.__init__(self)
        self.chatter = chatter

    def run(self):
        while True:
            try:
                msg = self.chatter.get_input()
                self.chatter.send_to_all(msg)
            except KeyboardInterrupt:
                # send the exit message if the user
                # hits control c-d
                self.chatter.send_exit_msg()
            except:
                raise

