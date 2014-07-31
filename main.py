import pika
import socket
import ConfigParser, os
import httplib
import requests
import json

from Play import Play
from Qloudman import Qloudman
from System import System

hostname = socket.gethostname()

config = ConfigParser.ConfigParser()
config.read(["qloudman.cfg", "/etc/qloudman.cfg"])

def receive_command(command):
	parts = command.split("|")
	command = parts[0]
	cmdid = parts[1]

	s = Qloudman(command)
	if s.is_responsible():
		(retval,result) = s.execute()
		
	s = System(command)
	if s.is_responsible():
		(retval,result) = s.execute()
		
	s = Play(command)
	if s.is_responsible():
		(retval,result) = s.execute()
		
	payload = {"node": hostname, "cmdid": cmdid, "retval": retval, "result": result}
	print payload

	url = "http://%s:%i/api/cmd_result" % (config.get("main", "server"), config.getint("main", "port"))
	r = requests.post(url, data=payload)
	print r.status_code

def callback(ch, method, properties, body):
	print "Message received: %r" % (body,)
	receive_command(body)



# Register at server
url = "http://%s:%i/api/register_node/%s" % (config.get("main", "server"), config.getint("main", "port"),  hostname)
response = requests.get(url)
print response.status_code, response.text


connection = pika.BlockingConnection(pika.ConnectionParameters(config.get("broadcast", "server"), config.getint("broadcast", "port")))
channel = connection.channel()

agent_queue = 'node-%s' % hostname

print agent_queue

channel.queue_declare(queue='broadcast')
channel.queue_declare(queue=agent_queue)

channel.basic_consume(callback, queue='broadcast', no_ack=True)
channel.basic_consume(callback, queue=agent_queue, no_ack=True)

channel.start_consuming()
