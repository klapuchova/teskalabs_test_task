import json
from datetime import datetime

file = open('C:\\Users\\42073\\IdeaProjects\\Python_learning\\teskalabs_issue\\sample-data.json')
data = json.load(file)

for row in data:
    name = row["name"]

    try:
        cpu = row["state"]["cpu"]["usage"]
    except TypeError:
        continue

    memory_usage = row["state"]["memory"]["usage"]
    created_at = row["created_at"]
    status = row["status"]
    print(status)

    addresses = row["state"]["network"]
    api_lines = []
    all_api_address = []
    for i in addresses:
        dict_name_paths = row["state"]["network"][i]["addresses"]

        for path in dict_name_paths:
            api_lines.append(path["address"])
    all_api_address.extend(api_lines)

    api_address = all_api_address





