"""
Constants for the Prompt Engineering Workshop application.
Centralizes configuration values and default settings.
"""

# Application Configuration
APP_TITLE = "Prompt Engineering Workshop"
APP_ICON = "🤖"
APP_LAYOUT = "wide"

ADMIN_PAGE_TITLE = "Admin Controls - Prompt Engineering Workshop"
ADMIN_PAGE_ICON = "🔒"

# View Configuration
VALID_VIEWS = ["main", "admin"]
DEFAULT_VIEW = "main"

# Default Configuration Values
DEFAULT_VISIBLE_MODELS = ["GPT-4o"]
DEFAULT_MAX_TOKENS = 1000
DEFAULT_SHOW_PRICING = False
DEFAULT_COMPARISON_MODE = False
DEFAULT_TEMPERATURE = 0.7
DEFAULT_ADMIN_PASSWORD = "admin123"

# UI Configuration
SYSTEM_PROMPT_HEIGHT = 150
USER_PROMPT_HEIGHT = 150
SINGLE_RESPONSE_HEIGHT = 300
COMPARISON_RESPONSE_HEIGHT = 200

SYSTEM_PROMPT_PLACEHOLDER = "You are a helpful AI assistant..."
USER_PROMPT_PLACEHOLDER = "What would you like to ask the AI?"

# Temperature Configuration
MIN_TEMPERATURE = 0.0
MAX_TEMPERATURE = 2.0
TEMPERATURE_STEP = 0.1

# Token Configuration
MIN_TOKENS = 1
MAX_ADMIN_TOKENS = 4000

# File Configuration
CONFIG_FILE = "model_config.json"

# Environment Variables
ENV_AZURE_ENDPOINT = "AZURE_OPENAI_ENDPOINT"
ENV_AZURE_KEY = "AZURE_OPENAI_KEY"
ENV_ADMIN_PASSWORD = "ADMIN_PASSWORD"

# UI Text
APP_DESCRIPTION = """
This interactive tool helps you learn about prompt engineering by experimenting with different prompts and model parameters.
"""

TEMPERATURE_HELP = "Higher values make the output more random, lower values make it more deterministic"
MAX_TOKENS_HELP_TEMPLATE = "Maximum number of tokens to generate (up to {max_tokens})"
COMPARISON_MODE_HELP = "Allow users to run the same prompt across all visible models"
ADMIN_MAX_TOKENS_HELP = "Set the maximum number of tokens users can generate"

NO_RESPONSE_MESSAGE = "Enter your prompts and click 'Generate Response' to see the output here."
ADMIN_SETTINGS_SAVED = "Settings saved!"

# Column Layouts
SINGLE_MODE_COLUMNS = [1, 1]
COMPARISON_MODE_COLUMNS = [1, 2]
