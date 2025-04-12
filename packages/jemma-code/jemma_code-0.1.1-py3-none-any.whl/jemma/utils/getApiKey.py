import os
from pathlib import Path


def get_api_key():
    # First check environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # If not in environment, check config file
    if not api_key:
        config_path = Path.home() / ".jemma" / "config"
        if config_path.exists():
            with open(config_path, "r") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        api_key = line.split("=")[1].strip()
    
    return api_key