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


os_version = ""
uptime = ""
vendor = ""
serial_number = ""
hostname = ""
fqdn = ""
def gather_basic_info():
	global os_version
	global uptime
	global vendor
	global serial_number
	global hostname
	global fqdn

	driver = get_network_driver("ios")
	ios_r = driver(ip,username,password)
	ios_r.open()

	ios_r_facts = ios_r.get_facts()
	print json.dumps(ios_r_facts, indent=3)


	'''
	{
	   "os_version": "2600 Software (C2691-ADVENTERPRISEK9-M), Version 12.4(15)T1, RELEASE SOFTWARE (fc2)", 
	   "uptime": 27720, 
	   "interface_list": [
	      "FastEthernet0/0", 
	      "FastEthernet0/1", 
	      "Loopback0"
	   ], 
	   "vendor": "Cisco", 
	   "serial_number": "XXXXXXXXXXX", 
	   "model": "2691", 
	   "hostname": "R1", 
	   "fqdn": "R1.idn.id"
	}

	'''

	### Grab the info
	os_version = ios_r_facts["os_version"]
	print os_version

	uptime = ios_r_facts["uptime"]
	print uptime

	vendor = ios_r_facts["vendor"]
	print vendor

	serial_number = ios_r_facts["serial_number"]
	print serial_number

	hostname = ios_r_facts["hostname"]
	print hostname

	fqdn = ios_r_facts["fqdn"]
	print fqdn

	ios_r.close()

gather_basic_info()