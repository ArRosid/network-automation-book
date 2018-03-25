import paramiko
import sys
from getpass import getpass
import time
import re

try:
	ip = raw_input("Input IP Address: ")
	username = raw_input("Input username: ")
	password = getpass()

except KeyboardInterrupt:
	print "\n\nProgram cancelled by user!"
	sys.exit()

def gather_cdp_info():
	global remote_hostname
	global local_int
	global remote_int
	global remote_ip
	global remote_platform
	global local_hostname

	session = paramiko.SSHClient()
	session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	session.connect(ip, username=username, password=password, allow_agent=False,look_for_keys=False)
	connection = session.invoke_shell()

	connection.send("terminal length 0\nsh cdp neighbor detail\n")
	time.sleep(1)

	#save the result to the output var
	output = connection.recv(65535)
	
	## R1#
	#Local Hostname
	def_local_hostname = re.search(r"(.+)\#", output)
	local_hostname = def_local_hostname.group(1)
	print local_hostname

	#Remote Hostname
	#Device ID: R4.idn.id
	remote_hostname = re.findall(r"Device ID: (.+)",output)
	print remote_hostname

	#Local Interface
	#Interface: FastEthernet0/0,  Port ID (outgoing port): Ethernet0/0
	local_int = re.findall(r"Interface: (.+)\,", output)
	print local_int

	#Remote Interfaces
	remote_int = re.findall(r"\(outgoing port\): (.+)", output)
	print remote_int

	#Remote IP Address
	#  IP address: 192.168.99.4
	remote_ip = re.findall(r"IP address: (.+)", output)
	print remote_ip

	#Remote Platforrm
	#Platform: Linux Unix,  Capabilities: Router 
	remote_platform = re.findall(r"Platform: (.+)\,", output)
	print remote_platform

	session.close()

gather_cdp_info()