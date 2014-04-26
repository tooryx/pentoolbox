# LICENSE

import yaml

class Configuration(object):
	"""
	Ensure the configuration is held in only one place.
	This class is also responsible for handling priorities between configuration
	sources.
	"""

	_instance = None

	def __new__(cls, *args, **kwargs):
		"""
		We use the Singleton design pattern to make sure only one
		Configuration instance is active at all times.
		"""
		if not cls._instance:
			cls._instance = super(Configuration, cls).__new__(cls, *args, **kwargs)

		return cls._instance

	def __init__(self, console):
		self.console = console

		# THESE ARE TEST VALUES #
		with open("core/core_config.yml", "r") as f:
			self.config = yaml.load(f.read())

		self.fetch_commands = self.config["fetch"]
		self.tools_path = "tools/"

		self.packages_asked_for = []
		self.tools_asked_for = [ "nmap" ]
		self.mode = "install"
		# ------ END --------- #

	def load_arguments(self):
		"""
		Load command line arguments.
		Those configuration option have the highest priority.
		"""
		pass

	def load_core_config(self):
		"""
		Load core configuration file.
		By default this file is under core/core_config.yaml
		"""
		pass

	def load_user_config(self):
		"""
		Load the user specific configuration options.
		The default is ./config.yaml
		"""
		pass
