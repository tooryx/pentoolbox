# LICENSE

import yaml
import os

class Tool(object):

	def __init__(self, tool_name, global_config, tool_config):
		"""
		FIXME: Comments. Explain config_file
		At this point, config_file's exisence has already been checked.
		"""
		self.name = tool_name
		self._config = global_config
		self._tool_cfg = tool_config
		self._categories = []
		self._real_path = None

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

	def get_categories(self):
		"""
		FIXME: Comments.
		"""
		if not self._categories and "categories" in self._options.keys():
			categories = filter(None, self._options["categories"].split(";"))
			for category in categories:
				self._categories.append(category)

		return self._categories

	def fetch(self, category_path):
		path = category_path + "/" + self.name

		if self._real_path:
			self._fetch_symlink(path)
			return

		self._real_path = path
		fetch_cmds = self._config.fetch_commands

		if not self.repository_type in fetch_cmds.keys():
			raise Exception("Can't fetch as %s, unknown command type (%s)" \
				% (self.repository_type, self._tool_cfg))

		current_dir = os.getcwd()
		os.chdir(category_path)

		self._fetch_install_cmd = fetch_cmds[self.repository_type]["install"]

		if "update" in fetch_cmds[self.repository_type].keys():
			self._fetch_update_cmd = fetch_cmds[self.repository_type]["update"]
		else:
			self._fetch_update_cmd = self._fetch_install_cmd

		self._fetch_install_cmd = self.populate_variables(self._fetch_install_cmd)
		self._fetch_update_cmd = self.populate_variables(self._fetch_update_cmd)

		if self._config.mode == "install":
			self._fetch_install(path)
		else:
			self._fetch_update(path)

		os.chdir(current_dir)

	def _fetch_symlink(self, path):
		print "Symlinking %s (%s)" % (self.name, path)
		os.symlink(self._real_path, path)

	def populate_variables(self, string):
		string = string.replace("{{name}}", self.name)
		string = string.replace("{{repository-url}}", self.repository_url)

		# FIXME: Temporary files.

		return string

	def _fetch_install(self, path):
		print "Fetching %s (%s)" % (self.name, path)
		os.system(self._fetch_install_cmd)

	def _fetch_update(self, path):
		pass

	def install(self):
		print "Installing: %s" % (self._real_path)
		pass

	def update(self):
		pass
