from netmiko import ConnectHandler

r1 = {
	"device_type" : "cisco_ios",
	"ip" : "192.168.99.1",
	"username" : "user",
	"password" : "user123"
}

conn = ConnectHandler(**r1)

print conn.send_command("show ip int br | i up")
