#!/bin/sh

# Fixed values for PostgreSQL user and database
pg_user="musicstore"
pg_password="m3S8iBg@"
pg_db="sirs"
schema_file="scheme.sql"

# Install PostgreSQL
sudo apt-get install -y postgresql postgresql-contrib

# Start and enable PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create a PostgreSQL database
sudo -u postgres psql -c "CREATE DATABASE $pg_db;"

# Create a PostgreSQL user
sudo -u postgres psql -c "CREATE USER $pg_user WITH PASSWORD '$pg_password';"

# Grant necessary privileges
sudo -u postgres psql -c "ALTER DATABASE $pg_db OWNER TO $pg_user;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $pg_db TO $pg_user;"

echo "PostgreSQL setup completed. Database: $pg_db"
