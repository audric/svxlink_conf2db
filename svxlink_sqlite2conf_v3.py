#!/usr/bin/env python3

import sqlite3

db_path = 'svxlink_conf_v3.db'  # Path to your SQLite database
config_file_path = 'svxlink_conf_v3.txt'  # Output configuration file

def write_config_from_db_ordered(db_path, file_path):
    """
    Write a configuration file from an SQLite database, ordering sections by svxlink_conf_sections table.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Retrieve the list of sections from svxlink_conf_sections in order
    cursor.execute("SELECT section_name FROM svxlink_conf_sections ORDER BY id")
    sections = cursor.fetchall()

    with open(file_path, 'w') as file:
        for section_name, in sections:
            # Write the section header
            file.write(f'[{section_name}]\n')
            print(f"Writing section: [{section_name}]")

            # Query key-value pairs for the current section
            cursor.execute(f'SELECT key, value FROM "{section_name}"')
            key_values = cursor.fetchall()

            # Write the key-value pairs
            for key, value in key_values:
                file.write(f'{key}={value}\n')

            # Add a newline for readability between sections
            file.write('\n')

    conn.close()
    print("Configuration file has been created from the SQLite database in ordered manner.")

# Generate the ordered configuration file from the database
write_config_from_db_ordered(db_path, config_file_path)
