# This file is part of pentoolbox.
# Please see LICENSE for details.

import os
import yaml
import argparse
import tempfile

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
		self.packages_asked_for = []
		self.tools_asked_for = []
		self.install_dir = None
		self.install_dir_chmod = None
		self.log_file = tempfile.NamedTemporaryFile()

		self.console.step("Loading configuration")

	def load_arguments(self):
		"""
		Load command line arguments.
		Those configuration option have the highest priority.
		"""
		self.console.substep("Command line arguments")
		argparser = argparse.ArgumentParser()

		argparser.add_argument("-f", "--config", default="config.yml", \
			help="Path to configuration file")
		argparser.add_argument("-i", "--install-dir", \
			help="Installation directory")
		argparser.add_argument("-d", "--debug-level", default=0, type=int, \
			help="Defines the debug level")
		argparser.add_argument("-t", "--tools", \
			help="Coma separated list of tools to install")
		argparser.add_argument("-p", "--packages", \
			help="Coma separated list of packages to install")
		argparser.add_argument("-y", "--force-yes", action="store_true", \
			help="Do not ask before deleting an existing dir/file")
		argparser.add_argument("--install", action="store_true", \
			help="Tools will be installed.")
		argparser.add_argument("--update", action="store_true", \
			help="Tools will be updated.")

		arguments = argparser.parse_args()

		self.user_config_path = arguments.config
		self.debug_level = arguments.debug_level
		self.force_yes = arguments.force_yes
		self.console.set_debug_level(self.debug_level)
		self.console.set_force_mode(self.force_yes)

		if arguments.install_dir:
			self.install_dir = arguments.install_dir

		if arguments.install:
			self.mode = "install"
		elif arguments.update:
			self.mode = "update"
		else:
			raise Exception("You should specify either --install or --update")

		if arguments.tools:
			self.tools_asked_for = filter(None, arguments.tools.split(","))

		if arguments.packages:
			self.packages_asked_for = filter(None, arguments.packages.split(","))

	def load_core_config(self):
		"""
		Load core configuration file.
		This file is under core/core_config.yml
		"""
		self.console.substep("Core configuration")
		core_config = "core/core_config.yml"
		if not os.path.exists(core_config):
			raise Exception("Core config file not found (%s)" % core_config)

		with open(core_config, "r") as f:
			self.config = yaml.load(f.read())

		self.fetch_commands = self.config["fetch"]
		self.tools_path = self.config["tools-path"]
		self.temp_dir = self.config["temp-dir"]
		self.install_dir_chmod = self.config["install-dir-chmod"]

	def load_user_config(self):
		"""
		Load the user specific configuration options.
		"""
		self.console.substep("User configuration")

		if os.path.exists(self.user_config_path):
			with open(self.user_config_path, "r") as c:
				data = yaml.load(c.read())

			if not self.install_dir and "install-dir" in data.keys():
				self.install_dir = data["install-dir"]

			if not self.tools_asked_for and "tools" in data.keys():
				self.tools_asked_for = data["tools"]

			if not self.packages_asked_for and "packages" in data.keys():
				self.packages_asked_for = data["packages"]

			if not "expand-path" in data.keys():
				self.expand_path = False
			else:
				self.expand_path = data["expand-path"]

			if self.expand_path:
				if not "path-extension" in data.keys():
					raise Exception("You must specify the path for $PATH extension")
				else:
					self.path_extension = data["path-extension"]
		else:
			self.console.warning("Config not found (%s)" % (self.user_config_path))

		if not self.install_dir:
			raise Exception("Installation directory must be specified.")
