import socket

from System import System


hostname = socket.gethostname()

def receive_command(command):
	if (command == u"system-update"):
		do_system_update()

def do_system_update():
	s = System()
	s.do_update()


receive_command(u"system-update")