class Message(object):
    MAPPINGS = {
            '\\s': ' ',
            '\\n': '\n',
            }

    def __init__(self, command):
        command = command.strip()
        if not command:
            raise ValueError("No command")

        self.raw_command = command

        self.args = self._get_arguments_from_string(self.raw_command)
        self.command = self._get_command_from_string(self.raw_command)

    def _get_command_from_string(self, cmd):
        return cmd.split(' ')[0]

    def _get_arguments_from_string(self, cmd):
        args = {}
        raw_args = cmd.split(' ')[1:]
        for raw_arg in raw_args:
            attribute, value = raw_arg.split('=', 1)
            args[attribute] = self._clean_incoming_value(value)
        return args

    def _clean_incoming_value(self, value):
        for fr, to in self.MAPPINGS.items():
            value = value.replace(fr, to)
        return value

    def __getitem__(self, key):
        return self.args[key]

    def __str__(self):
        return self.command

    def __unicode__(self):
        return unicode(self.__str__())

    def __repr__(self):
        return "<%s %s>" % (
                    self.__str__(),
                    self.args
                )
