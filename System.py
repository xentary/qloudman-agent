import os.path
import subprocess

class System:
	def __init__(self):
		self.ostype = "apt"
		if (os.path.isfile("/etc/redhat-release")):
			self.ostype = "rpm"


	def do_update(self):
		if self.ostype == u"rpm":
			self.__yum("update", "-y")
		elif self.ostype == u"apt":
			self.__apt("update")
			self.__apt("upgrade") 
			
	def __yum(self, command, options = ""):
		cmd = "yum %s %s" % (options, command)
		self.__exec(cmd)

	def __apt(self, command, options = ""):
		cmd = "apt-get %s %s" % (options, command)
		self.__exec(cmd)

	def __exec(self, cmd):
		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in p.stdout.readlines():
			print line,
		retval = p.wait()