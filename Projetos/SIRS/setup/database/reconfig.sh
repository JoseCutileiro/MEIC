#!/bin/sh

# Define the path to the pg_hba.conf file
pg_hba_conf="/etc/postgresql/16/main/pg_hba.conf"

# Define the parameters for the new entry
database="sirs"
user="musicstore"
address="192.168.1.1/24"
method="md5"

# Define the path to the PostgreSQL configuration file
config_file="/etc/postgresql/16/main/postgresql.conf"

# Define the new values for port and listen_addresses
new_port="5432"
new_listen_addresses="*"

# Check if the configuration file exists
if [ -e "$config_file" ]; then
    # Use sed to replace the existing values with the new ones
    sed -i "s/^port = .*/port = $new_port/" "$config_file"
    sed -i "s/^#listen_addresses = .*/listen_addresses = '$new_listen_addresses'/" "$config_file"

    echo "Configuration updated successfully."
else
    echo "Error: PostgreSQL configuration file not found."
fi

# Check if the pg_hba.conf file exists
if [ -e "$pg_hba_conf" ]; then
    # Replace the commented line with the new entry
    sudo sed -i "/^# host[[:space:]]*DATABASE[[:space:]]*USER[[:space:]]*ADDRESS[[:space:]]*METHOD[[:space:]]*\[OPTIONS\]$/c\host          $database  $user  $address  $method" "$pg_hba_conf"

    echo "Entry replaced in pg_hba.conf:"
    echo "host          $database  $user  $address  $method"
else
    echo "Error: pg_hba.conf file not found."
fi

