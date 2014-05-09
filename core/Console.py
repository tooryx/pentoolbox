# This file is part of pentoolbox.
# Please see LICENSE for details.

class Console(object):

	def __init__(self):
		"""
		Instanciate the tool and its colors.
		"""
		self._nocolor = "\033[00m"
		self._bold = "\033[00;01m"
		self._yellow = "\033[33;01m"
		self._green = "\033[32;01m"
		self._blue = "\033[34;01m"
		self._red = "\033[31;01m"

	def replace_color(self, message):
		"""
		A few tags has been defined to allow colorization of output.
		This function is responsible for replacing those tags.

		Parameters
			message: The message in which tags are to be replaced

		Return value
			The string with replaced tags
		"""
		message = message.replace("{{nocolor}}", self._nocolor)
		message = message.replace("{{bold}}", self._bold)
		message = message.replace("{{yellow}}", self._yellow)
		message = message.replace("{{green}}", self._green)
		message = message.replace("{{blue}}", self._blue)
		message = message.replace("{{red}}", self._red)

		return message

	def warning(self, message):
		"""
		Issue a warning to the user.

		Parameters
			message: Message of the warning.
		"""
		msg = self.replace_color("{{red}}[{{yellow}}!{{red}}]{{nocolor}} %s" \
			% (message))
		print msg

	def prompt(self, message=None):
		"""
		Ask the user if he wish to continue.

		Parameters
			message: The question to ask. Example: Continue ?
		"""
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
		"""
		Setter to change current debug level.

		Parameters
			level: Debug level to be set.
		"""
		self.debug_level = level

	def set_force_mode(self, force_mode):
		"""
		Setter to change to force mode.
		This force yes to all prompt() questions.

		Parameters
			force_mode: Force mode ? (bool)
		"""
		self.force_mode = force_mode

	def step(self, message):
		"""
		Print a major step of the program progress.

		Parameters
			message: The step message.
		"""
		print
		msg = self.replace_color("{{blue}}[{{bold}}-{{blue}}]{{nocolor}} %s" \
			% (message))
		print msg

	def substep(self, message):
		"""
		Print a substep (will be under major steps) of the program progress.

		Parameters
			message: The substep message.
		"""
		msg = self.replace_color("    {{bold}}*{{nocolor}} %s" % (message))
		print msg

	def banner(self):
		"""
		Display the banner.
		"""
		print """
	         PENTOOLBOX
	 '------------------------'
	  |__ '==' ------ '==' __|
	    |                  |
	    |__________________|
		"""

	def dump_config(self, config):
		"""
		Prints the current configuration.

		Parameters
			config: The configuration to be dumped.
		"""
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
		"""
		Prints the list of currently installed tools.

		Parameters
			config: The configuration to search installed tools in.
		"""
		self.step("Installed tools")

		for tool in config.tools_installed:
			self.substep("%s" % (tool))

		print

	def exists(self, path):
		"""
		Ask the user before deleting a file.

		Parameters
			path: Path to the file to be deleted.
		"""
		if not self.prompt("File/dir exists and will be deleted: %s" % (path)):
			exit(1)

	def debug(self, level, message):
		"""
		Print a debug message.

		Parameters
			level: Minimum debug level to display message
			message: Message to be displayed
		"""
		if self.debug_level >= level:
			msg = self.replace_color("{{blue}}[{{bold}}DBG{{blue}}]{{nocolor}} %s" \
					% (message))
			print msg
