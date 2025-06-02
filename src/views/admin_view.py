"""
Admin view for the Prompt Engineering Workshop application.
Handles the administrative interface for application configuration.
"""
import streamlit as st
import os
from ..core.config_manager import config_manager
from ..models.models import model_registry
from ..ui.ui_components import UIComponents
from ..core.constants import *


def show_admin_view():
    """Admin interface function."""
    # Title
    st.title("Admin Controls")
    
    # Admin configuration
    admin_password = os.getenv(ENV_ADMIN_PASSWORD, DEFAULT_ADMIN_PASSWORD)
    
    # Admin login
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
    
    # Login form
    if not st.session_state.is_admin:
        _, login_success = UIComponents.render_admin_login(admin_password)
        if login_success:
            st.session_state.is_admin = True
            st.rerun()
    else:        # Get current settings
        current_models = config_manager.get_visible_models()
        show_pricing = config_manager.get_pricing_visibility()
        max_tokens = config_manager.get_max_tokens()
        comparison_mode = config_manager.get_comparison_mode()
        generate_prompt_enabled = config_manager.get_generate_prompt_enabled()
        all_models = model_registry.get_all_models()
        
        # Render admin controls
        selected_models, new_max_tokens, new_show_pricing, new_comparison_mode, new_generate_prompt_enabled = (
            UIComponents.render_admin_controls(
                current_models, all_models, max_tokens, show_pricing, comparison_mode, generate_prompt_enabled
            )
        )
        
        # Save button
        if st.button("Save All Settings"):
            config_manager.update({
                'visible_models': selected_models,
                'max_tokens': new_max_tokens,
                'show_pricing': new_show_pricing,
                'comparison_mode': new_comparison_mode,
                'generate_prompt_enabled': new_generate_prompt_enabled
            })
            st.success(ADMIN_SETTINGS_SAVED)
        
        # Logout button
        if st.button("Logout"):
            st.session_state.is_admin = False
            st.rerun()
            
        # Add helpful information about returning to main view
        st.markdown("---")
        st.info("💡 **Tip**: Remove `?view=admin` from the URL to return to the main application.")
