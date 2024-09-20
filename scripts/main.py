import os
import re
import pandas as pd

from parser import parse_state_region, parse_state_ownership, parse_population
from utils import create_output_folder

# Setup output folder
output_folder = './output/'
create_output_folder(output_folder)

# Parsing state regions
state_regions_folder = './input/map_data/state_regions/'
history_states_file = './input/common/history/states/00_states.txt'

# Parse and handle the states
states_data = []  # This will hold the parsed states
for filename in os.listdir(state_regions_folder):
    if filename.endswith('.txt'):
        with open(os.path.join(state_regions_folder, filename), 'r', encoding='utf-8-sig') as file:
            content = file.read()
            print(f"Content of {filename}:\n{content[:150]}")  # Print the first 100 characters
            state_blocks = re.findall(r'STATE_\w+\s*=\s*{[^}]+}', content, re.DOTALL)
            print(f"Found {len(state_blocks)} state blocks in {filename}")
            for state_block in state_blocks:
                state_info = parse_state_region(state_block)
                if state_info:
                    states_data.append(state_info)

# Parse state ownerships
with open(history_states_file, 'r', encoding='utf-8-sig') as file:
    content = file.read()
    state_blocks = re.findall(r's:STATE_\w+\s*=\s*{[^}]+}', content, re.DOTALL)
    for state_block in state_blocks:
        ownership_info = parse_state_ownership(state_block)
        if ownership_info:
            for state in states_data:
                if state['state_name'] == ownership_info['state_name']:
                    state['ownership'] = ownership_info['ownership']
                    state['homelands'] = ownership_info['homelands']

# Path to the pops folder
pops_folder = './input/common/history/pops/'

# List to hold all parsed population data
pops_data = []

# Loop over all files in the pops folder
for filename in os.listdir(pops_folder):
    if filename.endswith('.txt'):
        with open(os.path.join(pops_folder, filename), 'r', encoding='utf-8-sig') as file:
            content = file.read()
            state_blocks = re.findall(r's:STATE_\w+\s*=\s*{[^}]+}', content, re.DOTALL)

            for state_block in state_blocks:
                population_info = parse_population(state_block)
                if population_info:
                    pops_data.append(population_info)

# You can print or save this data to a CSV as needed
print(f"Parsed {len(pops_data)} states with population data")

# Output data

# Convert to pandas DataFrame
df = pd.DataFrame(states_data)

# Display first few rows to verify
print(df.head())

# Save the parsed data to a CSV file in the output folder
output_csv_path = os.path.join(output_folder, 'parsed_states.csv')
df.to_csv(output_csv_path, index=False)

print(f"Number of states parsed: {len(states_data)}")
print("Script finished running!")