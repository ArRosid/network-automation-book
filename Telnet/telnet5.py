import telnetlib
import getpass

host = raw_input("Enter switch IP Address: ")
user = raw_input("Enter your telnet username: ")
password = getpass.getpass()

tn = telnetlib.Telnet(host,3001)

tn.read_until("Username: ")
tn.write(user + "\n")
if password:
	tn.read_until("Password: ")
	tn.write(password + "\n")

tn.write("sh run | section vty\n")
tn.write("exit\n")

print tn.read_all()
