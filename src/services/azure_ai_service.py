"""
Azure AI service layer for the Prompt Engineering Workshop.
Provides abstraction over Azure AI Inference API with error handling and response processing.
"""
import os
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import logging

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

from ..models.models import model_registry, ModelInfo

logger = logging.getLogger(__name__)

@dataclass
class TokenUsage:
    """Represents token usage information."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

@dataclass
class ModelResponse:
    """Represents a response from a model."""
    content: str
    usage: TokenUsage
    model_name: str
    cost: Optional[float] = None

class AzureAIService:
    """Service for interacting with Azure AI models."""
    
    def __init__(self):
        load_dotenv()
        self.client = self._initialize_client()
    
    def _initialize_client(self) -> ChatCompletionsClient:
        """Initialize the Azure AI Inference client."""
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_KEY")
        
        if not endpoint or not api_key:
            raise ValueError("Azure OpenAI endpoint and API key must be set in environment variables")
        
        return ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key)
        )
    
    def _create_messages(self, system_prompt: Optional[str], user_prompt: str) -> List:
        """Create message array for the API call."""
        messages = []
        if system_prompt and system_prompt.strip():
            messages.append(SystemMessage(content=system_prompt))
        messages.append(UserMessage(content=user_prompt))
        return messages
    
    def _calculate_cost(self, model_name: str, usage: TokenUsage) -> Optional[float]:
        """Calculate cost for the given model and usage."""
        pricing = model_registry.get_pricing(model_name)
        if pricing:
            return pricing.calculate_cost(usage.prompt_tokens, usage.completion_tokens)
        return None
    
    def generate_response(
        self,
        model_name: str,
        system_prompt: Optional[str],
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> ModelResponse:
        """Generate a response from a single model."""
        try:
            api_name = model_registry.get_api_name(model_name)
            if not api_name:
                raise ValueError(f"Unknown model: {model_name}")
            
            messages = self._create_messages(system_prompt, user_prompt)
            
            response = self.client.complete(
                messages=messages,
                model=api_name,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            usage = TokenUsage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens
            )
            
            cost = self._calculate_cost(model_name, usage)
            
            return ModelResponse(
                content=response.choices[0].message.content,
                usage=usage,
                model_name=model_name,
                cost=cost
            )
            
        except Exception as e:
            logger.error(f"Error generating response for model {model_name}: {e}")
            raise
    
    def generate_comparison_responses(
        self,
        model_names: List[str],
        system_prompt: Optional[str],
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict[str, ModelResponse]:
        """Generate responses from multiple models for comparison."""
        responses = {}
        errors = {}
        
        for model_name in model_names:
            try:
                response = self.generate_response(
                    model_name=model_name,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                responses[model_name] = response
            except Exception as e:
                logger.error(f"Error generating response for model {model_name}: {e}")
                errors[model_name] = str(e)
        
        if errors and not responses:
            # If all models failed, raise an exception with all errors
            error_details = "; ".join([f"{model}: {error}" for model, error in errors.items()])
            raise RuntimeError(f"All models failed to generate responses: {error_details}")
        elif errors:
            # Log partial failures but continue with successful responses
            logger.warning(f"Some models failed: {errors}")
        
        return responses

    def generate_system_prompt(
        self,
        user_description: str
    ) -> str:
        """Generate a system prompt based on user description using GPT-4o."""
        try:
            # Always use GPT-4o for prompt generation
            api_name = "gpt-4o"
            
            # Import here to avoid circular import
            from ..core.constants import PROMPT_GENERATION_PLACEHOLDER
            
            messages = [
                SystemMessage(content=PROMPT_GENERATION_PLACEHOLDER),
                UserMessage(content="Task, Goal, or Current Prompt:\n" + user_description)
            ]
            
            response = self.client.complete(
                messages=messages,
                model=api_name
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating system prompt: {e}")
            raise RuntimeError(f"Failed to generate system prompt: {str(e)}")

    def validate_model_availability(self, model_names: List[str]) -> Tuple[List[str], List[str]]:
        """Validate which models are available."""
        available = []
        unavailable = []
        
        for model_name in model_names:
            if model_registry.get_api_name(model_name):
                available.append(model_name)
            else:
                unavailable.append(model_name)
        
        return available, unavailable

# Global instance
azure_ai_service = AzureAIService()
