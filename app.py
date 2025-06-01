import streamlit as st
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from config import get_visible_models, get_pricing_visibility, get_max_tokens, get_comparison_mode
from model_config import MODEL_PRICING, MODELS # Import from model_config

# Load environment variables
load_dotenv()

# Admin configuration
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")  # Change this in production

# Initialize Azure AI Inference client
client = ChatCompletionsClient(
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("AZURE_OPENAI_KEY"))
)

# Available models and their pricing (per 1000 tokens)
# MODEL_PRICING = {
#     "DeepSeek-R1": {"input": 0.0005, "output": 0.0015},
#     "DeepSeek-V3-0324": {"input": 0.0005, "output": 0.0015},
#     "gpt-4.1": {"input": 0.005, "output": 0.015},
#     "gpt-4.1-nano": {"input": 0.0005, "output": 0.0015},
#     "gpt-4o": {"input": 0.005, "output": 0.015},
#     "gpt-4o-mini": {"input": 0.0005, "output": 0.0015},
#     "Llama-4-Scout-17B-16E-Instr": {"input": 0.001, "output": 0.003},
#     "mistral-medium-2505": {"input": 0.002, "output": 0.006},
#     "o1": {"input": 0.003, "output": 0.009},
#     "o3": {"input": 0.004, "output": 0.012},
#     "o4-mini": {"input": 0.0005, "output": 0.0015},
#     "Phi-4": {"input": 0.0005, "output": 0.0015},
#     "Phi-4-mini-reasoning": {"input": 0.0005, "output": 0.0015}
# }

# Available models
# MODELS = {
#     "DeepSeek-R1": "deepseek-r1",
#     "DeepSeek-V3-0324": "DeepSeek-V3-0324",
#     "gpt-4.1": "gpt-4.1",
#     "gpt-4.1-nano": "gpt-4.1-nano",
#     "gpt-4o": "gpt-4o",
#     "gpt-4o-mini": "gpt-4o-mini",
#     "Llama-4-Scout-17B-16E-Instr": "Llama-4-Scout-17B-16E-Instr",
#     "mistral-medium-2505": "mistral-medium-2505",
#     "o1": "o1",
#     "o3": "o3",
#     "o4-mini": "o4-mini",
#     "Phi-4": "phi-4",
#     "Phi-4-mini-reasoning": "Phi-4-mini-reasoning"
# }

# Set page config
st.set_page_config(
    page_title="Prompt Engineering Workshop",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Title and description
st.title("Prompt Engineering Workshop")
st.markdown("""
This interactive tool helps you learn about prompt engineering by experimenting with different prompts and model parameters.
""")

# Get settings from config
visible_models = get_visible_models()
show_pricing = get_pricing_visibility()
max_tokens = get_max_tokens()
comparison_mode = get_comparison_mode()

# Create input column
col1, col2 = st.columns([1, 2] if comparison_mode else [1, 1])

with col1:
    # System prompt input
    st.subheader("System Prompt")
    system_prompt = st.text_area(
        "Enter your system prompt here",
        height=150,
        placeholder="You are a helpful AI assistant...",
        key="system_prompt"
    )

    # User prompt input
    st.subheader("User Prompt")
    user_prompt = st.text_area(
        "Enter your user prompt here",
        height=150,
        placeholder="What would you like to ask the AI?",
        key="user_prompt"
    )

    # Model parameters
    st.subheader("Model Parameters")
    
    if not comparison_mode:
        # Single model selection
        selected_model = st.selectbox(
            "Select Model",
            options=visible_models
        )
    
    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher values make the output more random, lower values make it more deterministic"
    )
    
    # Max tokens input
    max_tokens_input = st.number_input(
        "Max Tokens",
        min_value=1,
        max_value=max_tokens,
        value=min(1000, max_tokens),
        help=f"Maximum number of tokens to generate (up to {max_tokens})"
    )

    # Submit button
    if st.button("Generate Response"):
        try:
            # Create the messages array
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            messages.append(UserMessage(content=user_prompt))

            if comparison_mode:
                # Generate responses for all visible models
                st.session_state.responses = {}
                for model_name in visible_models:
                    response = client.complete(
                        messages=messages,
                        model=MODELS[model_name],
                        temperature=temperature,
                        max_tokens=max_tokens_input
                    )
                    st.session_state.responses[model_name] = {
                        'content': response.choices[0].message.content,
                        'usage': {
                            'prompt_tokens': response.usage.prompt_tokens,
                            'completion_tokens': response.usage.completion_tokens,
                            'total_tokens': response.usage.total_tokens
                        }
                    }
            else:
                # Generate response for single model
                response = client.complete(
                    messages=messages,
                    model=MODELS[selected_model],
                    temperature=temperature,
                    max_tokens=max_tokens_input
                )
                st.session_state.last_response = response.choices[0].message.content
                st.session_state.token_usage = {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                }
                if show_pricing:
                    pricing = MODEL_PRICING[selected_model]
                    input_cost = (response.usage.prompt_tokens / 1000) * pricing['input']
                    output_cost = (response.usage.completion_tokens / 1000) * pricing['output']
                    st.session_state.cost = {
                        'total_cost': input_cost + output_cost
                    }

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

with col2:
    if comparison_mode and 'responses' in st.session_state:
        # Display responses from all models side by side
        for model_name in visible_models:
            if model_name in st.session_state.responses:
                response_data = st.session_state.responses[model_name]
                st.subheader(f"Response from {model_name}")
                st.text_area(
                    "Response",
                    value=response_data['content'],
                    height=200,
                    disabled=True,
                    key=f"response_{model_name}"
                )
                
                # Token usage for this model
                usage = response_data['usage']
                token_info = f"Tokens: {usage['prompt_tokens']} + {usage['completion_tokens']} = {usage['total_tokens']}"
                if show_pricing and 'cost' in response_data:
                    cost = response_data['cost']['total_cost']
                    token_info += f" | Cost: ${cost:.6f}"
                st.caption(token_info)
    else:
        # Display single model response
        st.subheader("Model Response")
        if 'last_response' in st.session_state:
            st.text_area(
                "Response",
                value=st.session_state.last_response,
                height=300,
                disabled=True,
                key="response_single"
            )
            
            # Compact token usage display
            if show_pricing and 'cost' in st.session_state:
                cost = st.session_state.cost['total_cost']
                token_info = f"Tokens: {st.session_state.token_usage['prompt_tokens']} + {st.session_state.token_usage['completion_tokens']} = {st.session_state.token_usage['total_tokens']} | Cost: ${cost:.6f}"
                st.caption(token_info)
                
                # Show projections on separate lines
                st.caption("Projected costs:")
                st.caption(f"10× : ${cost*10:.4f}")
                st.caption(f"100× : ${cost*100:.4f}")
                st.caption(f"1000× : ${cost*1000:.4f}")
            else:
                token_info = f"Tokens: {st.session_state.token_usage['prompt_tokens']} + {st.session_state.token_usage['completion_tokens']} = {st.session_state.token_usage['total_tokens']}"
                st.caption(token_info)
        else:
            st.info("Enter your prompts and click 'Generate Response' to see the output here.") 