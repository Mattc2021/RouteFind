import json

file_paths = ['Router0.txt', 'Router1.txt', 'Router2.txt', 'Router3.txt', 'Router4.txt']
#Pulls interface and protocol data. Does not look for VPN
for file_path in file_paths:
    with open(file_path) as f:
        lines = []
        keep = False
        for line in f:
            if line.startswith('interface') or line.startswith('router'):
                keep = True
            elif line.startswith('!'):
                keep = False
            if keep:
                lines.append(line.strip())
#Stores sorted data
    data = {}
    current_key = None
    for line in lines:
        if line.startswith('interface') or line.startswith('router'):
            current_key = line
            data[current_key] = []
        else:
            data[current_key].append(line)

    json_data = json.dumps(data, indent=4)
    print(json_data) #this prints all relevant data
    with open('configs.json', 'w') as f: 
        f.write(json_data) #only writes data from router0



 
