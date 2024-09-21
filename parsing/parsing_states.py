import os
import re
from debugging.logger import log_variable_to_file, setup_logger

def parse_state_regions(folder, debug=False):
    states_data = []
    if debug:
        print(f"Starting to parse state regions from {folder}")

    # Regex pattern to match everything between two STATE_ occurrences
    state_pattern = re.compile(r'(STATE_\w+\s*=\s*{.*?)(?=STATE_\w+\s*=|$)', re.DOTALL)

    # Parse logic here
    for filename in os.listdir(folder):
        if filename.endswith('.txt'):
            with open(os.path.join(folder, filename), 'r', encoding='utf-8-sig') as file:
                content = file.read()
                if debug:
                    print(f"Parsing file: {filename}")
                
                # Find all state blocks using the updated regex
                state_blocks = state_pattern.findall(content)
                if debug:
                    print(f"Found {len(state_blocks)} state blocks in {filename}")
                    # log_variable_to_file(state_blocks, "state_blocks.txt")

                # Parse each state block
                for state_block in state_blocks:
                    state_info = parse_state_region(state_block, debug)  # Parsing each state block
                    if state_info:
                        states_data.append(state_info)

    if debug:
        print(f"Finished parsing. Total states parsed: {len(states_data)}")

    return states_data

# This function is responsible for parsing the contents of each state block
def parse_state_region(state_block, debug=False):
    logger = setup_logger(debug=debug)
    
    """Parses a state block to extract relevant information."""
    
    state_info = {}

    # Parse the state name (e.g., STATE_HANNOVER)
    state_name_match = re.search(r'STATE_(\w+)', state_block)
    if state_name_match:
        state_info['state_name'] = state_name_match.group(1)

    # Parse 'id'
    id_match = re.search(r'id\s*=\s*(\d+)', state_block)
    if id_match:
        state_info['id'] = int(id_match.group(1))

    state_id = id_match.group(1)
    state_name = state_name_match.group(1)
    if debug:
        logger.info(f"Parsing: {state_id} - {state_name}")
        log_variable_to_file(state_block, f"states/{state_id} - {state_name}.txt")

    traits_match = re.search(r'traits\s*=\s*{([^}]+)}', state_block)
    if traits_match:
        state_info['traits'] = traits_match.group(1)

    # Parse 'subsistence_building'
    subsistence_building_match = re.search(r'subsistence_building\s*=\s*"([^"]+)"', state_block)
    if subsistence_building_match:
        state_info['subsistence_building'] = subsistence_building_match.group(1)

    # Parse 'provinces'
    provinces_match = re.search(r'provinces\s*=\s*{([^}]+)}', state_block)
    if provinces_match:
        state_info['provinces'] = re.findall(r'"([^"]+)"', provinces_match.group(1))

    # Parse city, port, farm, mine, wood
    state_info['city'] = re.search(r'city\s*=\s*"([^"]+)"', state_block).group(1) if re.search(r'city\s*=\s*"([^"]+)"', state_block) else None
    state_info['port'] = re.search(r'port\s*=\s*"([^"]+)"', state_block).group(1) if re.search(r'port\s*=\s*"([^"]+)"', state_block) else None
    state_info['farm'] = re.search(r'farm\s*=\s*"([^"]+)"', state_block).group(1) if re.search(r'farm\s*=\s*"([^"]+)"', state_block) else None
    state_info['mine'] = re.search(r'mine\s*=\s*"([^"]+)"', state_block).group(1) if re.search(r'mine\s*=\s*"([^"]+)"', state_block) else None
    state_info['wood'] = re.search(r'wood\s*=\s*"([^"]+)"', state_block).group(1) if re.search(r'wood\s*=\s*"([^"]+)"', state_block) else None

    # Parse 'arable_land'
    arable_land_match = re.search(r'arable_land\s*=\s*(\d+)', state_block)
    if arable_land_match:
        state_info['arable_land'] = int(arable_land_match.group(1))

    # Parse 'arable_resources'
    arable_resources_match = re.search(r'arable_resources\s*=\s*{([^}]+)}', state_block)
    if arable_resources_match:
        state_info['arable_resources'] = re.findall(r'"([^"]+)"', arable_resources_match.group(1))

    # Parse 'capped_resources'
    capped_resources_match = re.findall(r'(\w+)\s*=\s*(\d+)', re.search(r'capped_resources\s*=\s*{([^}]+)}', state_block).group(1) if re.search(r'capped_resources\s*=\s*{([^}]+)}', state_block) else "")
    if capped_resources_match:
        state_info['capped_resources'] = {match[0]: int(match[1]) for match in capped_resources_match}

    # Parse 'resources' (optional)
    resources_match = re.search(r'resource\s*=\s*{[^}]+}', state_block, re.DOTALL)
    if resources_match:
        state_info['resources'] = resources_match.group(0)  # Store the entire resource block as a string

    # Parse 'naval_exit_id' (optional)
    naval_exit_id_match = re.search(r'naval_exit_id\s*=\s*(\d+)', state_block)
    if naval_exit_id_match:
        state_info['naval_exit_id'] = int(naval_exit_id_match.group(1))

    return state_info