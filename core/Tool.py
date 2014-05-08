# This file is part of pentoolbox.
# Please see LICENSE for details.

import yaml
import shutil
import os
import subprocess

class Tool(object):

	def __init__(self, tool_name, global_config):
		"""
		FIXME: Comments. Explain config_file
		At this point, config_file's exisence has already been checked.
		"""
		self.name = tool_name
		self._config = global_config
		self._tool_cfg = self._config.tools_path + tool_name + ".yml"
		self._categories = []
		self._real_path = None
		self._installed = False
		self._tmp_files = []

		if not os.path.isfile(self._tool_cfg):
			raise Exception("Error loading config (%s)" % self._tool_cfg)

		self.load_config()

	def load_config(self):
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
		if not self._categories and "categories" in self._options.keys():
			categories = filter(None, self._options["categories"].split(";"))
			for category in categories:
				self._categories.append(category)

		return self._categories

	def get_all_paths(self):
		"""
		Warning ! When this function is called _real_path should be set.
		"""
		res = [ self._real_path ]

		for category in self._categories:
			res.append(self._config.install_dir + "/" + category + "/" + self.name)

		for binary in self.binaries_path:
			res.append(self._config.path_extension + "/" + binary)

		return list(set(res))

	def fetch(self):
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
		if not os.path.exists(path):
			self._config.console.debug(1, "Symlinking (%s)" % (path))
			os.symlink(self._real_path, path)
		else:
			self._config.console.debug(1, "Symlink/dir exists (%s)" % (path))

	def populate_variables(self, string):
		string = string.replace("{{name}}", self.name)
		string = string.replace("{{repository-url}}", self.repository_url)
		string = string.replace("{{tool-full-path}}", self._real_path)
		string = string.replace("{{tool-parent-path}}", self._real_category_path)

		tmp_file = self._config.get_tmp_file_name()
		self._tmp_files.append(tmp_file)

		string = string.replace("{{tmp-file}}", tmp_file)

		return string

	def _fetch_install(self, path):
		self._config.console.step("Fetching %s (%s)" % (self.name, path))

		if os.path.exists(path):
			self._config.console.exists(path)

			# We only delete if it's a directory
			# Any file would be overwritten anyway.
			if not os.path.isfile(path):
				shutil.rmtree(path)

		self._exec_command(self._fetch_install_cmd)

	def _fetch_update(self, path):
		self._config.console.step("Fetching %s (%s)" % (self.name, path))
		self._exec_command(self._fetch_update_cmd)

	def _exec_command(self, command, fatal=False):
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

	def _wrapper_install_or_update(self, action):
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
		command = self._config.dep_installed_cmd + " " + depName
		logFile = open(os.devnull, "w")

		ret_val = subprocess.call(command, stderr=logFile, stdout=logFile, \
			shell=True)

		logFile.close()

		return (ret_val == 0)

	def _manage_deps(self):
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
		
		self._exec_command(dep_string, fatal=True)

	def install(self):
		if self._installed:
			return

		self._installed = True
		self._wrapper_install_or_update("install")

	def update(self):
		self._wrapper_install_or_update("update")

	def clean_tmp(self):
		for f in self._tmp_files:
			if os.path.exists(f):
				os.unlink(f)
