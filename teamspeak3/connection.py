from telnetlib import Telnet

from message import Message
from command import Command

class TeamspeakConnection(Telnet):
    def __init__(self, hostname, port, timeout, pipe_in, pipe_out):
        self.pipe_in = pipe_in
        self.pipe_out = pipe_out
        Telnet.__init__(self, hostname, port, timeout)

    def write_command(self, command):
        self.write("%s\n" % command.get_output())

    def main_loop(self):
        while True:
            if not self.pipe_in.empty():
                comm = self.pipe_in.get_nowait()
                if isinstance(comm, Command):
                    self.write_command(comm)
            incoming = self.receive_message()
            if incoming:
                self.pipe_out.put(incoming)

    def receive_message(self):
        incoming_message = self.read_until('\n', self.timeout)
        try:
            return Message(incoming_message)
        except ValueError:
            return None
