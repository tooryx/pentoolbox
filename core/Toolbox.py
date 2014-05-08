# This file is part of pentoolbox.
# Please see LICENSE for details.

import os.path
from core.Tool import Tool

class Toolbox(object):
	"""
	FIXME: Comments.
	"""

	def __init__(self, config):
		"""
		FIXME: Comments.

		self.loaded_tools has the following form:
			{
				tool_name:
					tool_instance
			}
		self.categories has the following form:
			{
				category_name:
					[ tool_name, tool_name ]
			}
		"""
		self._config = config
		self.loaded_tools = {}
		self.categories = {}
		self.installed_tools = {}

		self._config.console.step("Loading toolbox")

	def build(self):
		"""
		This method builds the toolbox.
		Building means:
			* Retrieving the list of tools to be installed.
			* Loading information of each of these tools.
			* Grouping and listing categories of tools.
		"""
		tools_asked_for = self._config.tools_asked_for
		packages_asked_for = self._config.packages_asked_for

		tools_installed = self._config.tools_installed
		tools_to_install = []

		if self._config.mode == "install":
			for tool in tools_asked_for:
				if tool in tools_installed.keys():
					self._config.console.warning("%s already installed. Skipped." \
						% (tool))
				else:
					tools_to_install.append(tool)

		map(self.load_tool, tools_to_install)

		for tool, path in tools_installed.iteritems():
			instance = Tool(tool, self._config)
			instance._real_path = path
			self.installed_tools[tool] = instance

		# FIXME: Add packages 0/

	def load_tool(self, tool_name):
		"""
		Load a specific tool given his name.
		This function is reponsible for:
			* Ensuring the tool's configuration file is present.
			* Loading the tool with its config file.
			* Appending the tool and its categories to the list.
		"""
		self._config.console.substep("Loading %s" % (tool_name))

		tool_instance = Tool(tool_name, self._config)
		self.loaded_tools[tool_name] = tool_instance

		for category in tool_instance.get_categories():
			if category in self.categories.keys():
				self.categories[category].append(tool_name)
			else:
				self.categories[category] = [ tool_name ]

	def save_tools(self):
		save_file = self._config.install_dir + "/._config"

		with open(save_file, "w") as f:
			for tool, path in self._config.tools_installed.iteritems():
				f.write("%s: %s\n" % (tool, path))
