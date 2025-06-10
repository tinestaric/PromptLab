"""
Model configuration and pricing management for the Prompt Engineering Workshop.
Provides structured access to model information and cost calculations.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional
import logging

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
        """Initialize the model registry with available models."""
        models_data = {
            "DeepSeek-R1": {
                "api_name": "deepseek-r1",
                "pricing": ModelPricing(0.00120, 0.00478),
                "description": "DeepSeek R1 reasoning model"
            },
            "DeepSeek-V3-0324": {
                "api_name": "DeepSeek-V3-0324",
                "pricing": ModelPricing(0.00101, 0.00404),
                "description": "DeepSeek V3 model"
            },
            "gpt-4.1": {
                "api_name": "gpt-4.1",
                "pricing": ModelPricing(0.00177, 0.00708),
                "description": "GPT-4.1 model"
            },
            "gpt-4.1-nano": {
                "api_name": "gpt-4.1-nano",
                "pricing": ModelPricing(0.00009, 0.00036),
                "description": "GPT-4.1 Nano model"
            },
            "GPT-4o": {
                "api_name": "gpt-4o",
                "pricing": ModelPricing(0.002212, 0.008848),
                "description": "GPT-4o model"
            },
            "GPT-4o-mini": {
                "api_name": "gpt-4o-mini",
                "pricing": ModelPricing(0.00013272, 0.0005309),
                "description": "GPT-4o Mini model"
            },
            "Llama-4-Scout-17B-16E-Instruct": {
                "api_name": "Llama-4-Scout-17B-16E-Instruct",
                "pricing": ModelPricing(0.001, 0.003),
                "description": "Llama 4 Scout model"
            },
            "mistral-medium-2505": {
                "api_name": "mistral-medium-2505",
                "pricing": ModelPricing(0.002, 0.006),
                "description": "Mistral Medium model"
            },
            "O1": {
                "api_name": "o1",
                "pricing": ModelPricing(0.0132720, 0.053087950),
                "description": "OpenAI O1 model"
            },
            "O3": {
                "api_name": "o3",
                "pricing": ModelPricing(0.00885, 0.03540),
                "description": "OpenAI O3 model"
            },
            "o4-mini": {
                "api_name": "o4-mini",
                "pricing": ModelPricing(0.00098, 0.00390),
                "description": "OpenAI o4 Mini model"
            },
            "Phi-4": {
                "api_name": "phi-4",
                "pricing": ModelPricing(0.000111, 0.00045),
                "description": "Microsoft Phi-4 model"
            },
            "Phi-4-mini-reasoning": {
                "api_name": "Phi-4-mini-reasoning",
                "pricing": ModelPricing(0.000067, 0.00027),
                "description": "Microsoft Phi-4 Mini Reasoning model"
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
