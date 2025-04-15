import streamlit as st
import os
from dotenv import load_dotenv
from config import get_visible_models, set_visible_models, get_pricing_visibility, set_pricing_visibility, get_max_tokens, set_max_tokens

# Load environment variables
load_dotenv()

# Admin configuration
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")  # Change this in production

# Set page config
st.set_page_config(
    page_title="Admin Controls - Prompt Engineering Workshop",
    page_icon="🔒",
    layout="wide"
)

# Title
st.title("Admin Controls")

# Available models
MODELS = {
    "DeepSeek-R1": "deepseek-r1",
    "DeepSeek-V3-0324": "deepseek-v3-0324",
    "GPT-4o": "gpt-4o",
    "GPT-4o-mini": "gpt-4o-mini",
    "O3-mini": "o3-mini",
    "Phi-4": "phi-4"
}

# Admin login
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Login form
if not st.session_state.is_admin:
    admin_password = st.text_input("Enter Admin Password", type="password")
    if st.button("Login"):
        if admin_password == ADMIN_PASSWORD:
            st.session_state.is_admin = True
            st.success("Logged in as admin")
            st.rerun()
        else:
            st.error("Incorrect password")
else:
    # Get current settings
    current_models = get_visible_models()
    show_pricing = get_pricing_visibility()
    max_tokens = get_max_tokens()
    
    # Model selection
    st.subheader("Model Settings")
    selected_models = st.multiselect(
        "Select models visible to users",
        options=list(MODELS.keys()),
        default=current_models
    )
    
    # Max tokens setting
    new_max_tokens = st.number_input(
        "Maximum allowed tokens",
        min_value=1,
        max_value=4000,
        value=max_tokens,
        help="Set the maximum number of tokens users can generate"
    )
    
    # Pricing visibility
    st.subheader("Display Settings")
    new_show_pricing = st.checkbox(
        "Show pricing details to users",
        value=show_pricing
    )
    
    # Save button
    if st.button("Save All Settings"):
        set_visible_models(selected_models)
        set_max_tokens(new_max_tokens)
        set_pricing_visibility(new_show_pricing)
        st.success("Settings saved!")
    
    # Logout button
    if st.button("Logout"):
        st.session_state.is_admin = False
        st.rerun() 