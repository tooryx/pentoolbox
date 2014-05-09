# This file is part of pentoolbox.
# Please see LICENSE for detailsself.

import os
import shutil

class Installer(object):

	def __init__(self, config, toolbox):
		"""
		Instanciate the Installer.

		Parameters
			toolbox: An instance of toolbox object.
			config: The pentoolbox config object.
		"""
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
		self.installed_tools = self._toolbox.installed_tools

		self.prepare_install_dir()
		self.prepare_binaries_dir()
		self.temp_dir = self._config.temp_dir
		self._tmp_file = None

		for category in self.categories.keys():
			self.prepare_category_dir(category)

		if self._config.mode == "install":
			self.install_tools(self.tools.keys())
			map(self.expand_path, self.installed_tools.values())
		elif self._config.mode == "update":
			self.update_tools(self._config.tools_asked_for)
			map(self.expand_path, self.installed_tools.values())
		elif self._config.mode == "update-all":
			self.update_tools(self.installed_tools)
		elif self._config.mode == "remove":
			self.remove_tools(self._config.tools_asked_for)

	def prepare_install_dir(self):
		"""
		Creates the installation directory and change its permissions.
		This can be parametized in the user_config and the core_config files.
		"""
		self.install_dir = self._config.install_dir

		if not os.path.exists(self.install_dir):
			self._config.console.debug(1, "Creating directory (%s)" \
				% self.install_dir)
			os.mkdir(self.install_dir)
		else:
			self._config.console.debug(1, "Directory exists (%s)" \
				% (self.install_dir))

		if self._config.install_dir_chmod:
			os.chmod(self.install_dir, self._config.install_dir_chmod)

	def prepare_binaries_dir(self):
		"""
		If the user asked for path expansion, there's a need to create
			the directory which will contains all binaries.
		This folder permissions are set to 750 once created.
		"""
		if not self._config.expand_path:
			return

		self.path_extension = self._config.path_extension

		if not os.path.exists(self.path_extension):
			os.mkdir(self.path_extension)
		
		os.chmod(self.path_extension, 0750)

	def prepare_category_dir(self, category):
		"""
		This creates a directory in the install-dir for a given category.

		Parameters
			category: The category name.
		"""
		category_dir = self.install_dir + "/" + category

		if not os.path.exists(category_dir):
			self._config.console.debug(1, "Creating directory (%s)" \
				% (category_dir))
			os.mkdir(category_dir)
		else:
			self._config.console.debug(1, "Directory exists (%s)" \
				% (category_dir))

	def install_tools(self, tools_list):
		"""
		Install mode:
			- Fetch the tool
			- Install it
			- Add it to list of installed tools
			- Expand the path option

		Parameters:
			tools_list: List of tools to be installed.
		"""
		for tool_name in tools_list:
			tool_instance = self.tools[tool_name]

			tool_instance.fetch()
			tool_instance.install()

			self._config.tools_installed[tool_name] = tool_instance._real_path
			self.expand_path(tool_instance)

	def update_tools(self, tools_list):
		"""
		Update and update-all modes:
			- Fetch the tool (if necessary)
			- Update the tool
			- Expand path option

		Parameters:
			tools_list: List of tools to be updated.
		"""
		for tool_name in tools_list:
			if not tool_name in self.installed_tools.keys():
				self._config.console.warning("%s not installed. Can't update." \
					% (tool_name))
				continue

			tool_instance = self.installed_tools[tool_name]

			tool_instance.fetch()
			tool_instance.update()

			self.expand_path(tool_instance)

	def remove_tools(self, tools_list):
		"""
		Remove mode:
			- Retrieve tool installation paths
			- Makes sure the user really want to delete those paths
			- Remove those paths (file, symlink and directories)
			- Remove the tool from list of installed tools

		Parameters:
			tools_list: List of tools to be removed.
		"""
		for tool_name in tools_list:
			if not tool_name in self.installed_tools.keys():
				self._config.console.warning("%s not installed. Can't remove." \
					% (tool_name))
				continue

			tool_instance = self.installed_tools[tool_name]
			tool_paths = tool_instance.get_all_paths()

			self._config.console.warning("Those will be deleted:")

			for path in tool_paths:
				self._config.console.warning("   %s" % (path))

			if not self._config.console.prompt("Really remove %s ?" % (tool_name)):
				exit(1)

			self._config.console.step("Removing %s" % (tool_name))

			for path in tool_paths:
				if os.path.exists(path):
					if os.path.isfile(path) or os.path.islink(path):
						os.unlink(path)
					else:
						shutil.rmtree(path)

			del self._config.tools_installed[tool_name]

	def expand_path(self, tool_instance):
		"""
		If the user asked for the path expansion we shall copy all the
			current tool binaries to the binary directory.

		Parameters
			tool_instance: The current tool instance (to access binaries list)
		"""
		if not self._config.expand_path:
			return

		real_path = tool_instance._real_path

		for binary in tool_instance.binaries_path:
			real_bin_path = real_path + "/" + binary
			link_bin_path = self.path_extension + "/" + binary

			if os.path.exists(link_bin_path):
				return

			if not os.path.exists(real_bin_path):
				continue

			os.chmod(real_bin_path, 0750)
			os.symlink(real_bin_path, link_bin_path)
