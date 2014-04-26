# LICENSE

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
		self.test = 0

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
