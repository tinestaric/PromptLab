"""
Tests for the model registry and pricing functionality.
"""
import unittest
from src.models.models import ModelRegistry, ModelPricing, ModelInfo


class TestModelPricing(unittest.TestCase):
    """Test cases for ModelPricing."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pricing = ModelPricing(input_price=0.001, output_price=0.002)
    
    def test_calculate_cost(self):
        """Test cost calculation."""
        cost = self.pricing.calculate_cost(input_tokens=1000, output_tokens=500)
        expected_cost = (1000 / 1000) * 0.001 + (500 / 1000) * 0.002
        self.assertAlmostEqual(cost, expected_cost, places=6)
    
    def test_projected_costs(self):
        """Test projected cost calculations."""
        base_cost = 0.01
        projected = self.pricing.get_projected_costs(base_cost)
        
        self.assertEqual(projected['10x'], 0.1)
        self.assertEqual(projected['100x'], 1.0)
        self.assertEqual(projected['1000x'], 10.0)


class TestModelRegistry(unittest.TestCase):
    """Test cases for ModelRegistry."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.registry = ModelRegistry()
    
    def test_get_model_exists(self):
        """Test getting an existing model."""
        model = self.registry.get_model('GPT-4o')
        self.assertIsNotNone(model)
        self.assertEqual(model.display_name, 'GPT-4o')
        self.assertEqual(model.api_name, 'gpt-4o')
    
    def test_get_model_not_exists(self):
        """Test getting a non-existent model."""
        model = self.registry.get_model('NonExistentModel')
        self.assertIsNone(model)
    
    def test_get_api_name(self):
        """Test getting API name for a model."""
        api_name = self.registry.get_api_name('GPT-4o')
        self.assertEqual(api_name, 'gpt-4o')
    
    def test_get_pricing(self):
        """Test getting pricing for a model."""
        pricing = self.registry.get_pricing('GPT-4o')
        self.assertIsNotNone(pricing)
        self.assertIsInstance(pricing, ModelPricing)
    
    def test_get_all_models(self):
        """Test getting all available models."""
        models = self.registry.get_all_models()
        self.assertIsInstance(models, list)
        self.assertIn('GPT-4o', models)
        self.assertIn('Phi-4', models)


if __name__ == '__main__':
    unittest.main()
