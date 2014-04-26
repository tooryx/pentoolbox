# LICENSE

import yaml

class Tool(object):

	def __init__(self, tool_name, config_file):
		"""
		FIXME: Comments. Explain config_file
		At this point, config_file's exisence has already been checked.
		"""
		self._categories = []

		print "Object created for tool: %s" % (tool_name)

		with open(config_file, "r") as c:
			data = yaml.load(c.read())

		if tool_name not in data.keys():
			raise Exception("Malformed yaml file: %s" % (config_file))

		self._options = data[tool_name]

	def get_categories(self):
		"""
		FIXME: Comments.
		"""
		if not self._categories and "categories" in self._options.keys():
			categories = filter(None, self._options["categories"].split(";"))
			for category in categories:
				self._categories.append(category)

		return self._categories
