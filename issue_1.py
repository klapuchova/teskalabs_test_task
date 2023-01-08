import json
import psycopg2
import postgres_login
import os
from typing import Any


def connection(host: str, database: str, user: str, password: str):
    conn = psycopg2.connect(
    host = host,
    database = database,
    user = user,
    password = password
    )
    return conn


def load_source_data() -> dict[str, Any]:
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'sample-data.json')

    f = open(filename)
    load = json.load(f)
    f.close()
    return load


loaded_data = load_source_data()


for row in loaded_data:
    name = row["name"]

    try:
        cpu_usage = row["state"]["cpu"]["usage"]
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
        cur.execute("""INSERT INTO servers (name, cpu_usage, memory_usage, created_at, status, ip_address) VALUES (%s, %s, %s, to_timestamp(%s, 'YYYY-MM-DD"T"HH24:MI:SSTZH:TZM')::timestamptz, %s, %s)""",
                    (name, cpu_usage, memory_usage, created_at, status, api_address))

    conn.commit()
    cur.close()
    conn.close()