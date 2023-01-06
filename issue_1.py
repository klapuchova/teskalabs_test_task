import json
import psycopg2
import postgres_login


def connection(host, database, user, password):
    conn = psycopg2.connect(
    host = host,
    database = database,
    user = user,
    password = password
    )
    return conn


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


    addresses = row["state"]["network"]
    api_lines = []
    all_api_address = []
    for i in addresses:
        dict_name_paths = row["state"]["network"][i]["addresses"]

        for path in dict_name_paths:
            api_lines.append(path["address"])
    all_api_address.extend(api_lines)

    api_address = all_api_address


    # print(name)
    # print(cpu)
    # print(memory_usage)
    # print(created_at)
    # print(status)
    # print(api_address)
    # print('\n')


    conn = connection(postgres_login.host, postgres_login.database, postgres_login.user, postgres_login.password)
    cur = conn.cursor()
    cur.execute("SELECT * FROM servers WHERE name=%s AND memory_usage=%s", (name, memory_usage))
    if cur.rowcount == 0:
        cur.execute("INSERT INTO servers (name, cpu, memory_usage, created_at, status, ip_address) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, cpu, memory_usage, created_at, status, api_address))

    conn.commit()
    cur.close()
    conn.close()