import json
import tkinter as tk
from tkinter import filedialog
import ipaddress


def split_ip(ip):
    ipsplit = ip.split(".")
    subnet = ipsplit[3].split("/")
    ipsplit.pop(3)
    ipsplit.append(subnet[0])
    ipsplit.append(subnet[1])
    return ipsplit

def find_matching_ip():
    file_path = file_label.cget("text")
    with open(file_path, 'r') as f:
        data = json.load(f)

    dst_ip = dst_ip_entry.get()
    dst_ip_split = split_ip(dst_ip)

    route_list = []
    for route in data["RouteList"]:
        split_route = split_ip(route["route"])
        route_list.append(split_route)

    for route in route_list:
        for i in range(4):
            route[i] = int(route[i])
            route[i] = "{:08b}".format(route[i])

    for i in range(4):
        dst_ip_split[i] = int(dst_ip_split[i])
        dst_ip_split[i] = "{:08b}".format(dst_ip_split[i])

    dst_ip_split_joined = dst_ip_split[0] + dst_ip_split[1] + dst_ip_split[2] + dst_ip_split[3]


    match_list = []
    for route in route_list:
        route_joined = route[0] + route[1] + route[2] + route[3]
        subnet = route[4]
        route_match = route_joined[0 : int(subnet)]
        dst_ip_split_joined_spliced = dst_ip_split_joined[0 : int(subnet)]
        if route_match == dst_ip_split_joined_spliced:
            match_list.append(route_joined + "/" + subnet)
    if len(match_list) == 0:
        match_list.append("0000000000000000000000000000000/0")
    

    #TODO sort by type if subnets are equal Default 
    #Use lowest value and look at Liams PNG to determine
    max_subnet = -1
    nextpath = ""
    for match in match_list:
        subnet = match.split("/")[1]
        if (int(subnet) > max_subnet):
            nextpath = match
            max_subnet = int(subnet)
    
    binaryToDecimal = lambda binary_ip: str(ipaddress.IPv4Address(int(binary_ip.split('/')[0], 2))) + '/' + binary_ip.split('/')[1]
    nextpath = binaryToDecimal(nextpath)

    for route in data["RouteList"]:
        if nextpath == route["route"]:
            next_hop = route["next_hop"]
            route_type = route["type"]
            break

    output_label_route.config(text="The Route that matches most is..." + nextpath)
    output_label_next_hop.config(text = "The Next Hop is..." + next_hop)
    output_label_type.config(text = "The type of route is..." + route_type)

def browse_file():
    file_path = filedialog.askopenfilename()
    file_label.config(text=file_path)


root = tk.Tk()
root.geometry("400x200")

file_frame = tk.Frame(root)
file_label = tk.Label(file_frame, text="Enter file name or select file:")
file_entry = tk.Entry(file_frame)
file_button = tk.Button(file_frame, text="Select File", command=browse_file)

file_label.pack(side=tk.TOP)
file_entry.pack(side=tk.TOP)
file_button.pack(side=tk.TOP)

dst_ip_frame = tk.Frame(root)
dst_ip_label = tk.Label(dst_ip_frame, text="Enter Destination IP:")
dst_ip_entry = tk.Entry(dst_ip_frame)

dst_ip_label.pack(side=tk.TOP)
dst_ip_entry.pack(side=tk.TOP)

button_frame = tk.Frame(root)
search_button = tk.Button(button_frame, text="Search", command=find_matching_ip)

search_button.pack(side=tk.TOP)

output_frame = tk.Frame(root)
output_label_route = tk.Label(output_frame, text = "The Route that matches most is...")
output_label_next_hop = tk.Label(output_frame, text = "The Next Hop is...")
output_label_type = tk.Label(output_frame, text = "The type of route is...")

output_label_route.pack(side=tk.TOP)
output_label_next_hop.pack(side=tk.TOP)
output_label_type.pack(side=tk.TOP)

file_frame.pack(side=tk.TOP)
dst_ip_frame.pack(side=tk.TOP)
button_frame.pack(side=tk.TOP)
output_frame.pack(side=tk.TOP)


root.mainloop()