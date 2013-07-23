#! /usr/bin/python

# This file is part of OTD.
#
# OTD is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OTD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OTD. If not, see <http://www.gnu.org/licenses/>.

import os

class Shell(object):
    """
    The shell given to the user.

    For now this is a very basic shell. It should be enhanced with time or
    replaced with a python library maybe ?
    """

    def __init__(self):
        """
        Makes basic initialization.
        """
        self._exit_command = "exit"
        self._available_tools = {}
        self._internal_commands = {
            "list": self.list_tools
            }

        self.load_commands()

    def list_tools(self):
        """
        Retrieve and outputs the list of currently loaded tools.
        """
        for category in self._available_tools.keys():
            print "- %s" % (category)
            for tool in self._available_tools[category]:
                print "\t* %s (Command: %s)" % (tool.name, tool.command_name)

    def load_commands(self):
        """
        Loads every tools from available_tools directory.
        """
        path = "available_tools/"
        for f in os.listdir(path):
            if os.path.isfile(path + f):
                spl = os.path.splitext(f)

                if len(spl) <= 1 or spl[1] == ".pyc" or spl[0] == "__init__":
                    continue

                module = spl[0]

                try:
                    exec("from available_tools.%s import %s" % (module, module))
                    exec("obj = %s()" % (module))
                    for category in obj._categories:
                        if not category in self._available_tools.keys():
                            self._available_tools[category] = []
                        self._available_tools[category].append(obj)
                except Exception as e:
                    print "Could not load: %s (%s)" % (module, e)

    def start(self):
        """
        Starts the shell and the main loop.
        """
        while True:
            command = raw_input("> ")

            if command == self._exit_command:
                break

            self.handle_command(command)

    def handle_command(self, command):
        """
        Handle one command.
        """
        spl = command.strip().split()

        if len(spl) >= 1:
            for tool_list in self._available_tools.values():
                for tool in tool_list:
                    if spl[0] == tool.command_name:
                        print "Tool: %s" % (tool.name)
                        return

            if spl[0] in self._internal_commands:
                self._internal_commands[spl[0]]()
                return

            # FIXME: Fallback to real 'shell'.
            print "[FIXME] Unrecognized command: %s" % (spl[0])
