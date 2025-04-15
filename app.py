import streamlit as st
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Azure AI Inference client
client = ChatCompletionsClient(
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("AZURE_OPENAI_KEY"))
)

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
    layout="wide"
)

# Title and description
st.title("Prompt Engineering Workshop")
st.markdown("""
This interactive tool helps you learn about prompt engineering by experimenting with different prompts and model parameters.
""")

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
        options=list(MODELS.keys())
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
    max_tokens = st.number_input(
        "Max Tokens",
        min_value=1,
        max_value=4000,
        value=1000,
        help="Maximum number of tokens to generate"
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
                max_tokens=max_tokens
            )

            # Store the response in session state
            st.session_state.last_response = response.choices[0].message.content

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

with col2:
    st.subheader("Model Response")
    
    # Display the response
    if 'last_response' in st.session_state:
        st.text_area(
            "Response",
            value=st.session_state.last_response,
            height=400,
            disabled=True
        )
    else:
        st.info("Enter your prompts and click 'Generate Response' to see the output here.") 