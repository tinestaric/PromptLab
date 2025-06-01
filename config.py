import json
import os

CONFIG_FILE = "model_config.json"

def get_visible_models():
    """Get the currently visible models from config file"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('visible_models', ['GPT-4o'])
        except:
            return ['GPT-4o']
    return ['GPT-4o']

def set_visible_models(models):
    """Set the visible models in config file"""
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f) if os.path.exists(CONFIG_FILE) else {}
    config['visible_models'] = models
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def get_pricing_visibility():
    """Get whether pricing details should be visible"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('show_pricing', False)
        except:
            return False
    return False

def set_pricing_visibility(visible):
    """Set whether pricing details should be visible"""
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f) if os.path.exists(CONFIG_FILE) else {}
    config['show_pricing'] = visible
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def get_max_tokens():
    """Get the maximum allowed tokens"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('max_tokens', 1000)
        except:
            return 1000
    return 1000

def set_max_tokens(max_tokens):
    """Set the maximum allowed tokens"""
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f) if os.path.exists(CONFIG_FILE) else {}
    config['max_tokens'] = max_tokens
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def get_comparison_mode():
    """Get whether comparison mode is enabled"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('comparison_mode', False)
        except:
            return False
    return False

def set_comparison_mode(enabled):
    """Set whether comparison mode is enabled"""
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f) if os.path.exists(CONFIG_FILE) else {}
    config['comparison_mode'] = enabled
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f) 