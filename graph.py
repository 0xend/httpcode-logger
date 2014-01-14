import socket
import time
import sys

CARBON_SERVER = 'ec2-23-20-215-47.compute-1.amazonaws.com'
CARBON_PORT = 2003

message = 'test.stat.1 %d %d\n' % (int(sys.argv[1]), int(time.time()))

print 'sending message:\n%s' % message
sock = socket.socket()
sock.connect((CARBON_SERVER, CARBON_PORT))
sock.sendall(message)
sock.close()
