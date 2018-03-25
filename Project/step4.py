import xlsxwriter


def export_to_excel():
	local_hostname = "R1"
	remote_hostname = ["R2","R3","R4"]
	local_int = ["eth1", "eth2", "eth3"]
	remote_int = ["eth1", "eth1", "eth1"]
	remote_ip = ["192.168.99.2", "192.168.99.3", "192.168.99.4"]
	remote_platform = ["cisco", "cisco", "cisco"]
	
	#create a file
	workbook = xlsxwriter.Workbook('Cisco Data.xlsx')

	#create a bold format
	bold = workbook.add_format({'bold' : True})

	### Export basic info ####
	col = 0
	row = 1

	#create worksheet for CDP Info
	cdp_info_worksheet = workbook.add_worksheet('CDP Info')

	#create a header
	cdp_info_worksheet.write("A1", "Local Hostname", bold)
	cdp_info_worksheet.write("B1", "Remote Hostname", bold)
	cdp_info_worksheet.write("C1", "Local Interface", bold)
	cdp_info_worksheet.write("D1", "Remote Interface", bold)
	cdp_info_worksheet.write("E1", "Remote IP Address", bold)
	cdp_info_worksheet.write("F1", "Remote Platform", bold)


	cdp_info_worksheet.write(row, col, local_hostname)

	for x in range(len(remote_hostname)):
		cdp_info_worksheet.write(row, col + 1, remote_hostname[x])
		cdp_info_worksheet.write(row, col + 2, local_int[x])
		cdp_info_worksheet.write(row, col + 3, remote_int[x])
		cdp_info_worksheet.write(row, col + 4, remote_ip[x])
		cdp_info_worksheet.write(row, col + 5, remote_platform[x])
		row += 1

export_to_excel()