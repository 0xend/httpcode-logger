#!/usr/bin/env python

######################################
# Watches a log file and sends the   #
# updates to an instance of graphite.#
# It monitors the num. of ocurrences #
# of each http status code.      	 #
######################################

import re
import sys
import time
from watcher import Watcher
from graphite import Graphite
from helper import error_log

class CodeLoger():

	
	INTERVAL = 1 #check for new logs every second
	POSSIBLE_VALUES = 5 # 1xx, 2xx, 3xx, 4xx, 5xx

	def __init__(self,server,port,log):

		self.last_updated = 0	
		self.__init_ocurrences()
		self.graphite = Graphite(server, port)

		w = Watcher(log, self.count)
		w.watching(self.INTERVAL)
	

	# manage new log
	def count(self, line):
		
		search_code = re.search(".* HTTP/1.\d\" (\d{3}) .*", line)
		search_date = re.search(".* - \[(\d{2}/[a-zA-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} \+0000)\].*", line)
		
		if not search_code or not search_date:
			error_log("Log has wrong format", line)		
		else:
			code_no = int(search_code.group(1))
			t = time.strptime(search_date.group(1),"%d/%b/%Y:%H:%M:%S +0000")
			timestamp = time.mktime(t)

			#update for first timestamp
			if self.last_updated == 0:
				self.last_updated = timestamp

			self.update(code_no, timestamp) 
	
	
	def update(self, code_no, timestamp):
		#compute number of ocurrences in intervals
		if timestamp - self.last_updated > 0:
			self.last_updated = timestamp
			self.send(timestamp)
			self.__init_ocurrences()
		self.ocurrences[self.__stat_index(code_no)] += 1
	
	def send(self, timestamp):
		codes = []
		for i in range(0, self.POSSIBLE_VALUES):
			metric = "test.codes.%dxx" % (i+1)
			value = self.ocurrences[i]
			codes.append(self.graphite.prepare(metric, value, timestamp))
		message = '\n'.join(codes) + '\n'
		self.graphite.send(message)	
	
	def __init_ocurrences(self):
		self.ocurrences = {}
		for i in range(0, self.POSSIBLE_VALUES):
			self.ocurrences[i] = 0

	#map between codes and index in dict
	def __stat_index(self, code_no):
		if code_no < 100 or code_no > 599:
			error_log("Code extracted is invalid", " code = %d " % code_no)
		elif code_no < 200:
			return  0
		elif code_no < 300:
			return 1
		elif code_no < 400:
			return 2
		elif code_no < 500:
			return 3
		else:
			return 4

		

if __name__ == "__main__":
	
	if len(sys.argv) != 2:
		print "python codeloger.py <server> <port> <xxx.log>"
		sys.exit(1)
	l = CodeLoger(sys.argv[1], int(sys.argv[2]),sys.argv[3])
	#l = CodeLoger("/var/log/challenge/example.log")

