from pyntc import ntc_device

for x in range (1,7):
	ios = ntc_device(host="192.168.99.%s" % (x),
			 username="user",
			 password="user123",
	  		 device_type="cisco_ios_ssh")

	ios.open()

	ios.backup_running_config("R%s.cfg" % (x))
print "All backup saved!!"
