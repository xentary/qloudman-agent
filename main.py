import pika
import socket
import ConfigParser, os
import httplib

from Play import Play
from System import System

hostname = socket.gethostname()

config = ConfigParser.ConfigParser()
config.read(["qloudman.cfg", "/etc/qloudman.cfg"])

def receive_command(command):
	s = System(command)
	if s.is_responsible():
		s.execute()
		return

	s = Play(command)
	if s.is_responsible():
		s.execute()
		return


#receive_command(u"system-update")

def callback(ch, method, properties, body):
	print "Message received: %r" % (body,)
	receive_command(body)



# Register at server
conn = httplib.HTTPConnection(config.get("main", "server"), config.getint("main", "port"));
conn.request("GET", "/api/register_node/%s" % hostname)
response = conn.getresponse()
print response.status, response.reason


connection = pika.BlockingConnection(pika.ConnectionParameters(config.get("broadcast", "server"), config.getint("broadcast", "port")))
channel = connection.channel()

agent_queue = 'node-%s' % hostname

print agent_queue

channel.queue_declare(queue='broadcast')
channel.queue_declare(queue=agent_queue)

channel.basic_consume(callback, queue='broadcast', no_ack=True)
channel.basic_consume(callback, queue=agent_queue, no_ack=True)

channel.start_consuming()
