import json

def save_debug_json(data, filename):
    """Saves data as a JSON file for debugging purposes."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Debug JSON saved: {filename}")
