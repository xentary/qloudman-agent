import subprocess
import re


class Qloudman:
	def __init__(self, command):
		self.command = command

	def is_responsible(self):
		if self.command.startswith(u"self-update"):
			return True
		else:
			return False

	def execute(self):
		p = subprocess.Popen("git pull", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in p.stdout.readlines():
			print line,
		retval = p.wait()
			
