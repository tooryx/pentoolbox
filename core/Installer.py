# LICENSE

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

		for category,tools in enumerate(self.categories):
			self.prepare_category(category)
			self.fetch_tools(tools)

			# FIXME: There's a possible "update" action here.
			if self._config.mode == "install":
				self.install_tools(tools)
			else:
				self.update_tools(tools)

	def prepare_category(self, category):
		# If install: create_dir for category
		# elif update: nothing
		pass

	def fetch_tools(self, tools_list):
		# if install needs to rm then retrieve
		# if update:
		# 	git update
		#   --> install for http and co
		pass

	def install_tools(self, tools_list):
		pass

	def update_tools(self, tools_list):
		pass
