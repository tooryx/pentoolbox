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

class Tool(object):
    """
    A tool or project is the main component of OTD.
    It's what the script will try to fetch or update.
    """

    def __init__(self):
        """
        Each tool should be initialized. Logic.
        The LAST thing each tool do when initializing is to call the super
        initializer so core required initialization are made.

        Each module should at least initialize those values:
            - self.name: The tool name. Example: nmap ;
            - self.command_name: The tool command name. For example: tool.py ;
            - self._remote_list: List of Remote object to fetch the tool ;
            - self._require_sudo: Does the tool need privilege escalation ?
            - self._categories: A list of categories this tool belongs to.
        """
        pass

    def execute(self, *arguments):
        """
        Execute the tool with given arguments.
        """
        pass

    def is_installed(self):
        """
        As for now there's no database, this function verifies the presence
        of the tool locally.
        """
        return (os.path.exists("installed_tools/%s" % (self.name)))

    def fetch(self):
        """
        Actually fetches the tool using its remote.
        Once a remote succeed, we're stopping the fetch.
        """
        for remote in self._remote_list:
            try:
                remote.fetch()
                break
            except:
                continue
