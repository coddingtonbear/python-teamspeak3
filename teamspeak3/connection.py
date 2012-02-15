# Copyright (c) 2012 Adam Coddington
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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
