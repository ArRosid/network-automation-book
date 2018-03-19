from napalm_base import get_network_driver
import json

for x in range(1,7):
	driver = get_network_driver("ios")
	ios_r = driver("192.168.99.{0}".format(x),"user","user123")
	ios_r.open()

	r_arp = ios_r.get_arp_table()
	print "\nARP Table in R{0}".format(x)
	print json.dumps(r_arp,indent=3)
	ios_r.close()
