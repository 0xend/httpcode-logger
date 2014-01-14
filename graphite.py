####################################
# Creates a socket to connect to a #
# graphite instance. 				  #
# Prepare formats the input into a #
# graphite message and send, sends #
# it.										  #
####################################

import socket

class Graphite(object):
	
	#create socket
	def __init__(self, server, port):
		self.sock = socket.socket()
		self.sock.connect( (server, port) )

	#close socket
	def close():
		self.sock.close()

	#format message given the necessary args
	def prepare(self, metric, value, timestamp):
		return "%s %d %d\n" % (metric, value, timestamp)
	
	#send message through the socket
	def send(self, msg):
		self.sock.sendall(msg)

