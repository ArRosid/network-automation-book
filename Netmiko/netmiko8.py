from netmiko import ConnectHandler
from getpass import getpass

ip_input = raw_input("Masukkan file IP: ")
username = raw_input("Masukkan username: ")
password = getpass()


file_ip = open(ip_input, "r")
list_ip = file_ip.readlines()

for ip in list_ip:
	device = {
		"device_type" : "cisco_ios",
		"ip" : ip,
		"username" : username,
		"password" : password,
	}

	print "\nLogin to {0}".format(ip.rstrip("\n"))
	conn = ConnectHandler(**device)

	versi = conn.send_command("sh version")

	versi_file = open("v{0}.txt".format(ip.rstrip("\n")), "w")
	versi_file.write(versi)
	versi_file.close()
	print "Versi {0} tersimpan!!".format(ip.rstrip("\n"))
