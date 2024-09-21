from database.database_build import build_database
import sys
import os

# Adds the parsing folder to Python’s path
sys.path.append(os.path.join(os.path.dirname(__file__), 'parsing'))

def interactive_prompt():
    print("Vic3 State Tinkerer Tool - Interactive Mode")
    print("Available commands:")
    print("1. build-database (or 'bd') - Build the database from the game files.")
    print("2. modify-export (or 'me') - Modify data and export it back into the game.")
    print("You can add '--debug' or '--edit-pop-size' after commands for additional functionality.")
    print("Type 'help' to list available commands or 'exit' to quit.")

    while True:
        user_input = input("Enter a command: ").strip().lower()
        args = user_input.split()

        # Extract the base command and any flags
        base_command = args[0] if args else ''
        flags = args[1:] if len(args) > 1 else []

        if base_command in ['help', 'h']:
            print("Commands:")
            print("1. build-database (or 'bd') - Build the database.")
            print("2. modify-export (or 'me') - Modify and export game files.")
            print("Optional parameters:")
            print("--edit-pop-size: Enable bulk population size editing.")
            print("--factor: Adjust population size by a factor.")
            print("--debug: Enable debug mode.")
        elif base_command in ['build-database', 'bd']:
            print("Building the database...")
            
            # Check if '--debug' flag is passed
            debug_mode = '--debug' in flags
            if debug_mode:
                print("Debug mode is ON")

            # Call the actual database building function
            build_database(debug=debug_mode)

        elif base_command in ['modify-export', 'me']:
            print("Modifying data and exporting...")

            # Check if '--debug' flag is passed
            debug_mode = '--debug' in flags
            if debug_mode:
                print("Debug mode is ON")

            # Call modify and export logic
            # modify_and_export(debug=debug_mode)
            # TODO uncomment and create modify_and_export function

        elif base_command == 'exit':
            print("Exiting the tool.")
            break
        else:
            print("Unknown command. Type 'help' for available commands.")

if __name__ == "__main__":

    # Use interactive prompt
    interactive_prompt()
