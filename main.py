import argparse
import re
import sys
import os
import json

# Add the scripts folder to Python’s path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

# Now import from the scripts folder (without the `.py` extension)
from parser import parse_state_region, parse_population, parse_state_ownership
from utils import create_output_folder

# Define the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Use os.path.join to form the paths dynamically
state_regions_folder = os.path.join(project_root, 'input', 'map_data', 'state_regions')
pops_folder = os.path.join(project_root, 'input', 'common', 'history', 'pops')
history_states_folder = os.path.join(project_root, 'input', 'common', 'history', 'states')

# Create a function to handle the argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description="Vic3 State Tinkerer Tool")

    # Add command-line options
    parser.add_argument('--edit-pop-size', action='store_true', help='Edit population sizes')
    parser.add_argument('--factor', type=float, default=1, help='Factor by which to adjust populations')

    args = parser.parse_args()
    return args

# Main logic of the tool
def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Parse the state and population data
    state_regions_folder = './input/map_data/state_regions/'
    pops_folder = os.path.join(project_root, 'input', 'common', 'history', 'pops')
    history_states_file = './input/common/history/states/00_states.txt'

    # Load state regions data (existing logic)
    states_data = []  # This list will hold parsed state data
    for filename in os.listdir(state_regions_folder):
        if filename.endswith('.txt'):
            with open(os.path.join(state_regions_folder, filename), 'r', encoding='utf-8-sig') as file:
                content = file.read()
                state_blocks = re.findall(r'STATE_\w+\s*=\s*{[^}]+}', content, re.DOTALL)
                for state_block in state_blocks:
                    state_info = parse_state_region(state_block)
                    if state_info:
                        states_data.append(state_info)

    # Load population data
    pops_data = []  # This list will hold parsed population data
    for filename in os.listdir(pops_folder):
        if filename.endswith('.txt'):
            with open(os.path.join(pops_folder, filename), 'r', encoding='utf-8-sig') as file:
                content = file.read()
                state_blocks = re.findall(r's:STATE_\w+\s*=\s*{[^}]+}', content, re.DOTALL)
                for state_block in state_blocks:
                    population_info = parse_population(state_block)
                    if population_info:
                        pops_data.append(population_info)

    # Now that the data is loaded, we can modify it if needed
    if args.edit_pop_size:
        print(f"Editing population sizes by factor {args.factor}")
        for state in pops_data:
            for region in state['regions']:
                for pop in region['pops']:
                    original_size = pop['size']
                    pop['size'] = int(original_size * args.factor)
                    print(f"Updated pop size from {original_size} to {pop['size']} in {state['state_name']}")

    # Return the modified pops_data
    return pops_data
    
def export_population_data_to_json(pops_data, output_file):
    # Export the population data to a JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(pops_data, file, indent=4)  # Dump the data with indentation for readability


if __name__ == "__main__":
    pops_data = main()  # Get the pops_data from main()

    # Specify a single output file for all the states
    output_file = './output/history/pops/combined_population_data.txt'
    create_output_folder(os.path.dirname(output_file))

    # Export the population data into one file
    export_population_data(pops_data, output_file)

