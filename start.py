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


# This script is the start-up script of the suite.
# It will take responsability for initializing everything.

from core.Shell import Shell

shell = Shell()
shell.start()
