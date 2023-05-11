import json

def split_ip(ip):
    ipsplit = ip.split(".")
    subnet = ipsplit[3].split("/")
    ipsplit.pop(3)
    ipsplit.append(subnet[0])
    ipsplit.append(subnet[1])
    return ipsplit

with open('routes.json', 'r') as f:
    data = json.load(f)

dst_ip = input("Enter Destination IP: ")
dst_ip_split = split_ip(dst_ip)

route_list = []
hop_list = []
type_list = []
for route in data["Routes"]:
    split_route = split_ip(route[0])
    route_list.append(split_route)
    hop_list.append(route[1])
    type_list.append(route[2])

for route in route_list:
    for i in range(4):
        route[i] = int(route[i])
        route[i] = "{:08b}".format(route[i])

for i in range(4):
    dst_ip_split[i] = int(dst_ip_split[i])
    dst_ip_split[i] = "{:08b}".format(dst_ip_split[i])

print(dst_ip_split)
print(route_list[1])

dst_ip_split_joined = dst_ip_split[0]+dst_ip_split[1]+dst_ip_split[2]+dst_ip_split[3]

match_list = []
for route in route_list:
    subnet = route[4]
    route = route[0]+route[1]+route[2]+route[3]
    split_route = route[0:int(subnet)]
    dst_ip_split_subnet = dst_ip_split_joined[0:int(subnet)]

    if dst_ip_split_subnet == split_route:
        match_list.append(True)
    else:
        match_list.append(False)
    
print(match_list)

