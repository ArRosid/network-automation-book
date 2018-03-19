import paramiko
import time

ip_address = "192.168.99.1"
username = "user"
password = "user123"

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_client.connect(hostname=ip_address,
		   username=username,
		   password=password,
		   port=2222)

print "Success login to {0}".format(ip_address)
conn = ssh_client.invoke_shell()

conn.send("terminal length 0\n")
conn.send("show ip int brief | i up\n")
time.sleep(1)

output = conn.recv(65535)
print output

ssh_client.close()
