import telnetlib
import getpass

ip_in = raw_input("Enter IP Address file name: ")
user = raw_input("Enter your telnet username: ")
password = getpass.getpass()

ip_file = open(ip_in,"r")

device_list = ip_file.readlines()

for host in device_list:
	print "Configuring %s" % (host)
	tn = telnetlib.Telnet(host)

	tn.read_until("Username: ")
	tn.write(user + "\n")
	if password:
		tn.read_until("Password: ")
		tn.write(password + "\n")

	tn.write("conf t\n")
	tn.write("vlan 300\n")
	tn.write("name PythonVlan300\n")
	tn.write("end\n")
	tn.write("exit\n")

	print tn.read_all()
