from napalm_base import get_network_driver
import json

for x in range(1,7):
	print "\nConnecting to R{0}".format(x)
	driver = get_network_driver("ios")
	ios_r = driver("192.168.99.{0}".format(x),"user","user123")
	ios_r.open()

	r_config = ios_r.get_config()

	print "Backup running conf R{0}".format(x)
	runn_conf = r_config["running"]

	runn_file = open("running_R{0}".format(x),"w")
	runn_file.write(runn_conf)
	runn_file.close()

	print "Backup startup conf R{0}".format(x)
	start_conf = r_config["startup"]

	start_file = open("startup_R{0}".format(x),"w")
	start_file.write(start_conf)
	start_file.close()

	ios_r.close()
