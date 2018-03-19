import telnetlib
import getpass

host = raw_input("Enter switch IP Address: ")
user = raw_input("Enter your telnet username: ")
password = getpass.getpass()

tn = telnetlib.Telnet(host)

tn.read_until("Username: ")
tn.write(user + "\n")
if password:
	tn.read_until("Password: ")
	tn.write(password + "\n")

tn.write("conf t\n")
tn.write("vlan 10\n")
tn.write("name PythonVlan10\n")
tn.write("vlan 20\n")
tn.write("name PythonVlan20\n")
tn.write("end\n")
tn.write("exit\n")

print tn.read_all()
