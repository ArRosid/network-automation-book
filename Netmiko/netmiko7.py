from netmiko import ConnectHandler

file_ip = open("ip.txt", "r")
list_ip = file_ip.readlines()

for ip in list_ip:
	device = {
		"device_type" : "cisco_ios",
		"ip" : ip,
		"username" : "user",
		"password" : "user123",
	}

	print "\nLogin to {0}".format(ip.strip("\n"))
	conn = ConnectHandler(**device)

	versi = conn.send_command("sh version")

	versi_file = open("v{0}.txt".format(ip.rstrip("\n")), "w")
	versi_file.write(versi)
	versi_file.close()
	print "Versi {0} tersimpan!!".format(ip.rstrip("\n"))
