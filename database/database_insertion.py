def insert_state_data(conn, state_data):
    cursor = conn.cursor()

    # DEBUG: Log or print the state_data to check its structure
    for state in state_data:
        print(f"Inserting state: {state}")  # This will show you the structure of each state
    
        cursor.execute('''
            INSERT INTO states (name, region, arable_land, arable_resources, capped_resources)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            state['state_name'],  # Ensure 'state_name' exists in state_data
            state.get('region', None),  # If 'region' is not found, default to None
            state.get('arable_land', None),
            ','.join(state.get('arable_resources', [])),  # If 'arable_resources' is missing, use an empty list
            ','.join(state.get('capped_resources', []))
        ))

    conn.commit()

def insert_pop_data(conn, pop_data):
    """Insert parsed population data into the SQLite database."""
    cursor = conn.cursor()

    for region in pop_data['regions']:
        for pop in region['pops']:
            cursor.execute('''
                INSERT INTO pops (state_name, region_state, culture, religion, size)
                VALUES (?, ?, ?, ?, ?)
            ''', (pop_data['state_name'], region['region_state'], pop['culture'], pop.get('religion', None), pop['size']))

    conn.commit()

def insert_arable_resources(conn, state_id, arable_resources):
    """Insert arable resources for a state."""
    cursor = conn.cursor()

    for resource in arable_resources:
        cursor.execute('''
            INSERT INTO states_arable_resources (state_id, resource_type, is_enabled)
            VALUES (?, ?, ?)
        ''', (state_id, resource, True))

    conn.commit()

def insert_capped_resources(conn, state_id, capped_resources):
    """Insert capped resources for a state."""
    cursor = conn.cursor()

    for resource, cap in capped_resources.items():
        cursor.execute('''
            INSERT INTO states_capped_resources (state_id, resource_type, cap)
            VALUES (?, ?, ?)
        ''', (state_id, resource, cap))

    conn.commit()