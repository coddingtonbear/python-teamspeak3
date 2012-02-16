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
class Message(object):
    MAPPINGS = {
            '\\\\': '\\',
            '\\/': '/',
            '\\s': ' ',
            '\\p': '|',
            '\\a': '',
            '\\b': '',
            '\\f': '\n',
            '\\n': '\n',
            '\\r': '\n',
            '\\t': '\t',
            '\\v': '',
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
