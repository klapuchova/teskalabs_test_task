CREATE TABLE servers(id serial primary key ,
                     name text unique,
                     cpu int,
                     memory_usage int,
                     created_at timestamp with time zone,
                     status text,
                     ip_address text[]
);
