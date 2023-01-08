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
conn = connection(postgres_login.host, postgres_login.database, postgres_login.user, postgres_login.password)


def get_ip_addresses():
    global ip_address
    network = row['state']['network']
    ip_lines = []
    all_ip_address = []
    for network_name in network:
        dict_name_paths = row['state']['network'][network_name]['addresses']

        for path in dict_name_paths:
            ip_lines.append(path['address'])
    all_ip_address.extend(ip_lines)
    ip_address = all_ip_address


def save():
    return """INSERT INTO servers (name, cpu_usage, memory_usage, created_at, status, ip_address) VALUES (%s, %s, %s, to_timestamp(%s, 'YYYY-MM-DD"T"HH24:MI:SSTZH:TZM')::timestamptz, %s, %s) ON CONFLICT (name) DO UPDATE SET cpu_usage = EXCLUDED.cpu_usage, memory_usage = EXCLUDED.memory_usage, created_at = EXCLUDED.created_at, status = EXCLUDED.status, ip_address = EXCLUDED.ip_address"""


for row in loaded_data:
    name = row['name']

    status = row['status']
    if status == 'Stopped':
        cpu_usage = 0
        memory_usage = 0
        ip_address = []
    else:
        cpu_usage = row['state']['cpu']['usage']
        memory_usage = row['state']['memory']['usage']
        created_at = row['created_at']

        get_ip_addresses()

    cur = conn.cursor()
    cur.execute(save(), (name, cpu_usage, memory_usage, created_at, status, ip_address))

    conn.commit()
    cur.close()

conn.close()