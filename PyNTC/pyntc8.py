from pyntc import ntc_device

ios = ntc_device(host="192.168.99.1",
		 username="user",
		 password="user123",
  		 device_type="cisco_ios_ssh",
		 port=2222)

ios.open()
print ios.show("show clock")
