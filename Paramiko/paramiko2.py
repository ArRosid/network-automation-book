import paramiko
import time
import getpass

ip_address = raw_input("Masukkan IP Address: ")
username = raw_input("Masukkann Username: ")
password = getpass.getpass()

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip_address,username=username, password=password)

print "Success login to {0}".format(ip_address)
conn = ssh_client.invoke_shell()

conn.send("terminal length 0\n")
conn.send("show run\n")
time.sleep(1)
output = conn.recv(65535)

output_file = open("{0}.cfg".format(ip_address), "w")
output_file.write(output)
output_file.close()
print "Config in {0} saved!!".format(ip_address)
ssh_client.close()
