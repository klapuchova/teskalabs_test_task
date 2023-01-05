import json
file = open('C:\\Users\\42073\\IdeaProjects\\Python_learning\\teskalabs_issue\\sample-data.json')
data = json.load(file)

for row in data:
    name = row["name"]

    try:
        cpu = row["state"]["cpu"]
    except TypeError:
        continue

    memory_usage = row["state"]["memory"]["usage"]
    created_at = row["created_at"]
    status = row["status"]

    addresses = row["state"]["network"]["lo"]["addresses"]
    for address in addresses:
        ip_address = address['address']
