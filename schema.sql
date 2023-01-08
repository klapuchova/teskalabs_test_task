CREATE TABLE servers(id serial primary key ,
                     name text unique,
                     cpu int,
                     memory_usage int,
                     created_at timestamp with time zone,
                     status text,
                     ip_address text[]
);


SELECT to_timestamp('2020-05-19T16:23:07+02:00', 'YYYY-MM-DD"T"HH24:MI:SSTZH:TZM')::timestamptz;