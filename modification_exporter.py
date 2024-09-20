import json
import os

def modify_and_export():
    # Load the database
    with open('./output/database.json', 'r', encoding='utf-8') as json_file:
        database = json.load(json_file)

    # Apply modifications (for example, reducing population by a factor)
    for state in database['pops']:
        for region in state['regions']:
            for pop in region['pops']:
                original_size = pop['size']
                pop['size'] = int(original_size * 0.5)  # Example modification: halve population size
                print(f"Updated pop size from {original_size} to {pop['size']} in {state['state_name']}")

    # Export the modified data into game-readable text files
    output_folder = './output/history/pops/'
    os.makedirs(output_folder, exist_ok=True)
    
    for state in database['pops']:
        output_file = os.path.join(output_folder, f"{state['state_name']}.txt")
        with open(output_file, 'w', encoding='utf-8-sig') as file:
            file.write(f"s:STATE_{state['state_name']} = {{\n")
            for region in state['regions']:
                file.write(f"\tregion_state:{region['region_state']} = {{\n")
                for pop in region['pops']:
                    file.write("\t\tcreate_pop = {\n")
                    file.write(f"\t\t\tculture = {pop['culture']}\n")
                    if 'religion' in pop:
                        file.write(f"\t\t\treligion = {pop['religion']}\n")
                    file.write(f"\t\t\tsize = {pop['size']}\n")
                    file.write("\t\t}\n")
                file.write("\t}\n")
            file.write("}\n\n")
    print("Modifications applied and exported to game-readable files.")
