import os
import yaml

def load_config():
    config_path = os.path.join('config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def ensure_directories(config):
    """Create necessary directories if they don't exist."""
    os.makedirs(config['storage']['upload_dir'], exist_ok=True)
    os.makedirs(config['storage']['scan_dir'], exist_ok=True)

def check_auth(username, password, config):
    """Check if username and password match configured values."""
    if not config['server']['auth_enabled']:
        return True
        
    return (username == config['server']['username'] and 
            password == config['server']['password'])