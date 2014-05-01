# This file is part of pentoolbox.
# Please see LICENSE for details.

class Console(object):

	def __init__(self):
		self._nocolor = "\033[00m"
		self._white = "\033[00;01m"
		self._yellow = "\033[33;01m"
		self._green = "\033[32;01m"
		self._blue = "\033[34;01m"
		self._red = "\033[31;01m"

	def warning(self, message):
		print "%sWarning:%s %s" % (self._yellow, self._nocolor, message)

	def prompt(self, message=None):
		if self.force_mode:
			return True

		while True:
			if message:
				print message
			raw_answer = raw_input("Do you wish to continue ? [y/N] ")
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
		print "%s[%s-%s]%s %s" \
			% (self._blue, self._white, self._blue, self._nocolor, message)

	def substep(self, message):
		print "    %s*%s %s" \
			% (self._white, self._nocolor, message)

	def dump_config(self, config):
		self.step("Current configuration")
		self.substep("Log file: %s" % (config.log_file.name))
		self.substep("Install directory: %s" % (config.install_dir))
		self.substep("Path for binaries: %s" % (config.path_extension))

		print
		if not self.prompt():
			exit(0)

	def exists(self, path):
		if not self.prompt("File/dir exists and will be deleted: %s" % (path)):
			exit(0)

	def debug(self, level, message):
		if self.debug_level >= level:
			print "%s[%sDBG%s]%s %s" \
				% (self._blue, self._white, self._blue, self._nocolor, message)
