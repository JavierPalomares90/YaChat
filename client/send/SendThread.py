# Class to send message on udp port
import threading


class SendThread(threading.Thread):

    def __init__(self, chatter):
        super(SendThread, self).__init__()
        self.chatter = chatter
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        while self.chatter.isEnabled():
            try:
                msg = self.chatter.get_input()
                self.chatter.send_to_all(msg)
            except (KeyboardInterrupt, EOFError):
                # send the exit message if the user
                # hits control c-d
                self.chatter.print_msg("caught keyboard exception")
                self.chatter.send_exit_msg()
        exit()



