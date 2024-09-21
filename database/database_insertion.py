from debugging.logger import setup_logger


def insert_state_data(conn, state_data, debug=False):
    cursor = conn.cursor()
    logger = setup_logger(debug=debug)
    logger.info("Starting to insert the region states database...")

    for state in state_data:
        if debug:
            print(f"Inserting state: {state['state_name']}")  # This will show you the structure of each state

        # Convert lists to comma-separated strings for storing in the database
        provinces_str = ','.join(state.get('provinces', []))
        traits_str = ','.join(state.get('traits', []))  # Convert traits list to a comma-separated string
        arable_resources_str = ','.join(state.get('arable_resources', []))
        capped_resources_str = ','.join([f"{key}:{value}" for key, value in state.get('capped_resources', {}).items()])

        logger.info(f"Inserting state: {state['state_name']}")
        logger.info(f"{state['state_name']} Subsistence: {state.get('subsistence_building', None)}")

        # Insert the state data, including the resource block as a string
        cursor.execute('''
            INSERT INTO states (
                id, name, subsistence_building, provinces, traits, city, port, farm, mine, wood,
                arable_land, arable_resources, capped_resources, resources, naval_exit_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            state.get('id', None),
            state['state_name'],
            state.get('subsistence_building', None),
            provinces_str,
            traits_str,
            state.get('city', None),
            state.get('port', None),
            state.get('farm', None),
            state.get('mine', None),
            state.get('wood', None),
            state.get('arable_land', None),
            arable_resources_str,
            capped_resources_str,
            state.get('resources', None),  # Store the full resource block as a string
            state.get('naval_exit_id', None)
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