import logging
import os
import json

def make_log_folder():
    # Ensure the _log directory exists
    log_dir = './_log'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir

def setup_logger(debug=False):
    log_dir = make_log_folder()

    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        filename=os.path.join(log_dir, 'tool_log.log'),
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=log_level
    )
    logger = logging.getLogger()
    return logger

def save_debug_json(data, filename):
    """Saves data as a JSON file for debugging purposes."""
    
    log_dir = make_log_folder()

    # Create the full file path with _log directory and debug_ prefix
    full_filename = os.path.join(log_dir, f'debug_{filename}.json')

    # Write data to the JSON file
    with open(full_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    print(f"Debug JSON saved: {full_filename}")

def log_variable_to_file(variable, filepath):
    """Logs a variable (e.g., string or object) to a specified file."""
    # log_variable_to_file(large_string, f"./_log/states/{state_name}.txt")
    
    # Ensure the folder for the given filepath exists
    folder = os.path.dirname(filepath)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    # Write the variable to the file
    with open(filepath, 'w', encoding='utf-8') as f:
        # If the variable is not a string, convert it to string
        f.write(str(variable))

    print(f"Variable logged to: {filepath}")

def log_variable_to_file(variable, relative_filepath):
    """Logs a variable (e.g., string or object) to a file in the _log directory."""
    
    # Prepend the _log folder to the given relative filepath
    base_log_dir = './_log'
    full_filepath = os.path.join(base_log_dir, relative_filepath)

    # Ensure the folder for the full filepath exists
    folder = os.path.dirname(full_filepath)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    # Write the variable to the file
    with open(full_filepath, 'w', encoding='utf-8') as f:
        # If the variable is not a string, convert it to string
        f.write(str(variable))

    # print(f"Variable logged to: {full_filepath}")