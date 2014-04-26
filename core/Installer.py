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
		pass
