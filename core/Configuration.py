# This file is part of pentoolbox.
# Please see LICENSE for details.

import os
import yaml
import argparse

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
		"""
		Instanciate the configuration.

		Parameters
			console: The current pentoolbox console.
		"""
		self.console = console
		self.packages_asked_for = []
		self.tools_asked_for = []
		self.tools_installed = {}
		self.install_dir = None
		self.install_dir_chmod = None
		self.log_file = open("/tmp/pentoolbox_log", "w")

		self.console.step("Loading configuration")

	def load_arguments(self):
		"""
		Load command line arguments.
		"""
		self.console.substep("Command line arguments")
		argparser = argparse.ArgumentParser()

		argparser.add_argument("-f", "--config", default="config.yml", \
			help="Path to configuration file to replace command line options")
		argparser.add_argument("-i", "--install-dir", \
			help="Installation directory")
		argparser.add_argument("-d", "--debug-level", default=0, \
			action="count", help="Increase g level")
		argparser.add_argument("-y", "--force-yes", action="store_true", \
			help="Do not ask before deleting an existing dir/file")
		argparser.add_argument("-p", "--package-mode", action="store_true", \
			help="Allow you to specify packages instead of tools")

		subparsers = argparser.add_subparsers(dest="mode")
		install_parser = subparsers.add_parser("install", help="Install tools")
		install_parser.add_argument("tools", nargs="+", \
			help="List of tools to install")
		update_parser = subparsers.add_parser("update", help="Update specific tools")
		update_parser.add_argument("tools", nargs="+", \
			help="List of tools to update")
		update_all_parser = subparsers.add_parser("update-all", \
			help="Update all installed tools")
		rm_parser = subparsers.add_parser("remove", help="Remove specific tools")
		rm_parser.add_argument("tools", nargs="+", help="List of tools to remove")

		arguments = argparser.parse_args()

		self.user_config_path = arguments.config
		self.debug_level = arguments.debug_level
		self.force_yes = arguments.force_yes
		self.console.set_debug_level(self.debug_level)
		self.console.set_force_mode(self.force_yes)

		if arguments.install_dir:
			self.install_dir = arguments.install_dir

		self.mode = arguments.mode

		if self.mode == 'update-all':
			arguments.tools = []

		if arguments.tools and not arguments.package_mode:
			self.tools_asked_for = arguments.tools
		elif arguments.tools and arguments.package_mode:
			self.packages_asked_for = arguments.tools

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
		self.install_dir_chmod = self.config["install-dir-chmod"]
		self.dep_cmd = self.config["dep-cmd"]
		self.dep_installed_cmd = self.config["dep-installed-cmd"]

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

			if not "expand-path" in data.keys():
				self.expand_path = False
			else:
				self.expand_path = data["expand-path"]

			if self.expand_path:
				if not "path-extension" in data.keys():
					raise Exception("You must specify the $PATH for extension")
				else:
					self.path_extension = data["path-extension"]
		else:
			self.console.warning("Config not found (%s)" % (self.user_config_path))

		if not self.install_dir:
			raise Exception("Installation directory must be specified.")

	def get_tmp_file_name(self):
		"""
		If necessary, the Configuration object can create temporary file name.
		This function does this.
		"""
		# FIXME: Really create a temporary file here.
		return "/tmp/iamatemporaryfile"

	def load_saved_tools(self):
		"""
		Load the list of already installed tools contained in the ._config file.
		The format of this file is:
			tool_name: tool/main/install/path
		"""
		if not self.install_dir:
			raise Exception("Installation directory must be specified.")

		self.console.substep("Saved installation config")
		saved_config = self.install_dir + "/._config"

		if not os.path.exists(saved_config):
			self.console.warning("No installed config found. First install ?")
			return

		with open(saved_config, "r") as f:
			for line in f.readlines():
				line = line.strip()
				if line:
					key, value = line.split(":", 1)
					self.tools_installed[key.strip()] = value.strip()

		os.chmod(saved_config, 0600)

	def end(self):
		"""
		Ensure the log file is closed.
		"""
		self.log_file.close()
