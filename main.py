import pika
import socket
import ConfigParser, os

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

connection = pika.BlockingConnection(pika.ConnectionParameters(config.get("main", "server")))
channel = connection.channel()

agent_queue = 'agent-%s' % hostname

channel.queue_declare(queue='broadcast')
channel.queue_declare(queue=agent_queue)

channel.basic_consume(callback, queue='broadcast', no_ack=True)
channel.basic_consume(callback, queue=agent_queue, no_ack=True)

channel.start_consuming()
