from message import Message

__all__ = ['Command']

class Command(Message):
    def __init__(self, command, args = None):
        self.command = command
        if args:
            self.args = args
        else:
            self.args = {}

    def _clean_outgoing_value(self, value):
        for fr, to in self.MAPPINGS.items():
            value = value.replace(to, fr)
        return value

    def get_output(self):
        arglist = []
        for param, value in self.args.items():
            arglist.append("%s=%s" % (
                    param,
                    self._clean_outgoing_value(value),
                ))
        return "%s %s" % (
                    self.command,
                    " ".join(arglist),
                )
