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
from multiprocessing import Process, Queue

from connection import TeamspeakConnection

__all__ = ['Client']

class Client(object):
    def __init__(self, hostname='127.0.0.1', port=25639, timeout=0.25):
        self.pipe_out = Queue()
        self.pipe_in = Queue()

        self.proc = Process(
                target=self.__class__.start_connection,
                args = (hostname, port, timeout, self.pipe_in, self.pipe_out)
            )
        self.proc.start()

    def __enter__(self, *args, **kwargs):
        return Client(*args, **kwargs)

    def __exit__(self, type, value, traceback):
        self.proc.terminate()
        return True

    def close(self):
        self.proc.terminate()

    @classmethod
    def start_connection(cls, hostname, port, timeout, pipe_in, pipe_out):
        # Connect the out to the in, and the in to the out.
        conn = TeamspeakConnection(hostname, port, timeout, pipe_out, pipe_in)
        conn.main_loop()

    def get_messages(self):
        messages = []
        while True:
            message = self.get_message()
            if not message:
                return messages
            messages.append(message)

    def get_message(self):
        if not self.pipe_in.empty():
            msg = self.pipe_in.get_nowait()
            return msg
        return None

    def send_command(self, command):
        self.pipe_out.put(command)
