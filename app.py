import streamlit as st
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from config import get_visible_models, get_pricing_visibility, get_max_tokens

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
MODEL_PRICING = {
    "DeepSeek-R1": {"input": 0.0005, "output": 0.0015},
    "DeepSeek-V3-0324": {"input": 0.0005, "output": 0.0015},
    "GPT-4o": {"input": 0.005, "output": 0.015},
    "GPT-4o-mini": {"input": 0.0005, "output": 0.0015},
    "O3-mini": {"input": 0.0005, "output": 0.0015},
    "Phi-4": {"input": 0.0005, "output": 0.0015}
}

# Available models
MODELS = {
    "DeepSeek-R1": "deepseek-r1",
    "DeepSeek-V3-0324": "deepseek-v3-0324",
    "GPT-4o": "gpt-4o",
    "GPT-4o-mini": "gpt-4o-mini",
    "O3-mini": "o3-mini",
    "Phi-4": "phi-4"
}

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

# Create two columns for input and output
col1, col2 = st.columns([1, 1])

with col1:
    # System prompt input
    st.subheader("System Prompt")
    system_prompt = st.text_area(
        "Enter your system prompt here",
        height=150,
        placeholder="You are a helpful AI assistant..."
    )

    # User prompt input
    st.subheader("User Prompt")
    user_prompt = st.text_area(
        "Enter your user prompt here",
        height=150,
        placeholder="What would you like to ask the AI?"
    )

    # Model parameters
    st.subheader("Model Parameters")
    
    # Model selection
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

            # Make the API call
            response = client.complete(
                messages=messages,
                model=MODELS[selected_model],
                temperature=temperature,
                max_tokens=max_tokens_input
            )

            # Store the response and token usage in session state
            st.session_state.last_response = response.choices[0].message.content
            st.session_state.token_usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens
            }
            
            # Calculate cost if pricing is visible
            if show_pricing:
                pricing = MODEL_PRICING[selected_model]
                input_cost = (response.usage.prompt_tokens / 1000) * pricing['input']
                output_cost = (response.usage.completion_tokens / 1000) * pricing['output']
                total_cost = input_cost + output_cost
                
                st.session_state.cost = {
                    'input_cost': input_cost,
                    'output_cost': output_cost,
                    'total_cost': total_cost
                }

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

with col2:
    st.subheader("Model Response")
    
    # Display the response
    if 'last_response' in st.session_state:
        st.text_area(
            "Response",
            value=st.session_state.last_response,
            height=300,
            disabled=True
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