from napalm_base import get_network_driver

driver = get_network_driver("ios")
ios_r = driver("192.168.99.1",
	"user","user123",
	optional_args={"port":2222,
		       "dest_file_system":"nvram:"})

ios_r.open()

ios_r.load_merge_candidate(filename="confR1.txt")

compare = ios_r.compare_config()

if len(compare) > 0:
	compare_file = open("log.txt","w")
	compare_file.write(compare)
	compare_file.close()
	ios_r.commit_config()
	print "Configuration Saved!!"

else:
	print "No Change Required!!"
	ios_r.discard_config()

ios_r.close()
