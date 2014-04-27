# LICENSE

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

	def set_debug_level(self, level):
		self.debug_level = level

	def step(self, message):
		print "%s[%s-%s]%s %s" \
			% (self._blue, self._white, self._blue, self._nocolor, message)

	def substep(self, message):
		print "    %s*%s %s" \
			% (self._white, self._nocolor, message)

	def display_config(self, config):
		pass

	def debug(self, level, message):
		if self.debug_level >= level:
			print "%s[%sDBG%s]%s %s" \
				% (self._blue, self._white, self._blue, self._nocolor, message)