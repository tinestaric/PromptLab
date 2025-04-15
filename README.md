# Prompt Engineering Workshop App

This Streamlit application is designed for workshop attendees to learn about prompt engineering with Azure OpenAI models.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory with your Azure OpenAI credentials:
```
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=your_endpoint_here
```

3. Run the application:
```bash
streamlit run app.py
```

## Features

- System prompt input
- User prompt input
- Model selection (GPT-4, GPT-3.5-Turbo)
- Temperature control
- Max tokens configuration
- Real-time response display

## Usage

1. Enter your system prompt (optional)
2. Enter your user prompt
3. Select the model
4. Adjust temperature and max tokens as needed
5. Click "Generate Response" to see the output

## Note

Make sure you have valid Azure OpenAI credentials and the necessary model deployments set up in your Azure OpenAI service.