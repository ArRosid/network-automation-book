from netmiko import ConnectHandler

for x in range(2,7):
	device = {
		"device_type" : "cisco_ios",
		"ip" : "192.168.99.{0}".format(x),
		"username" : "user",
		"password" : "user123",
	}

	print "\nConfigure {0}".format(device["ip"])
	conn = ConnectHandler(**device)
	conn.enable()

	config_list = ["interface loopback0",
		       "ip add {0}.{1}.{2}.{3} 255.255.255.255".format(x,x,x,x)]

	print conn.send_config_set(config_list)
	print conn.send_command("sh ip int brief | i up")
