from netmiko import ConnectHandler

r1 = {
	"device_type" : "cisco_ios",
	"ip" : "192.168.99.1",
	"username" : "user",
	"password" : "user123",
	"port" : 2222,
	"secret" : "cisco"
}
r2 = {
	"device_type" : "cisco_ios",
	"ip" : "192.168.99.2",
	"username" : "user",
	"password" : "user123",
}
r3 = {
	"device_type" : "cisco_ios",
	"ip" : "192.168.99.3",
	"username" : "user",
	"password" : "user123",
}
r4 = {
	"device_type" : "cisco_ios",
	"ip" : "192.168.99.4",
	"username" : "user",
	"password" : "user123",
}
r5 = {
	"device_type" : "cisco_ios",
	"ip" : "192.168.99.5",
	"username" : "user",
	"password" : "user123",
}
r6 = {
	"device_type" : "cisco_ios",
	"ip" : "192.168.99.6",
	"username" : "user",
	"password" : "user123",
}

device_list = [r1,r2,r3,r4,r5,r6]

for device in device_list:
	print "Int info in {0}".format(device["ip"])
	conn = ConnectHandler(**device)
	conn.enable()

	print conn.send_command("sh ip int brief | i up")
