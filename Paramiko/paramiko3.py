import paramiko
import time

ip_list = ["192.168.99.1","192.168.99.2",
	   "192.168.99.3","192.168.99.4",
	   "192.168.99.5","192.168.99.6"]

username = "user"
password = "user123"

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for ip_address in ip_list:
	ssh_client.connect(hostname=ip_address,
			   username=username,
			   password=password)

	print "Success login to {0}".format(ip_address)
	conn = ssh_client.invoke_shell()

	conn.send("terminal length 0\n")
	conn.send("show run\n")
	time.sleep(1)
	output = conn.recv(65535)

	output_file = open("{0}.cfg".format(ip_address), "w")
	output_file.write(output)
	output_file.close()
	print "Config in {0} saved!!\n".format(ip_address)

	ssh_client.close()
