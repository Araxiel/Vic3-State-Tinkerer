from database.database_setup import connect_db, create_tables
from database.database_insertion import insert_pop_data, insert_state_data
from debugging.logger import setup_logger, save_debug_json
from parsing.parsing_states import parse_state_regions
from parsing.parsing_pops import parse_pops

def build_database(debug=False):
    logger = setup_logger(debug=debug)
    logger.info("Starting to build the database...")

    try:
        # Connect to the database
        conn = connect_db()

        # Create the necessary tables
        logger.info("Creating tables...")
        create_tables(conn)

        # Parse state regions
        logger.info("Parsing state regions...")
        state_data = parse_state_regions('./_input/map_data/state_regions/', debug=debug)
        logger.info(f'Successfully parsed {len(state_data)} states')
        save_debug_json(state_data, 'state_data')

        # Insert state data into the database
        logger.info("Inserting state data into database...")
        insert_state_data(conn, state_data, debug)

        # Parse population data
        logger.info("Parsing population data...")
        pop_data = parse_pops('./_input/common/history/pops/', debug=debug)
        logger.info(f'Successfully parsed {len(pop_data)} pops')
        save_debug_json(pop_data, 'pop_data')

        # Insert population data into the database
        logger.info("Inserting population data into database...")
        insert_pop_data(conn, pop_data)

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        logger.info("Database built successfully.")
    except Exception as e:
        logger.error(f"Error building the database: {e}", exc_info=True)
