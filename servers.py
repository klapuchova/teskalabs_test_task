import json
import psycopg2
import os
from typing import Any

class Servers:
    def __init__(self, host: str, database: str, user: str, password: str):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def __connection(self) -> Any:
        conn = psycopg2.connect(host = self.host, database = self.database, user = self.user, password = self.password)
        return conn

    def __load_source_data(self) -> dict[str, Any]:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'sample-data.json')

        f = open(filename)
        load = json.load(f)
        f.close()
        return load

    def __get_ip_addresses(self, row) -> list[str]:
        network = row['state']['network']
        ip_lines = []
        all_ip_address = []
        for network_name in network:
            dict_name_paths = row['state']['network'][network_name]['addresses']

            for path in dict_name_paths:
                ip_lines.append(path['address'])
        all_ip_address.extend(ip_lines)

        return all_ip_address

    def save(self) -> None:
        conn = self.__connection()
        loaded_data = self.__load_source_data()
        for row in loaded_data:
            name = row['name']
            created_at = row['created_at']
            status = row['status']

            if status == 'Stopped':
                cpu_usage = 0
                memory_usage = 0
                ip_address = []
            else:
                cpu_usage = row['state']['cpu']['usage']
                memory_usage = row['state']['memory']['usage']
                ip_address = self.__get_ip_addresses(row)

            cur = conn.cursor()
            query = """
            INSERT INTO servers (name, cpu_usage, memory_usage, created_at, status, ip_address)
            VALUES (%s, %s, %s, to_timestamp(%s, 'YYYY-MM-DD"T"HH24:MI:SSTZH:TZM')::timestamptz, %s, %s)
            ON CONFLICT (name) 
            DO UPDATE SET cpu_usage = EXCLUDED.cpu_usage,
                          memory_usage = EXCLUDED.memory_usage,
                          created_at = EXCLUDED.created_at,
                          status = EXCLUDED.status,
                          ip_address = EXCLUDED.ip_address
            """
            cur.execute(query, (name, cpu_usage, memory_usage, created_at, status, ip_address))
            conn.commit()
            cur.close()

        conn.close()