# LswBareIPsFinder
# v1.0
# Dimofinf, Inc
# # # # # # # # # #

import requests
import json
import ipcalc

apiurl = 'https://api.leaseweb.com/v1/bareMetals'
apikey = ''
headers = {"X-Lsw-Auth": apikey}
ips_pool = []  # Leaseweb servers IPs list
search_pool = []  # IPs to search from msg
search_pool_file_name = 'search_pool_file.txt'
results = []
debug = 0

# Get list of servers
try:
    response = requests.get(apiurl, headers=headers)
    content = response.text
    content_json = json.loads(content)
    servers_number = len(content_json["bareMetals"])

    print("Please wait for a while until we get your IPs pool from leaseweb.")
    for count in range(servers_number):
        baremetal_json = content_json["bareMetals"][count]
        baremetal_id = baremetal_json['bareMetal']["bareMetalId"]
        baremetal_name = baremetal_json['bareMetal']["serverName"]

        if debug == 1:
            print("Generating information of : " + baremetal_name)

        percentage = 100 * (int(count)/int(servers_number))
        print("Percentage : %d %%" % (int(percentage)))

        # GET IPs information for each server
        apiurl_getip = 'https://api.leaseweb.com/v1/bareMetals/' + baremetal_id + '/ips'
        if debug == 1:
            print(apiurl_getip + "\n")

        ips_request = requests.get(apiurl_getip, headers=headers)
        ips_request_text = ips_request.text
        ips_request_json = json.loads(ips_request_text)
        ip_list = ips_request_json['ips']

        # Loop onto IPs list and filter it out in a clean list
        for z in ip_list:
            ipaddr = z['ip']['ip']
            servername = z['ip']['serverName']
            ips_pool.append(ipaddr)

except any:
    pass

# Open the server pool file and add the content to the list
with open(search_pool_file_name) as f:
    content = f.readlines()
for lines in content:
    search_pool.append(lines.replace('\n', ''))

# Search the IPs found in leaseweb message
print("\n \nPlease wait for another while until we compare the pool with the input..")
print("========= Concerned IPs =========")
for ip_to_calc in search_pool:
    for x in ipcalc.Network(ip_to_calc):
        if x in ips_pool:
            print(x)
            results.append(x)

# Print message if no results
results_count = len(results)
if results_count == 0:
    print("\nNo Match Found")

print("\nFinished: SUCCESS")
