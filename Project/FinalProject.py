from napalm import get_network_driver
import json
import paramiko
import sys
import re
import time
import xlsxwriter
from getpass import getpass
import MySQLdb as mdb


try:
	ip_file = raw_input("Input IP Address File(ip.txt): ") or "ip.txt"
	sql_file = raw_input("Input SQL File(sql.txt): ") or "sql.txt"
	username = raw_input("Input username: ")
	password = getpass()
	export_excel = raw_input("Export to excel(yes)? ") or "yes"
	export_database = raw_input("Export to database(yes)? ") or "yes"

except KeyboardInterrupt:
	print "\n\nProgram cancelled by user!"
	sys.exit()


os_version = ""
uptime = ""
vendor = ""
serial_number = ""
hostname = ""
fqdn = ""
def gather_basic_info(ip):
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
	#print json.dumps(ios_r_facts, indent=3)


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
	uptime = ios_r_facts["uptime"]
	vendor = ios_r_facts["vendor"]
	serial_number = ios_r_facts["serial_number"]
	hostname = ios_r_facts["hostname"]
	fqdn = ios_r_facts["fqdn"]

	ios_r.close()


interface_list = []
address_list = []
prefix_list = []
mac_list = []
description_list = []
router_hostname = ""

def gather_int_info(ip):
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

	#gather interface list
	interface_list = []

	for iface,info in ios_r_int_ip.iteritems():
		interface_list.append(iface)

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


	#gather mac address & description
	mac_list = []
	description_list = []
	for interface in interface_list:
		mac_list.append(ios_r_int[interface]["mac_address"])
		description_list.append(ios_r_int[interface]["description"])
	
	#close the connection
	ios_r.close()


##### GET Neighbor Information ######
remote_hostname = []
local_int = []
remote_int = []
remote_ip = []
remote_platform = []
local_hostname = ""

def gather_cdp_info(ip):
	global remote_hostname
	global local_int
	global remote_int
	global remote_ip
	global remote_platform
	global local_hostname

	session = paramiko.SSHClient()
	session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	session.connect(ip, username=username, password=password)
	connection = session.invoke_shell()

	connection.send("terminal length 0\nsh cdp neighbor detail\n")
	time.sleep(1)

	#save the result to the output var
	output = connection.recv(65535)
	
	## R1#
	#Local Hostname
	def_local_hostname = re.search(r"(.+)\#", output)
	local_hostname = def_local_hostname.group(1)

	#Remote Hostname
	#Device ID: R4.idn.id
	remote_hostname = re.findall(r"Device ID: (.+)",output)

	#Local Interface
	#Interface: FastEthernet0/0,  Port ID (outgoing port): Ethernet0/0
	local_int = re.findall(r"Interface: (.+)\,", output)

	#Remote Interfaces
	remote_int = re.findall(r"\(outgoing port\): (.+)", output)

	#Remote IP Address
	#  IP address: 192.168.99.4
	remote_ip = re.findall(r"IP address: (.+)", output)

	#Remote Platforrm
	#Platform: Linux Unix,  Capabilities: Router 
	remote_platform = re.findall(r"Platform: (.+)\,", output)

	session.close()


def export_to_excel():
	#create a file
	workbook = xlsxwriter.Workbook('Cisco Data.xlsx')

	#create a bold format
	bold = workbook.add_format({'bold' : True})


	#open ip file
	address = open(ip_file,"r").readlines()


	### Export basic info ####
	col = 0
	row = 1

	#create a worksheet for basic info
	basic_info_worksheet = workbook.add_worksheet('Basic Info')

	#create a header
	basic_info_worksheet.write("A1", "Hostname", bold)
	basic_info_worksheet.write("B1", "Vendor", bold)
	basic_info_worksheet.write("C1", "OS Version", bold)
	basic_info_worksheet.write("D1", "Serial Number", bold)
	basic_info_worksheet.write("E1", "FQDN", bold)
	basic_info_worksheet.write("F1", "Uptime", bold)


	for ip in address:
		print "Writing basic info for {} to excel".format(ip)
		gather_basic_info(ip)
		basic_info_worksheet.write(row, col, hostname)
		basic_info_worksheet.write(row, col + 1, vendor)
		basic_info_worksheet.write(row, col + 2, os_version)
		basic_info_worksheet.write(row, col + 3, serial_number)
		basic_info_worksheet.write(row, col + 4, fqdn)
		basic_info_worksheet.write(row, col + 5, uptime)
		row += 1

	##### Export interface info ######
	col = 0
	row = 1

	#create a worksheet for interface info
	int_info_worksheet = workbook.add_worksheet('Interface Info')

	#write a header
	int_info_worksheet.write("A1", "Hostname", bold)
	int_info_worksheet.write("B1", "Interface", bold)
	int_info_worksheet.write("C1", "IP Address", bold)
	int_info_worksheet.write("D1", "Prefix", bold)
	int_info_worksheet.write("E1", "MAC Address", bold)
	int_info_worksheet.write("F1", "Description", bold)

	for ip in address:
		print "Writing Interface Info for {} to excel".format(ip)
		gather_int_info(ip)
		int_info_worksheet.write(row, col, router_hostname)

		for x in range(len(interface_list)):
			int_info_worksheet.write(row, col + 1, interface_list[x])
			int_info_worksheet.write(row, col + 2, address_list[x])
			int_info_worksheet.write(row, col + 3, prefix_list[x])
			int_info_worksheet.write(row, col + 4, mac_list[x])
			int_info_worksheet.write(row, col + 5, description_list[x])
			row += 1


	### Export CDP Info ####
	col = 0
	row = 1

	#create worksheet for CDP Info
	cdp_info_worksheet = workbook.add_worksheet('CDP Info')

	#create a header
	cdp_info_worksheet.write("A1", "Local Hostname", bold)
	cdp_info_worksheet.write("B1", "Remote Hostname", bold)
	cdp_info_worksheet.write("C1", "Local Interface", bold)
	cdp_info_worksheet.write("D1", "Remote Interface", bold)
	cdp_info_worksheet.write("E1", "Remote IP Address", bold)
	cdp_info_worksheet.write("F1", "Remote Platform", bold)

	for ip in address:
		print "Writing CDP Neighbor Information for {} to excel".format(ip)
		gather_cdp_info(ip)

		cdp_info_worksheet.write(row, col, local_hostname)

		for x in range(len(remote_hostname)):
			cdp_info_worksheet.write(row, col + 1, remote_hostname[x])
			cdp_info_worksheet.write(row, col + 2, local_int[x])
			cdp_info_worksheet.write(row, col + 3, remote_int[x])
			cdp_info_worksheet.write(row, col + 4, remote_ip[x])
			cdp_info_worksheet.write(row, col + 5, remote_platform[x])
			row += 1


def export_to_database():
	address = open(ip_file,"r").readlines()
	sql_data = open(sql_file,"r").readlines()
	sql_host = sql_data[0].strip()
	sql_username = sql_data[1].strip()
	sql_password = sql_data[2].strip()
	sql_database = sql_data[3].strip()

	sql_conn = mdb.connect(sql_host, sql_username, sql_password, sql_database)
	cursor = sql_conn.cursor()

	cursor.execute("Use CiscoData")

	#### Export Basic Info ###
	for ip in address:
		print "Writing Basic Info for {} to database".format(ip)
		gather_basic_info(ip)
		cursor.execute("INSERT INTO BasicInfo({},{},{},{},{},{}) VALUES ('{}','{}','{}','{}','{}','{}')".format(
					   "OSVersion","Uptime","Vendor","SerialNumber","Hostname","FQDN",
					   os_version, uptime, vendor, serial_number, hostname, fqdn))


	### Export Interface Info ###
	for ip in address:
		print "Writing Interface Info for {} to database".format(ip)
		gather_int_info(ip)
		for x in range(len(address_list)):
			cursor.execute("INSERT INTO InterfaceInfo({},{},{},{},{},{}) VALUES ('{}','{}','{}','{}','{}','{}')".format(
						   "Hostname","Interface","IPAddress","Prefix","MACAddress","Description",
						   router_hostname, interface_list[x],address_list[x],prefix_list[x],mac_list[x],description_list[x]))

	### Export CDP Info ###
	for ip in address:
		print "Writing CDP Info for {} to database".format(ip)
		gather_cdp_info(ip)
		for x in range(len(remote_hostname)):
			cursor.execute("INSERT INTO CDPInfo({},{},{},{},{},{}) VALUES ('{}','{}','{}','{}','{}','{}')".format(
						   "LocalHostname","RemoteHostname","LocalInterface","RemoteInterface","RemoteIP","RemotePlatform",
						   local_hostname,remote_hostname[x],local_int[x],remote_int[x],remote_ip[x],remote_platform[x]))

	sql_conn.commit()
def main():
	if export_excel == "yes":
		export_to_excel()
	if export_database == "yes":
		export_to_database()
	else:
		print "Nothing to do!"

main()