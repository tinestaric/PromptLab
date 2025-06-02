"""
Tests for the ConfigManager class.
"""
import unittest
import tempfile
import os
import json
from src.core.config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.config_manager = ConfigManager(self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_get_default_value(self):
        """Test getting a default value when config file doesn't exist."""
        result = self.config_manager.get('non_existent_key', 'default_value')
        self.assertEqual(result, 'default_value')
    
    def test_set_and_get_value(self):
        """Test setting and getting a configuration value."""
        self.config_manager.set('test_key', 'test_value')
        result = self.config_manager.get('test_key')
        self.assertEqual(result, 'test_value')
    
    def test_update_multiple_values(self):
        """Test updating multiple configuration values at once."""
        updates = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 123
        }
        self.config_manager.update(updates)
        
        self.assertEqual(self.config_manager.get('key1'), 'value1')
        self.assertEqual(self.config_manager.get('key2'), 'value2')
        self.assertEqual(self.config_manager.get('key3'), 123)
    
    def test_visible_models_defaults(self):
        """Test default visible models."""
        models = self.config_manager.get_visible_models()
        self.assertEqual(models, ['GPT-4o'])
    
    def test_max_tokens_default(self):
        """Test default max tokens."""
        max_tokens = self.config_manager.get_max_tokens()
        self.assertEqual(max_tokens, 1000)


if __name__ == '__main__':
    unittest.main()
