import os
from pathlib import Path
 
from jemma.utils.terminalPrettifier import errorText, successText, warningText

def set_api_key():
    """Interactive configuration of the Gemini API key."""
    api_key = input("Enter your Gemini API key: ").strip()
    
    if api_key:
        # Create config directory if it doesn't exist
        config_dir = Path.home() / ".jemma"
        os.makedirs(config_dir, exist_ok=True)
        
        # Write API key to config file
        with open(config_dir / "config", "w") as f:
            f.write(f"GEMINI_API_KEY={api_key}\n")
        
        print(successText(f"API key saved to {config_dir}/config"))
        print(warningText('You should probably run '+ successText(text='jemma -configure',)+ warningText(' to set preferences')))
        return True
    else:
        print(errorText("No API key provided. Configuration cancelled."))
        return False