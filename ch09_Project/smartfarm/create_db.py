# file: create_db.py
# This script creates a SQLite database for the smart farm project.

import sqlite3
import os

from config import DB_PATH

DB_DIR = os.path.dirname(DB_PATH)

def create_database():
    try:
        # 1. Check and create DB folder path
        os.makedirs(DB_DIR, exist_ok=True)

        # 2. Connect to DB
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 3. Create table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL,
            humidity REAL,
            moisture REAL,
            water_level REAL,
            growth_level INTEGER,
            confidence REAL
        )
        ''')

        # 4. Commit and close
        conn.commit()
        conn.close()
        print(f'Database created successfully at {DB_PATH}')

    except sqlite3.Error as err:
        print(f'SQLite error: {err}')
    except Exception as err:
        print(f'Unexpected error: {err}')

if __name__ == "__main__":
    create_database()