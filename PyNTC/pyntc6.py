from pyntc import ntc_device

ios = ntc_device(host="192.168.99.1",
		 username="user",
		 password="user123",
		 device_type="cisco_ios_ssh")

ios.open()

ios.backup_running_config("R1.cfg")
