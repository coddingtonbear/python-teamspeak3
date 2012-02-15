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

    def get_message(self):
        if not self.pipe_in.empty():
            msg = self.pipe_in.get_nowait()
            return msg
        return None

    def send_command(self, command):
        self.pipe_out.put(command)
