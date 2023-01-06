CREATE TABLE servers(id serial PRIMARY KEY,
                     name TEXT unique,
                     cpu INT,
                     memory_usage INT,
                     created_at TIMESTAMP WITHOUT TIME ZONE,
                     status TEXT,
                     ip_address text[]
);