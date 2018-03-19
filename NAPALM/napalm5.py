from napalm_base import get_network_driver
import json

for x in range(1,7):
	driver = get_network_driver("ios")
	ios_r = driver("192.168.99.{0}".format(x),"user","user123")
	ios_r.open()

	r_ip = ios_r.get_interfaces_ip()
	print "\nIP Address in R{0}".format(x)
	print json.dumps(r_ip,indent=3)
	ios_r.close()
