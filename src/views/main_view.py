"""
Main view for the Prompt Engineering Workshop application.
Handles the primary user interface for prompt testing and model interaction.
"""
import streamlit as st
from ..core.config_manager import config_manager
from ..services.azure_ai_service import azure_ai_service
from ..ui.ui_components import UIComponents
from ..core.constants import *


def show_main_view():
    """Main application function."""
    # Render page header
    UIComponents.render_page_header(APP_TITLE, '')
    
    # Get settings from config
    visible_models = config_manager.get_visible_models()
    show_pricing = config_manager.get_pricing_visibility()
    max_tokens = config_manager.get_max_tokens()
    
    # Create input column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Render input components
        system_prompt, user_prompt = UIComponents.render_prompt_inputs()
        selected_model, temperature, max_tokens_input = UIComponents.render_model_parameters(
            visible_models, max_tokens
        )
        
        # Submit button
        if st.button("Generate Response"):
            if not user_prompt.strip():
                st.error("Please enter a user prompt.")
                return
                
            try:
                # Generate response for single model
                response = azure_ai_service.generate_response(
                    model_name=selected_model,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens_input
                )
                st.session_state.last_response = response

            except Exception as e:
                UIComponents.render_error(str(e))
    
    with col2:
        # Display responses
        if 'last_response' in st.session_state:
            st.subheader("Model Response")
            UIComponents.render_single_response(st.session_state.last_response, show_pricing)
        else:
            st.subheader("Model Response")
            st.info(NO_RESPONSE_MESSAGE)
