#!/usr/bin/env python3

import sqlite3

db_path = 'svxlink_conf_v1.db'  # Path to your SQLite database
config_file_path = 'svxlink_conf_v1.txt'  # Output configuration file

def write_config_from_db(db_path, file_path):
    """
    Write a configuration file from an SQLite database, excluding system tables.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Retrieve the list of tables (sections), excluding system tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = cursor.fetchall()

    with open(file_path, 'w') as file:
        for table_name in tables:
            # Write the section header
            section = table_name[0]
            file.write(f'[{section}]\n')
            print(f"Writing section: [{section}]")

            # Query key-value pairs for the current table
            cursor.execute(f'SELECT key, value FROM "{section}"')
            key_values = cursor.fetchall()

            # Write the key-value pairs
            for key, value in key_values:
                file.write(f'{key}={value}\n')

            # Add a newline for readability between sections
            file.write('\n')

    conn.close()
    print("Configuration file has been created from the SQLite database.")

# Generate the configuration file from the database
write_config_from_db(db_path, config_file_path)
