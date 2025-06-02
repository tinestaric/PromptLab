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
DEFAULT_GENERATE_PROMPT_ENABLED = False

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

TEMPERATURE_HELP = "Higher values make the output more random, lower values make it more deterministic"
MAX_TOKENS_HELP_TEMPLATE = "Maximum number of tokens to generate (up to {max_tokens})"
COMPARISON_MODE_HELP = "Allow users to run the same prompt across all visible models"
ADMIN_MAX_TOKENS_HELP = "Set the maximum number of tokens users can generate"
GENERATE_PROMPT_HELP = "Enable AI-powered system prompt generation for users"

# Prompt Generation
PROMPT_GENERATION_PLACEHOLDER = """Given a task description or existing prompt, produce a detailed system prompt to guide a language model in completing the task effectively.

# Guidelines

- Understand the Task: Grasp the main objective, goals, requirements, constraints, and expected output.
- Minimal Changes: If an existing prompt is provided, improve it only if it's simple. For complex prompts, enhance clarity and add missing elements without altering the original structure.
- Reasoning Before Conclusions**: Encourage reasoning steps before any conclusions are reached. ATTENTION! If the user provides examples where the reasoning happens afterward, REVERSE the order! NEVER START EXAMPLES WITH CONCLUSIONS!
    - Reasoning Order: Call out reasoning portions of the prompt and conclusion parts (specific fields by name). For each, determine the ORDER in which this is done, and whether it needs to be reversed.
    - Conclusion, classifications, or results should ALWAYS appear last.
- Examples: Include high-quality examples if helpful, using placeholders [in brackets] for complex elements.
- What kinds of examples may need to be included, how many, and whether they are complex enough to benefit from placeholders.
- Clarity and Conciseness: Use clear, specific language. Avoid unnecessary instructions or bland statements.
- Formatting: Use markdown features for readability. DO NOT USE ``` CODE BLOCKS UNLESS SPECIFICALLY REQUESTED.
- Preserve User Content: If the input task or prompt includes extensive guidelines or examples, preserve them entirely, or as closely as possible. If they are vague, consider breaking down into sub-steps. Keep any details, guidelines, examples, variables, or placeholders provided by the user.
- Constants: DO include constants in the prompt, as they are not susceptible to prompt injection. Such as guides, rubrics, and examples.
- Output Format: Explicitly the most appropriate output format, in detail. This should include length and syntax (e.g. short sentence, paragraph, JSON, etc.)
    - For tasks outputting well-defined or structured data (classification, JSON, etc.) bias toward outputting a JSON.
    - JSON should never be wrapped in code blocks (```) unless explicitly requested.

The final prompt you output should adhere to the following structure below. Do not include any additional commentary, only output the completed system prompt. SPECIFICALLY, do not include any additional messages at the start or end of the prompt. (e.g. no "---")

[Concise instruction describing the task - this should be the first line in the prompt, no section header]

[Additional details as needed.]

[Optional sections with headings or bullet points for detailed steps.]

# Steps [optional]

[optional: a detailed breakdown of the steps necessary to accomplish the task]

# Output Format

[Specifically call out how the output should be formatted, be it response length, structure e.g. JSON, markdown, etc]

# Examples [optional]

[Optional: 1-3 well-defined examples with placeholders if necessary. Clearly mark where examples start and end, and what the input and output are. User placeholders as necessary.]
[If the examples are shorter than what a realistic example is expected to be, make a reference with () explaining how real examples should be longer / shorter / different. AND USE PLACEHOLDERS! ]

# Notes [optional]

[optional: edge cases, details, and an area to call or repeat out specific important considerations]"""

GENERATE_PROMPT_BUTTON_TEXT = "Generate Prompt"
PROMPT_DESCRIPTION_PLACEHOLDER = "What would you like the model to do?"

NO_RESPONSE_MESSAGE = "Enter your prompts and click 'Generate Response' to see the output here."
ADMIN_SETTINGS_SAVED = "Settings saved!"

# Column Layouts
SINGLE_MODE_COLUMNS = [1, 1]
COMPARISON_MODE_COLUMNS = [1, 2]
