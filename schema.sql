CREATE TABLE servers
(
  id serial PRIMARY KEY,
  name text UNIQUE,
  cpu int,
  memory_usage int,
  created_at timestamp with time zone,
  status text,
  ip_address text[]
);
