#!/bin/sh

# Create the database
psql -U postgres < create_db.sql

# install 
psql -U postgres mcoverart < `pg_config --sharedir`/contrib/cube.sql

# Create the tables
psql -U mcoverart mcoverart < create_tables.sql
