from napalm import get_network_driver
from getpass import getpass
import json
import sys

try:
	ip = raw_input("Input IP Address: ")
	username = raw_input("Input username: ")
	password = getpass()

except KeyboardInterrupt:
	print "\n\nProgram cancelled by user!"
	sys.exit()


interface_list = []
address_list = []
prefix_list = []
mac_list = []
description_list = []
router_hostname = ""

def gather_int_info():
	global interface_list
	global address_list
	global prefix_list
	global mac_list
	global description_list
	global router_hostname

	driver = get_network_driver("ios")
	ios_r = driver(ip,username,password)
	ios_r.open()

	ios_r_int_ip = ios_r.get_interfaces_ip()
	print json.dumps(ios_r_int_ip, indent=3)

	'''
	{
	   "Ethernet0/0": {
	      "ipv4": {
	         "192.168.99.9": {
	            "prefix_length": 24
	         }
	      }
	   }
	}

	'''

	ios_r_int = ios_r.get_interfaces()
	print json.dumps(ios_r_int, indent=3)

	'''
	{
	   "Ethernet1/0": {
	      "is_enabled": false, 
	      "description": "", 
	      "last_flapped": -1.0, 
	      "is_up": false, 
	      "mac_address": "AA:BB:CC:00:01:01", 
	      "speed": 10
	   }, 
	   "Ethernet1/1": {
	      "is_enabled": false, 
	      "description": "", 
	      "last_flapped": -1.0, 
	      "is_up": false, 
	      "mac_address": "AA:BB:CC:00:01:11", 
	      "speed": 10
	   }, 

	'''


	#get hostname
	router_hostname = ios_r.get_facts()["hostname"]
	print router_hostname

	#gather interface list
	interface_list = []

	for iface,info in ios_r_int_ip.iteritems():
		interface_list.append(iface)
	print interface_list

	#gather ip address & prefix
	address_list = []
	prefix_list = []


	{
	   "Ethernet0/0": {
	      "ipv4": {
	         "192.168.99.9": {
	            "prefix_length": 24
	         }
	      }
	   }
	}


	for iface,info in ios_r_int_ip.iteritems():
		for add_ver,ip_prefix in info.iteritems():
			if add_ver == "ipv4":
				for ipaddr,prefix_info in ip_prefix.iteritems():
					address_list.append(ipaddr)
					for prefix_lngth,prefix in prefix_info.iteritems():
						prefix_list.append(prefix)

			else:
				continue
	
	print address_list
	print prefix_list

	#gather mac address & description
	mac_list = []
	description_list = []
	for interface in interface_list:
		mac_list.append(ios_r_int[interface]["mac_address"])
		description_list.append(ios_r_int[interface]["description"])
	
	print mac_list
	#close the connection
	ios_r.close()

gather_int_info()