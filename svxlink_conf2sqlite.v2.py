#!/usr/bin/env python3

import sqlite3
import re

config_file_path = 'svxlink.conf.in'  # The path to the configuration file
db_path = 'svxlink_conf_v2.db'  # The path to the SQLite database

# Regular expressions for parsing
section_regex = re.compile(r'^\[(.+)\]$')
key_value_regex = re.compile(r'^([^#=]+)=(.*)$')

def parse_config(file_path):
    """
    Parse the configuration file into a dictionary of sections with their key-value pairs.
    """
    config = {}
    current_section = None

    print("Starting to parse the configuration file...")
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Skip empty lines and comments
            
            section_match = section_regex.match(line)
            if section_match:
                current_section = section_match.group(1)
                if current_section not in config:
                    config[current_section] = []
                print(f"Found section: {current_section}")
            else:
                key_value_match = key_value_regex.match(line)
                if key_value_match and current_section is not None:
                    key, value = key_value_match.groups()
                    config[current_section].append((key.strip(), value.strip()))
                    print(f"Added key-value pair: {key.strip()} = {value.strip()}")

    print("Finished parsing the configuration file.")
    return config

def create_db_from_config(config, db_path):
    """
    Create an SQLite database from the parsed configuration dictionary.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create a table for storing sections
    cursor.execute('CREATE TABLE IF NOT EXISTS svxlink_conf_sections (id INTEGER PRIMARY KEY AUTOINCREMENT, section_name TEXT UNIQUE)')

    print("Creating SQLite database from configuration data...")
    for section, key_values in config.items():
        # Insert the section into svxlink_conf_sections
        cursor.execute('INSERT OR IGNORE INTO svxlink_conf_sections (section_name) VALUES (?)', (section,))

        # Adjust table schema to include an auto-increment ID, creation, and update timestamps
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{section}" (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           key TEXT,
                           value TEXT,
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           )''')
        
        # Insert key-value pairs into the table, adjusting for the new schema
        print(f"Inserting key-value pairs into table: {section}")
        cursor.executemany(f'''INSERT INTO "{section}" (key, value) 
                               VALUES (?, ?)''', key_values)

    conn.commit()
    conn.close()
    print("SQLite database creation completed.")

# Parse the configuration file
config = parse_config(config_file_path)

# Create the SQLite database from the parsed configuration
create_db_from_config(config, db_path)

print("SQLite database has been created with the configuration data.")
