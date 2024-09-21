import sqlite3

def connect_db(db_name='vic3_database.db'):
    """Connects to the SQLite database or creates it if it doesn't exist."""
    conn = sqlite3.connect(db_name)
    return conn

def create_tables(conn):
    """Creates the necessary tables for states, countries, pops, and resources."""
    cursor = conn.cursor()

    # Create States table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS states (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            region TEXT,
            arable_land INTEGER
        )
    ''')

    # Create Pops table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pops (
            id INTEGER PRIMARY KEY,
            state_name TEXT,
            region_state TEXT,
            culture TEXT,
            religion TEXT,
            size INTEGER
        )
    ''')

    # Create Arable Resources table (boolean-like)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS states_arable_resources (
            id INTEGER PRIMARY KEY,
            state_id INTEGER,
            resource_type TEXT,
            is_enabled BOOLEAN,
            FOREIGN KEY (state_id) REFERENCES states(id)
        )
    ''')

    # Create Capped Resources table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS states_capped_resources (
            id INTEGER PRIMARY KEY,
            state_id INTEGER,
            resource_type TEXT,
            cap INTEGER,
            FOREIGN KEY (state_id) REFERENCES states(id)
        )
    ''')

    conn.commit()