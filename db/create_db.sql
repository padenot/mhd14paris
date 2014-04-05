\set ON_ERROR_STOP 1

-- Create the user and the database. Must run as user postgres.

--CREATE USER mcoverart PASSWORD 'mcoverartrox' NOCREATEDB NOCREATEUSER;
CREATE USER mcoverart NOCREATEDB NOCREATEUSER;
CREATE DATABASE mcoverart WITH OWNER = mcoverart TEMPLATE template0 ENCODING = 'UNICODE';
