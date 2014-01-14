########################################
# Opens a file and apples the callback #
# function to every line. After it     #
# finishes reading, keeps watching for #
# new lines.                           #
########################################

import os
import time

class Watcher(object):
	
	def __init__(self,filename, callback):
	
		# check for right input and save vars
		if not os.path.exists(filename):
			raise IOError("File does not exists : %s" % filename)

		if not hasattr(callback, "__call__"):
			raise TypeError("%s: not a function" % callback)

		self.f = open(filename, 'r')
		self.callback = callback

		#read file for first time
		print 'Reading existent file...'
		self.read_lines()
		print 'Finished reading.'

	#blocking call to watch
	def watching(self, interval):
		print '<----------------------->\nStarted watching...\n'
		while 1:
			self.read_lines()
			time.sleep(interval)
			
	def read_lines(self):
		for line in self.f.readlines():
			self.callback(line)


