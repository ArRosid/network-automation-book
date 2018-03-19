from pyntc import ntc_device
import json

ios = ntc_device(host="192.168.99.1",
		 username="user",
		 password="user123",
		 device_type="cisco_ios_ssh")

ios.open()

ios_facts = ios.facts

print json.dumps(ios_facts, indent=3)
