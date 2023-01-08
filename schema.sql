CREATE TABLE servers
(
  id serial PRIMARY KEY,
  name text UNIQUE NOT NULL CHECK (trim(name) != ''),
  cpu int NOT NULL CHECK (cpu >= 0),
  memory_usage int NOT NULL CHECK (cpu >= 0),
  created_at timestamp with time zone NOT NULL,
  status text NOT NULL CHECK (status IN ('Running', 'Stopped')),
  ip_address text[] NOT NULL
);
