from pyntc import ntc_device
import json

ios = ntc_device(host="192.168.99.1",
		 username="user",
		 password="user123",
		 device_type="cisco_ios_ssh")

ios.open()

commands = ["sh run int e0/0",
	    "sh ip int brief | i up",
	    "sh clock"]

ios_data = ios.show_list(commands)

for line in ios_data:
	print line
