"""
Configuration manager for the Prompt Engineering Workshop application.
Provides centralized configuration handling with improved error handling and caching.
"""
import json
import os
from typing import Any, Dict, List, Union
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    """Centralized configuration manager with caching and error handling."""
    
    def __init__(self, config_file: str = "config/model_config.json"):
        self.config_file = config_file
        self._cache = None
        self._cache_dirty = False
        
    @contextmanager
    def _file_lock(self):
        """Simple file locking mechanism (can be enhanced with proper file locking)."""
        try:
            yield
        finally:
            pass
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file with caching."""
        if self._cache is not None and not self._cache_dirty:
            return self._cache
            
        if not os.path.exists(self.config_file):
            self._cache = {}
            return self._cache
            
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self._cache = json.load(f)
                self._cache_dirty = False
                return self._cache
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"Failed to load config file {self.config_file}: {e}")
            self._cache = {}
            return self._cache
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file."""
        try:
            with self._file_lock():
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2)
                self._cache = config.copy()
                self._cache_dirty = False
        except OSError as e:
            logger.error(f"Failed to save config file {self.config_file}: {e}")
            raise
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        config = self._load_config()
        return config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        config = self._load_config()
        config[key] = value
        self._save_config(config)
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple configuration values at once."""
        config = self._load_config()
        config.update(updates)
        self._save_config(config)
    
    def get_visible_models(self) -> List[str]:
        """Get the currently visible models."""
        return self.get('visible_models', ['GPT-4o'])
    
    def set_visible_models(self, models: List[str]) -> None:
        """Set the visible models."""
        self.set('visible_models', models)
    
    def get_pricing_visibility(self) -> bool:
        """Get whether pricing details should be visible."""
        return self.get('show_pricing', False)
    
    def set_pricing_visibility(self, visible: bool) -> None:
        """Set whether pricing details should be visible."""
        self.set('show_pricing', visible)
    
    def get_max_tokens(self) -> int:
        """Get the maximum allowed tokens."""
        return self.get('max_tokens', 1000)
    
    def set_max_tokens(self, max_tokens: int) -> None:
        """Set the maximum allowed tokens."""
        self.set('max_tokens', max_tokens)
    
    def get_comparison_mode(self) -> bool:
        """Get whether comparison mode is enabled."""
        return self.get('comparison_mode', False)
    
    def set_comparison_mode(self, enabled: bool) -> None:
        """Set whether comparison mode is enabled."""
        self.set('comparison_mode', enabled)
    
    def get_generate_prompt_enabled(self) -> bool:
        """Get whether the generate prompt feature is enabled."""
        return self.get('generate_prompt_enabled', False)
    
    def set_generate_prompt_enabled(self, enabled: bool) -> None:
        """Set whether the generate prompt feature is enabled."""
        self.set('generate_prompt_enabled', enabled)

# Global instance
config_manager = ConfigManager()

# Backward compatibility functions
def get_visible_models() -> List[str]:
    return config_manager.get_visible_models()

def set_visible_models(models: List[str]) -> None:
    config_manager.set_visible_models(models)

def get_pricing_visibility() -> bool:
    return config_manager.get_pricing_visibility()

def set_pricing_visibility(visible: bool) -> None:
    config_manager.set_pricing_visibility(visible)

def get_max_tokens() -> int:
    return config_manager.get_max_tokens()

def set_max_tokens(max_tokens: int) -> None:
    config_manager.set_max_tokens(max_tokens)

def get_comparison_mode() -> bool:
    return config_manager.get_comparison_mode()

def set_comparison_mode(enabled: bool) -> None:
    config_manager.set_comparison_mode(enabled)

def get_generate_prompt_enabled() -> bool:
    return config_manager.get_generate_prompt_enabled()

def set_generate_prompt_enabled(enabled: bool) -> None:
    config_manager.set_generate_prompt_enabled(enabled)
