import os
import re

def parse_state_regions(folder, debug=False):
    states_data = []
    if debug:
        print(f"Starting to parse state regions from {folder}")

    # Parse logic here
    for filename in os.listdir(folder):
        if filename.endswith('.txt'):
            with open(os.path.join(folder, filename), 'r', encoding='utf-8-sig') as file:
                content = file.read()
                if debug:
                    print(f"Parsing file: {filename}")
                
                # Find all state blocks using regex
                state_blocks = re.findall(r'STATE_\w+\s*=\s*{[^}]+}', content, re.DOTALL)
                if debug:
                    print(f"Found {len(state_blocks)} state blocks in {filename}")

                # Parse each state block
                for state_block in state_blocks:
                    state_info = parse_state_region(state_block)  # Fix here
                    if state_info:
                        states_data.append(state_info)

    if debug:
        print(f"Finished parsing. Total states parsed: {len(states_data)}")

    return states_data

# This function is responsible for parsing the contents of each state block
def parse_state_region(state_block):
    state_data = {}
    
    # Extract state name, id, etc.
    state_name_match = re.search(r'STATE_(\w+)', state_block)
    state_id_match = re.search(r'id\s*=\s*(\d+)', state_block)
    arable_land_match = re.search(r'arable_land\s*=\s*(\d+)', state_block)
    
    if state_name_match:
        state_data['state_name'] = state_name_match.group(1)
    if state_id_match:
        state_data['id'] = int(state_id_match.group(1))
    if arable_land_match:
        state_data['arable_land'] = int(arable_land_match.group(1))
    
    # Continue extracting other relevant data...
    
    return state_data
