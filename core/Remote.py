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

class Remote(object):
    """
    This class defined the way a tools is remotely fetched.
    For example, some child classes could be Git or Mercurial.
    Each tool is possess at least one remote.
    """

    def __init__(self, remote_addr, remote_port, local_name, extract=False, compiled=True):
        """
        Some initialization is made here.
        Of course, remote childs could override this method but should
        take care of those initialization and should keep param
        order (but you are free to add param with defaulted values).

        The best way to achieve this is by calling super().
        """
        self._remote_addr = remote_addr
        self._remote_port = remote_port
        self._local_name = local_name
        self._need_extract = extract
        self._need_compile = not(compiled)

    def fetch(self):
        """
        Retrieve the associated tool.
        Each child should call this as super LASTLY.
        """
        if (self._need_extract):
            # FIXME: Extract the tool (bzip2, gzip, zip, tar, ...)
            pass

        if (self._need_compile):
            # FIXME: Compile the tool (gcc, clang, ...)
            pass
