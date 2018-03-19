from netmiko import ConnectHandler

for x in range(2,7):
	device = {
		"device_type" : "cisco_ios",
		"ip" : "192.168.99.{0}".format(x),
		"username" : "user",
		"password" : "user123",
	}

	print "Int info in {0}".format(device["ip"])
	conn = ConnectHandler(**device)
	conn.enable()

	print conn.send_command("sh ip int brief | i up")