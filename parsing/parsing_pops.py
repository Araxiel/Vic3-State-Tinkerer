import re

def parse_pops(filename, debug=False):
    """Parses population data from the given file."""
    population_data = {}

    state_name_match = re.search(r's:STATE_(\w+)', state_block)
    if state_name_match:
        population_data['state_name'] = state_name_match.group(1)

    # Find all region states in the block
    region_blocks = re.findall(r'region_state:(\w+)\s*=\s*{([^}]+)}', state_block, re.DOTALL)

    regions = []
    for region_name, region_content in region_blocks:
        region = {'region_state': region_name}

        # Find all create_pop blocks in the region content
        create_pop_blocks = re.findall(r'create_pop\s*=\s*{([^}]+)}', region_content, re.DOTALL)

        pops = []
        for pop_block in create_pop_blocks:
            pop_data = {}
            culture_match = re.search(r'culture\s*=\s*(\w+)', pop_block)
            religion_match = re.search(r'religion\s*=\s*(\w+)', pop_block)
            size_match = re.search(r'size\s*=\s*(\d+)', pop_block)

            if culture_match:
                pop_data['culture'] = culture_match.group(1)
            if religion_match:
                pop_data['religion'] = religion_match.group(1)
            if size_match:
                pop_data['size'] = int(size_match.group(1))

            pops.append(pop_data)

        region['pops'] = pops
        regions.append(region)

    population_data['regions'] = regions
    return population_data