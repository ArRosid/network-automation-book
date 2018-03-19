import telnetlib
import getpass

user = raw_input("Enter your telnet username: ")
password = getpass.getpass()

device_list = ["192.168.99.1","192.168.99.2",
			   "192.168.99.3","192.168.99.4"]

for host in device_list:
	print "Configuring %s" % (host)
	tn = telnetlib.Telnet(host)

	tn.read_until("Username: ")
	tn.write(user + "\n")
	if password:
		tn.read_until("Password: ")
		tn.write(password + "\n")

	tn.write("conf t\n")
	tn.write("vlan 100\n")
	tn.write("name PythonVlan100\n")
	tn.write("vlan 200\n")
	tn.write("name PythonVlan200\n")
	tn.write("end\n")
	tn.write("exit\n")

	print tn.read_all()
