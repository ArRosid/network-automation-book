from pyntc import ntc_device
import json

ios = ntc_device(host="192.168.99.1",
		 username="user",
		 password="user123",
		 device_type="cisco_ios_ssh")

ios.open()

conf_list = ["int loopback0",
	     "ip add 1.1.1.1 255.255.255.255",
	     "int loopback1",
	     "ip add 2.2.2.2 255.255.255.255"]

ios.config_list(conf_list)

print ios.show("show ip int brief | i up")
