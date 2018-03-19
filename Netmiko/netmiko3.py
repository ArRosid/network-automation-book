from netmiko import ConnectHandler

r1 = {
	"device_type" : "cisco_ios",
	"ip" : "192.168.99.1",
	"username" : "user",
	"password" : "user123",
	"port" : 2222,
	"secret" : "cisco"
}

conn = ConnectHandler(**r1)
conn.enable()

config_list = ["interface loopbac1",
	       "ip add 11.11.11.11 255.255.255.255"]

print conn.send_config_set(config_list)

print conn.send_command("sh ip int brief | i up")
