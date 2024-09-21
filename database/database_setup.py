import sqlite3

def connect_db(db_name='vic3_database.db'):
    """Connects to the SQLite database or creates it if it doesn't exist."""
    conn = sqlite3.connect(db_name)
    return conn

def create_tables(conn):
    """Creates the necessary tables for states, countries, pops, and resources."""
    cursor = conn.cursor()

    # Drop the table if it exists
    cursor.execute('DROP TABLE IF EXISTS states')

    # Create States table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS states (
            id INTEGER PRIMARY KEY,           -- The state id
            name TEXT NOT NULL,               -- The state name
            subsistence_building TEXT,         -- The subsistence building in the state
            provinces TEXT,                    -- Provinces as a comma-separated string
            traits TEXT,                       -- Capped resources as a comma-separated string
            city TEXT,                         -- City in the state
            port TEXT,                         -- Port in the state
            farm TEXT,                         -- Farm in the state
            mine TEXT,                         -- Mine in the state
            wood TEXT,                         -- Wood in the state
            arable_land INTEGER,               -- Arable land amount
            arable_resources TEXT,             -- Arable resources as a comma-separated string
            capped_resources TEXT,             -- Capped resources as a comma-separated string
            resources TEXT,                    -- Type of undiscovered resource (if present)
            naval_exit_id INTEGER              -- Naval exit id (if present)
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