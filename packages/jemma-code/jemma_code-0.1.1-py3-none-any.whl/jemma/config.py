 
from pathlib import Path
import sys
from jemma.utils.terminalPrettifier import successText, errorText, warningText

import json
 
from typing import Dict, Any

class JemmaConfig:
    _instance = None
    _config: Dict[str, Any] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JemmaConfig, cls).__new__(cls)
            cls._load_config()
        return cls._instance
    
    @classmethod
    def _load_config(cls):
        """Load config once per session"""
        config_path = Path.home() / ".jemma" / "config.json"
        try:
            with open(config_path, 'r') as f:
                cls._config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(errorText("Can't find your configurations, please run "+ warningText('jemma --configure') ))
            return None
    @property
    def model(self) -> str:
        return self._config.get('model', 'gemini-2.0-flash')
    
    @property
    def temperature(self) -> float:
        return self._config.get('settings', {}).get('temperature', 0.3)
    @property
    def max_output_tokens(self) -> float:
        return self._config.get('settings',{}).get('max_output_tokens',0)
    @property
    def api_base(self) -> str:
        return f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}"

# Global configuration instance
CONFIG = JemmaConfig()

def configure_jemma():
    """Interactive configuration setup for Jemma AI assistant"""
 
    CONFIG_PATH = Path.home() / ".jemma" /  "config.json"
    config_exists: bool = False
 
    # Check for existing configuration
    if CONFIG_PATH.exists():
        config_exists = True
        confirm = input("⚠️ Existing configuration found. Overwrite? [y/N] ").lower()
        if confirm != "y":
            print("Aborting configuration")
            sys.exit(0)
    
    # Default configuration
    config = {
        "model": CONFIG.model,
        "settings": {
            "temperature": CONFIG.temperature ,
            "max_output_tokens": CONFIG.max_output_tokens,
            "safety_settings": {
                "harassment": "block_only_high",
                "dangerous": "block_medium_and_above"
            }
        }
    }
    
    print(successText("\n✨ Welcome to Jemma Setup! ✨\n"))
    
    # Model Selection
    while True:
        print(f"Choose your preferred model(current, {CONFIG.model}):" if config_exists else "Choose your preferred model:")
        print("1. Gemini 2.0 Flash Lite (most cost effective model)")
        print("2. Gemini 2.0 Flash (most balanced model)")
        print("3. Gemini 1-5.pro (largest token window, great for mega codebases)")
        choice = input("> ").strip()
        
        if choice == "1":
            config["model"] = "gemini-2.0-flash-lite"
            break
        elif choice == "2":
            config["model"] = "gemini-2.0-flash"
            break
        elif choice =="3":
            config['model'] = "gemini-1.5-pro"
            break
        else:
            print(errorText(f"⚠️ Invalid choice '{choice}'. Please enter 1 or 2\n"))
    
    # Additional Configuration
    print("\n🔧 Optional Advanced Settings (press Enter to use defaults)")
    
    # Temperature setting
    try:
        temp_input = input(f"Temperature, value between 0.1 and 1.0(current {CONFIG.temperature})) " if config_exists else "Temperature, value between 0.1 and 1.0: default 0.3")
        if temp_input:
            temp = float(temp_input)
            config['settings']['temperature'] = max(0.0, min(1.0, temp))
    except ValueError:
        print(errorText("Invalid temperature value. Using default."))
    
    # Max tokens setting
    try:
        tokens_input = input(f"Max tokens *out*, max : models max output {CONFIG.max_output_tokens} " if config_exists else f"Max tokens {warningText('*out*')}, default: none ")
        if tokens_input:
            tokens = int(tokens_input)
            config['settings']['max_output_tokens'] = max(1, tokens)
    except ValueError:
        print(errorText("Invalid max tokens value. Using default."))
    
    # Save Configuration
    try:
        # Use json.dump with indentation for readability
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)
        
        # Verify the file was created
        if CONFIG_PATH.exists() and CONFIG_PATH.stat().st_size > 0:
            print(successText(f"\n✅ Configuration saved to {CONFIG_PATH}"))
            print(f"Your Jemma AI assistant is now configured to use {config['model']}")
            return True
        else:
            print(errorText("\n❌ Configuration file appears to be empty or not created"))
            return False
    except Exception as e:
        print(errorText(f"\n❌ Failed to save configuration: {str(e)}"))
        sys.exit(1)

 
 