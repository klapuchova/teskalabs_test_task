CREATE TABLE servers
(
  id serial PRIMARY KEY,
  name text UNIQUE NOT NULL,
  cpu int NOT NULL,
  memory_usage int NOT NULL,
  created_at timestamp with time zone NOT NULL,
  status text NOT NULL,
  ip_address text[] NOT NULL
);
