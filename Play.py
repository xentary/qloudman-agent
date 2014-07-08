import subprocess
import re


class Play:
	def __init__(self, command):
		self.command = command

	def is_responsible(self):
		if self.command.startswith(u"play-restart"):
			return True
		else:
			return False

	def execute(self):
		screen = re.match(r"(\d+)", self.command)
		print screen
		if screen:
			print screen.groups
		#print screen.groups()
			
