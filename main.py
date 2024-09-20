import argparse
from database_builder import build_database
from modification_exporter import modify_and_export

def parse_arguments():
    parser = argparse.ArgumentParser(description="Vic3 State Tinkerer Tool")

    parser.add_argument('--mode', choices=['build-database', 'modify-export'], required=True, help='Choose the mode: build-database or modify-export')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode for verbose output')

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_arguments()

    if args.mode == 'build-database':
        build_database(debug=args.debug)  # Pass the debug flag to the function
    elif args.mode == 'modify-export':
        modify_and_export()  # Debug mode could be added here later if needed