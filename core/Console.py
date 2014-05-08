# This file is part of pentoolbox.
# Please see LICENSE for details.

class Console(object):

	def __init__(self):
		self._nocolor = "\033[00m"
		self._bold = "\033[00;01m"
		self._yellow = "\033[33;01m"
		self._green = "\033[32;01m"
		self._blue = "\033[34;01m"
		self._red = "\033[31;01m"

	def replace_color(self, message):
		message = message.replace("{{nocolor}}", self._nocolor)
		message = message.replace("{{bold}}", self._bold)
		message = message.replace("{{yellow}}", self._yellow)
		message = message.replace("{{green}}", self._green)
		message = message.replace("{{blue}}", self._blue)
		message = message.replace("{{red}}", self._red)

		return message

	def warning(self, message):
		msg = self.replace_color("{{red}}[{{yellow}}!{{red}}]{{nocolor}} %s" \
			% (message))
		print msg

	def prompt(self, message=None):
		if not message:
			message = "Continue ?"

		message = "{{red}}[{{yellow}}!{{red}}]{{nocolor}} %s [y/N] " % (message)
		message = self.replace_color(message)

		if self.force_mode:
			print message
			return True

		while True:
			raw_answer = raw_input(message)
			raw_answer = raw_answer.strip().lower()

			if raw_answer in [ "y", "yes" ]:
				return True
			elif raw_answer in [ "n", "no" ]:
				return False

	def set_debug_level(self, level):
		self.debug_level = level

	def set_force_mode(self, force_mode):
		self.force_mode = force_mode

	def step(self, message):
		print
		msg = self.replace_color("{{blue}}[{{bold}}-{{blue}}]{{nocolor}} %s" \
			% (message))
		print msg

	def substep(self, message):
		msg = self.replace_color("    {{bold}}*{{nocolor}} %s" % (message))
		print msg

	def banner(self):
		print """
	         PENTOOLBOX
	 '------------------------'
	  |__ '==' ------ '==' __|
	    |                  |
	    |__________________|
		"""

	def dump_config(self, config):
		self.step("Current configuration")
		self.substep("Log file: {{bold}}%s{{nocolor}}" % (config.log_file.name))
		self.substep("Mode: {{bold}}%s{{nocolor}}" % (config.mode))

		tools = ""
		for tool in config.tools_asked_for:
			tools += "%s " % tool

		self.substep("Tools concerned: %s" % (tools))
		self.substep("Install directory: %s" % (config.install_dir))
		self.substep("Path for binaries: %s" % (config.path_extension))

	def dump_installed_tools(self, config):
		self.step("Installed tools")

		for tool in config.tools_installed:
			self.substep("%s" % (tool))

		print

	def exists(self, path):
		if not self.prompt("File/dir exists and will be deleted: %s" % (path)):
			exit(0)

	def debug(self, level, message):
		if self.debug_level >= level:
			msg = self.replace_color("{{blue}}[{{bold}}DBG{{blue}}]{{nocolor}} %s" \
					% (message))
			print msg
