def error_log(desc, msg):
	error_log = open("errors.log","a+")
	error_log.write("%s : %s" % (desc, msg) )
	error_log.close()

