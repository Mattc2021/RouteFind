import json
#Pulls router configs
file_paths = ['Router0.txt', 'Router1.txt', 'Router2.txt', 'Router3.txt', 'Router4.txt']
#Filters out more useless information
ignore_strings = ["no ip address", "duplex auto", "speed auto","shutdown", "log-adjacency-changes"]
#Array to hold data for JSON outside the for loop
all_data = []

for file_path in file_paths:
    with open(file_path) as f:
        lines = []
        keep = False
        for line in f:
            if any(ignore_string in line for ignore_string in ignore_strings):     #filters out strings
                continue
            if line.startswith('interface') or line.startswith('router'):
                keep = True
            elif line.startswith('!'):
                keep = False
            if keep:
                lines.append(line.strip())
                
    data = {}
    current_key = None
    for line in lines:
        if line.startswith('interface') or line.startswith('router'):
            current_key = line
            data[current_key] = []
        else:
            data[current_key].append(line)

    all_data.append(data)

json_data = json.dumps(all_data, indent=4)     #fixed previous issue with data being overwritten each itteration of the for loop
#print(json_data)
   
with open('configs.json', 'w') as f:
   f.write(json_data)


 
