# This file is part of pentoolbox.
# Please see LICENSE for details.

import yaml
import shutil
import os
import subprocess

class Tool(object):
	"""
	A tool is what the user will want to install.
	This object is responsible for:
		- Loading a tool configuration
		- Fetching a tool from its repo/website
		- Installing the tool (each tool as its own set of commands)
		- Creating symlink for different categories
		- Installing dependencies
		- Updating the tool
	"""

	def __init__(self, tool_name, global_config):
		"""
		Create the instance.
		
		Parameters
			tool_name: The name of the tool. Used to load config file.
			global_config: The current pentoolbox configuration object.
		"""
		self.name = tool_name
		self._config = global_config
		self._tool_cfg = self._config.tools_path + tool_name + ".yml"
		self._categories = []
		self._real_path = None
		self._tmp_files = []

		if not os.path.isfile(self._tool_cfg):
			raise Exception("Error loading config (%s)" % self._tool_cfg)

		self.load_config()

	def load_config(self):
		"""
		Load the configuration file (.yml) and populates variables.
		For example, the repository type or url or the command used to install
			the tool.
		"""
		with open(self._tool_cfg, "r") as c:
			data = yaml.load(c.read())

		if self.name not in data.keys():
			raise Exception("Malformed yaml file: %s" % (config_file))

		self._options = data[self.name]

		if not "repository-type" in self._options.keys() \
		or not "repository-url" in self._options.keys():
			raise Exception("repository type or url missing (%s)" \
				% (self._tool_cfg))

		self.repository_type = self._options["repository-type"]
		self.repository_url = self._options["repository-url"]

		self.install_commands = []
		self.update_commands = []
		self.binaries_path = []

		if "install-commands" in self._options.keys():
			self.install_commands = self._options["install-commands"]

		if "update-commands" in self._options.keys():
			self.update_commands = self._options["update-commands"]

		if "binaries-path" in self._options.keys():
			self.binaries_path = self._options["binaries-path"]

		self.get_categories()

	def get_categories(self):
		"""
		Retrieve the list of categories the tool is part of.
		
		Return value
			List of categories(string)
		"""
		if not self._categories and "categories" in self._options.keys():
			categories = filter(None, self._options["categories"].split(";"))
			for category in categories:
				self._categories.append(category)

		return self._categories

	def get_all_paths(self):
		"""
		Retrieve all paths the tool may be installed under.
		This contains the binaries installed in the binaries directory
			when expand path option is enabled.
		
		Return value
			List of paths(string)
		"""
		res = [ self._real_path ]

		for category in self._categories:
			res.append(self._config.install_dir + "/" + category + "/" + self.name)

		for binary in self.binaries_path:
			res.append(self._config.path_extension + "/" + binary)

		return list(set(res))

	def fetch(self):
		"""
		Find the best way to fetch the tool.
		This function does the following:
			- Retrieve the main folder of installation
			- Creates a symlink for each other categories
			- Retrieve the repository type and its fetch commands
			- Change variables in those commands
			- If this is an installation:
				* Change  directory for the *category* folder (not the tool's one)
				* Launch the installation specialized fetch action
			- If this is an update:
				* Change directory for the *tool* folder
				* Launch the update specialied fetch action
			- Clean temporary files that may have been created.
			- Change directory for last directory
		"""
		if len(self._categories) == 0:
			raise Exception("Tool %s has no defined categories." % (self.name))

		self._real_category_path = self._config.install_dir + "/" + self._categories[0]
		self._real_path = self._real_category_path + "/" + self.name

		if len(self._categories) > 1:
			for category in self._categories[1:]:
				path = self._config.install_dir + "/" + category + "/" + self.name
				self._fetch_symlink(path)

		fetch_cmds = self._config.fetch_commands

		if not self.repository_type in fetch_cmds.keys():
			raise Exception("Can't fetch as %s, unknown command type (%s)" \
				% (self.repository_type, self._tool_cfg))

		current_dir = os.getcwd()

		self._fetch_install_cmd = fetch_cmds[self.repository_type]["install"]

		if "update" in fetch_cmds[self.repository_type].keys():
			self._fetch_update_cmd = fetch_cmds[self.repository_type]["update"]
		else:
			self._fetch_update_cmd = self._fetch_install_cmd

		self._fetch_install_cmd = self.populate_variables(self._fetch_install_cmd)
		self._fetch_update_cmd = self.populate_variables(self._fetch_update_cmd)

		if self._config.mode == "install":
			os.chdir(self._real_category_path)
			self._fetch_install(self._real_path)
		else:
			os.chdir(self._real_path)
			self._fetch_update(self._real_path)

		self.clean_tmp()
		os.chdir(current_dir)

	def _fetch_symlink(self, path):
		"""
		This function is responsible for creating the symlink.
		It's called when a category is not the main one and the tool should
			be symlinked (obviously).

		Parameter
			path: The absolute path of the symlink (with symlink name)
		"""
		if not os.path.exists(path):
			self._config.console.debug(1, "Symlinking (%s)" % (path))
			os.symlink(self._real_path, path)
		else:
			self._config.console.debug(1, "Symlink/dir exists (%s)" % (path))

	def populate_variables(self, string):
		"""
		When creating fetch commands in the core_config file you have the
			possibility to use custom variables.
		Those variables are modified here.
		If necessary, this function also ask for the creation of a temporary file.

		Parameters
			string: The string to modify the variables in.

		Return value
			The modified string
		"""
		string = string.replace("{{name}}", self.name)
		string = string.replace("{{repository-url}}", self.repository_url)
		string = string.replace("{{tool-full-path}}", self._real_path)
		string = string.replace("{{tool-parent-path}}", self._real_category_path)

		tmp_file = self._config.get_tmp_file_name()
		self._tmp_files.append(tmp_file)

		string = string.replace("{{tmp-file}}", tmp_file)

		return string

	def _fetch_install(self, path):
		"""
		This is the install specialized fetch action.
		- Ask the user and delete the tool directory if exists
		- Execute the fetch command corresponding to install

		Parameters
			path: The path of the installation.
		"""
		self._config.console.step("Fetching %s (%s)" % (self.name, path))

		if os.path.exists(path):
			self._config.console.exists(path)

			# We only delete if it's a directory
			# Any file would be overwritten anyway.
			if not os.path.isfile(path):
				shutil.rmtree(path)

		self._exec_command(self._fetch_install_cmd)

	def _fetch_update(self, path):
		"""
		This is the update specialized fetch action.
		It just launch the update command.

		Parameters
			path: The path of the installation.
		"""
		self._config.console.step("Fetching %s (%s)" % (self.name, path))
		self._exec_command(self._fetch_update_cmd)

	def _exec_command(self, command, fatal=False):
		"""
		This is a helper for command execution.
		It will execute a command by retrieving the pentoolbox logFile and
			appending stdout/stderr of tool to this log file.

		Parameters
			command: The command  to execute.
			fatal: Is the command fatal to program ? (if return value not 0)
		"""
		command = command.strip()

		if len(command) > 80:
			self._config.console.substep(command[:80] + "[...]")
		else:
			self._config.console.substep(command)

		logFile = self._config.log_file
		ret_val = subprocess.call(command, stderr=logFile, stdout=logFile, \
			shell=True)

		if ret_val == 0:
			msg = "Return code: {{green}}%s{{nocolor}}" % (ret_val)
		elif fatal:
			raise Exception("Return code %s for command `%s`" % (ret_val, command))
		else:
			msg = "Return code: {{red}}%s{{nocolor}} (See: %s)" \
			% (ret_val, logFile.name)

		self._config.console.substep(msg)

	def install(self):
		"""
		Launch tool installation by calling the wrapper in install mode.
		"""
		self._wrapper_install_or_update("install")

	def update(self):
		"""
		Launch tool update by calling the wrapper in update mode.
		"""
		self._wrapper_install_or_update("update")

	def _wrapper_install_or_update(self, action):
		"""
		As its name state this is a wrapper to launch either:
			- An installation
			- An update

		This function does the following:
			- Retrieve the commands (install commands or update commands)
			- If this is an install, we need to ensure dependencies are ok.
			- Change dir to the tool directory (which has been created by fetch)
			- Launch the commands

		Parameters
			action: Defines if this is an install or an update.
		"""
		if action == "install":
			msg = "Installing %s (%s)" % (self.name, self._real_path)
			commands = self.install_commands
		else:
			msg = "Updating %s (%s)" % (self.name, self._real_path)
			commands = self.update_commands

		self._config.console.step(msg)

		if action == "install":
			self._manage_deps()

		current_dir = os.getcwd()
		os.chdir(self._real_path)

		self._config.console.substep("Install commands")
		
		if type(commands) == str:
			commands = [ commands ]

		for command in commands:
			self._exec_command(command)

		os.chdir(current_dir)

	def is_dependency_installed(self, depName):
		"""
		Checks if a depedency is installed.
		It uses the command in the core_config file to do so.

		Parameters
			depName: The dependency name.

		Return value
			Is the dependency installed ? (bool)
		"""
		command = self._config.dep_installed_cmd + " " + depName
		logFile = open(os.devnull, "w")

		ret_val = subprocess.call(command, stderr=logFile, stdout=logFile, \
			shell=True)

		logFile.close()

		return (ret_val == 0)

	def _manage_deps(self):
		"""
		Checks and install all dependencies needed by a tool.
		"""
		if not "dependencies" in self._options.keys() \
		or not self._options["dependencies"]:
			return

		self._config.console.substep("Checking for dependencies")
		dep_string = self._config.dep_cmd

		for dependency in self._options["dependencies"]:
			if not self.is_dependency_installed(dependency):
				dep_string += " " + dependency

		if dep_string == self._config.dep_cmd:
			return

		self._config.console.warning("Following dep will be installed: %s" \
			% (dep_string))
		
		if not self._config.console.prompt():
			exit(1)

		self._exec_command(dep_string, fatal=True)

	def clean_tmp(self):
		"""
		Clean all temporary files created.
		(Mainly by fetch)
		"""
		for f in self._tmp_files:
			if os.path.exists(f):
				os.unlink(f)
