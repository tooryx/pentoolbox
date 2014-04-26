# LICENSE

import os

class Installer(object):

	def __init__(self, config, toolbox):
		self._toolbox = toolbox
		self._config = config

	def start(self):
		"""
		Starts the installation process.
		An installation process can refer:
			* To a new installation
			* An update

		In both case, the following actions are taken:
			* Creating directories if necessary
			* Fetching all tools (install and non repository-based updates)
			* Installing/updating all tools
			* Cleaning
		"""
		self.tools = self._toolbox.loaded_tools
		self.categories = self._toolbox.categories

		self.prepare_install_dir()
		self.prepare_temp_dir()

		for category,tools in self.categories.iteritems():
			self.prepare_category_dir(category)
			self.process_tools(tools)

		self.clean_temp_dir()

	def prepare_install_dir(self):
		self.install_dir = self._config.install_dir

		if not os.path.exists(self.install_dir):
			print "Creating %s" % self.install_dir
			os.mkdir(self.install_dir)
			# FIXME: chmod

	def prepare_temp_dir(self):
		self.temp_dir = self._config.temp_dir
		pass

	def prepare_category_dir(self, category):
		self._current_category_dir = self.install_dir + "/" + category

		if not os.path.exists(self._current_category_dir):
			print "Creating %s" % (self._current_category_dir)
			os.mkdir(self._current_category_dir)

	def process_tools(self, tools_list):
		for tool_name in tools_list:
			tool_instance = self.tools[tool_name]
			tool_instance.fetch(self._current_category_dir)

			if self._config.mode == "install":
				tool_instance.install()
			else:
				tool_instance.udate()

	def clean_temp_dir(self):
		pass
