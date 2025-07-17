"""
Model configuration and pricing management for the Prompt Engineering Workshop.
Provides structured access to model information and cost calculations.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional
import logging
import json
import os

logger = logging.getLogger(__name__)

@dataclass
class ModelPricing:
    """Represents pricing information for a model."""
    input_price: float  # Price per 1000 input tokens
    output_price: float  # Price per 1000 output tokens
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate total cost for given token usage."""
        input_cost = (input_tokens / 1000) * self.input_price
        output_cost = (output_tokens / 1000) * self.output_price
        return input_cost + output_cost
    
    def get_projected_costs(self, base_cost: float) -> Dict[str, float]:
        """Get projected costs for different scales."""
        return {
            "10x": base_cost * 10,
            "100x": base_cost * 100,
            "1000x": base_cost * 1000
        }

@dataclass
class ModelInfo:
    """Represents information about a model."""
    display_name: str
    api_name: str
    pricing: ModelPricing
    description: Optional[str] = None
    max_tokens: Optional[int] = None

class ModelRegistry:
    """Registry for managing available models and their configurations."""
    
    def __init__(self):
        self._models: Dict[str, ModelInfo] = {}
        self._initialize_models()
    
    def _initialize_models(self) -> None:
        """Initialize the model registry with available models from JSON configuration."""
        try:
            # Get the path to the config directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'config')
            models_file = os.path.join(config_dir, 'models.json')
            
            if not os.path.exists(models_file):
                logger.warning(f"Models configuration file not found at {models_file}. Using default models.")
                self._load_default_models()
                return
            
            with open(models_file, 'r', encoding='utf-8') as f:
                models_config = json.load(f)
            
            models_data = models_config.get('models', {})
            
            for display_name, model_data in models_data.items():
                self._models[display_name] = ModelInfo(
                    display_name=display_name,
                    api_name=model_data["api_name"],
                    pricing=ModelPricing(
                        input_price=model_data["input_price"],
                        output_price=model_data["output_price"]
                    ),
                    description=model_data.get("description")
                )
            
            logger.info(f"Loaded {len(self._models)} models from configuration file")
            
        except Exception as e:
            logger.error(f"Error loading models configuration: {e}. Using default models.")
            self._load_default_models()
    
    def _load_default_models(self) -> None:
        """Load default models as fallback."""
        models_data = {
            "GPT-4o-mini": {
                "api_name": "gpt-4o-mini",
                "pricing": ModelPricing(0.00013272, 0.0005309),
                "description": "GPT-4o Mini model (default fallback)"
            }
        }
        
        for display_name, model_data in models_data.items():
            self._models[display_name] = ModelInfo(
                display_name=display_name,
                api_name=model_data["api_name"],
                pricing=model_data["pricing"],
                description=model_data.get("description")
            )
    
    def get_model(self, display_name: str) -> Optional[ModelInfo]:
        """Get model information by display name."""
        return self._models.get(display_name)
    
    def get_api_name(self, display_name: str) -> Optional[str]:
        """Get API name for a model by display name."""
        model = self.get_model(display_name)
        return model.api_name if model else None
    
    def get_pricing(self, display_name: str) -> Optional[ModelPricing]:
        """Get pricing information for a model."""
        model = self.get_model(display_name)
        return model.pricing if model else None
    
    def get_all_models(self) -> List[str]:
        """Get all available model display names."""
        return list(self._models.keys())
    
    def get_models_dict(self) -> Dict[str, str]:
        """Get dictionary mapping display names to API names (for backward compatibility)."""
        return {name: info.api_name for name, info in self._models.items()}
    
    def get_pricing_dict(self) -> Dict[str, Dict[str, float]]:
        """Get pricing dictionary (for backward compatibility)."""
        return {
            name: {"input": info.pricing.input_price, "output": info.pricing.output_price}
            for name, info in self._models.items()
        }

# Global instance
model_registry = ModelRegistry()

# Backward compatibility
MODEL_PRICING = model_registry.get_pricing_dict()
MODELS = model_registry.get_models_dict()
