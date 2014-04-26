# LICENSE

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

	def build(self):
		"""
		This method builds the toolbox.
		Building means:
			* Retrieving the list of tools to be installed.
			* Loading information of each of these tools.
			* Grouping and listing categories of tools.
		"""
		tools_asked_for = self._config.tools_asked_for

		for tool in self._config.packages_asked_for:
			tools_asked_for.append(tool)

		map(self.load_tool, tools_asked_for)

	def load_tool(self, tool_name):
		"""
		Load a specific tool given his name.
		This function is reponsible for:
			* Ensuring the tool's configuration file is present.
			* Loading the tool with its config file.
			* Appending the tool and its categories to the list.
		"""
		tool_config_file = self._config.tools_path + tool_name + ".yml"

		print "Loading: %s (%s)" % (tool_name, tool_config_file)

		if not os.path.isfile(tool_config_file):
			# FIXME: Error
			return

		tool_instance = Tool(tool_name, tool_config_file)
		self.loaded_tools[tool_name] = tool_instance

		for category in tool_instance.get_categories():
			if category in self.categories.keys():
				self.categories[category].append(tool_name)
			else:
				self.categories[category] = [ tool_name ]

		print "Loaded: %s" % (tool_name)
