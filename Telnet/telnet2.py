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
for x in range(2,11):
	tn.write("vlan " + str(x) + "\n")
	tn.write("name PythonVlan" + str(x) + "\n")

tn.write("end\n")
tn.write("exit\n")

print tn.read_all()
