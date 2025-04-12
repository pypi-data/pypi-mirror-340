import json
from pathlib import Path

def get_config():
    """Loads the configuration from the config.json file in the .jemma directory."""
    config_path = Path.home() / ".jemma" / "config.json"
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print("Configuration file not found. Please run jemma --configure.")
        return None
    except json.JSONDecodeError:
        print("Error decoding configuration file. Please run jemma --configure.")
        return None

if __name__ == '__main__':
    config = get_config()
    if config:
        print(f"Model: {config.get('model')}")
        print(f"Temperature: {config.get('settings', {}).get('temperature')}")