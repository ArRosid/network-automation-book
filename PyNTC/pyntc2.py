from pyntc import ntc_device
import json

ios = ntc_device(host="192.168.99.1",
		 username="user",
		 password="user123",
		 device_type="cisco_ios_ssh")

ios.open()

ios_int = ios.show("show run int e0/0")

print ios_int
