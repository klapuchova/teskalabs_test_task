CREATE TABLE servers
(
  id serial PRIMARY KEY,
  name text UNIQUE NOT NULL CHECK (trim(name) != ''),
  cpu_usage int NOT NULL CHECK (cpu_usage >= 0),
  memory_usage int NOT NULL CHECK (cpu_usage >= 0),
  created_at timestamp with time zone NOT NULL,
  status text NOT NULL CHECK (status IN ('Running', 'Stopped')),
  ip_address text[] NOT NULL
);
