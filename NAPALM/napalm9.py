from napalm_base import get_network_driver

driver = get_network_driver("ios")
ios_r = driver("192.168.99.1",
	"user","user123",
	optional_args={"port":2222,
		       "dest_file_system":"nvram:"})

ios_r.open()

ios_r.load_merge_candidate(filename="confR1.txt")

print ios_r.compare_config()

ios_r.commit_config()

ios_r.close()
