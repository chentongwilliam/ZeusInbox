import os
from pathlib import Path
from typing import Dict, Any

def get_env_path() -> Path:
    """Get the path to the .env file"""
    return Path(__file__).parent.parent.parent / '.env'

def read_env() -> Dict[str, str]:
    """Read the .env file and return a dictionary of key-value pairs"""
    env_path = get_env_path()
    if not env_path.exists():
        return {}
    
    env_vars = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

def write_env(env_vars: Dict[str, Any]) -> None:
    """Write key-value pairs to the .env file"""
    env_path = get_env_path()
    
    # Read existing env vars
    existing_vars = read_env()
    
    # Update with new vars
    existing_vars.update(env_vars)
    
    # Write back to file
    with open(env_path, 'w') as f:
        for key, value in existing_vars.items():
            f.write(f"{key}={value}\n")

def update_email_settings(email: str, imap_server: str, imap_port: int, username: str, password: str, update_interval: int) -> None:
    """Update email settings in .env file"""
    env_vars = {
        'EMAIL_UPDATE_INTERVAL': str(update_interval)
    }
    write_env(env_vars)

def update_language_setting(language: str) -> None:
    """Update language setting in .env file"""
    env_vars = {'LANGUAGE': language}
    write_env(env_vars)

def get_language_setting() -> str:
    """Get language setting from .env file, default to 'en' if not set"""
    env_vars = read_env()
    return env_vars.get('LANGUAGE', 'en') 