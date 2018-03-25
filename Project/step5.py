import MySQLdb as mdb
import sys


try:
	sql_file = raw_input("Input SQL File(sql.txt): ") or "sql.txt"

except KeyboardInterrupt:
	print "\n\nProgram cancelled by user!"
	sys.exit()

def export_to_database():
	local_hostname = "R1"
	remote_hostname = ["R2","R3","R4"]
	local_int = ["eth1", "eth2", "eth3"]
	remote_int = ["eth1", "eth1", "eth1"]
	remote_ip = ["192.168.99.2", "192.168.99.3", "192.168.99.4"]
	remote_platform = ["cisco", "cisco", "cisco"]

	sql_data = open(sql_file,"r").readlines()
	sql_host = sql_data[0].strip()
	sql_username = sql_data[1].strip()
	sql_password = sql_data[2].strip()
	sql_database = sql_data[3].strip()

	sql_conn = mdb.connect(sql_host, sql_username, sql_password, sql_database)
	cursor = sql_conn.cursor()

	cursor.execute("Use CiscoData")


	### Export CDP Info ###
	for x in range(len(remote_hostname)):
		cursor.execute("INSERT INTO CDPInfo({},{},{},{},{},{}) VALUES ('{}','{}','{}','{}','{}','{}')".format(
					   "LocalHostname","RemoteHostname","LocalInterface","RemoteInterface","RemoteIP","RemotePlatform",
					   local_hostname,remote_hostname[x],local_int[x],remote_int[x],remote_ip[x],remote_platform[x]))

	sql_conn.commit()

export_to_database()