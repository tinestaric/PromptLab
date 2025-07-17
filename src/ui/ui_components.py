"""
UI components for the Prompt Engineering Workshop application.
Provides reusable Streamlit components for consistent UI.
"""
import streamlit as st
from typing import List, Dict, Optional, Tuple, Any
from ..services.azure_ai_service import ModelResponse
from ..models.models import model_registry

class UIComponents:
    """Collection of reusable UI components."""
    
    @staticmethod
    def render_prompt_inputs() -> Tuple[str, str]:
        """Render prompt input components."""
        from ..core.config_manager import config_manager
        from ..core.constants import GENERATE_PROMPT_BUTTON_TEXT, EDIT_PROMPT_BUTTON_TEXT
        
        # System Prompt section with Generate/Edit Prompt button
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("System Prompt")
        with col2:
            # Show Generate/Edit Prompt button only if enabled in admin settings
            if config_manager.get_generate_prompt_enabled():
                # Check if system prompt exists to determine button text
                has_system_prompt = bool(st.session_state.get("system_prompt", "").strip())
                button_text = EDIT_PROMPT_BUTTON_TEXT if has_system_prompt else GENERATE_PROMPT_BUTTON_TEXT
                
                if st.button(button_text, key="generate_prompt_btn"):
                    # Clear the prompt description field when opening the modal
                    if "prompt_description" in st.session_state:
                        del st.session_state.prompt_description
                    UIComponents._show_generate_prompt_modal()
        
        system_prompt = st.text_area(
            "Enter your system prompt here",
            label_visibility='collapsed',            
            height=150,
            placeholder="You are a helpful AI assistant...",
            key="system_prompt"
        )

        st.subheader("User Prompt")
        user_prompt = st.text_area(
            "Enter your user prompt here",
            label_visibility='collapsed',
            height=150,
            placeholder="What would you like to ask the AI?",
            key="user_prompt"
        )
        
        return system_prompt, user_prompt
    
    @staticmethod
    def _show_generate_prompt_modal():
        """Show the generate prompt modal dialog."""
        from ..core.constants import (
            PROMPT_DESCRIPTION_PLACEHOLDER, 
            EDIT_PROMPT_DESCRIPTION_PLACEHOLDER,
            EDIT_PROMPT_GENERATION_PLACEHOLDER
        )
        from ..services.azure_ai_service import azure_ai_service
        
        # Check if we're editing an existing prompt
        has_system_prompt = bool(st.session_state.get("system_prompt", "").strip())
        is_editing = has_system_prompt
        
        # Use Streamlit's modal functionality
        modal_title = "Edit System Prompt" if is_editing else "Generate System Prompt"
        placeholder_text = EDIT_PROMPT_DESCRIPTION_PLACEHOLDER if is_editing else PROMPT_DESCRIPTION_PLACEHOLDER
        
        @st.dialog(modal_title)
        def generate_prompt_dialog():           
            user_description = st.text_area(
                "Prompt Description",
                placeholder=placeholder_text,
                height=100,
                key="prompt_description"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                button_text = "Edit" if is_editing else "Generate"
                if st.button(button_text, disabled=not user_description.strip()):
                    if user_description.strip():
                        try:
                            with st.spinner(f"{'Editing' if is_editing else 'Generating'} system prompt..."):
                                if is_editing:
                                    # Use edit prompt meta prompt (placeholder for now)
                                    # This will need the edit prompt generation method
                                    generated_prompt = azure_ai_service.edit_system_prompt(
                                        existing_prompt=st.session_state.get("system_prompt", ""),
                                        change_description=user_description
                                    )
                                else:
                                    # Use generate prompt meta prompt
                                    generated_prompt = azure_ai_service.generate_system_prompt(
                                        user_description=user_description
                                    )
                            
                            # Automatically use the generated prompt and close modal
                            st.session_state.system_prompt = generated_prompt
                            success_message = "System prompt edited and applied!" if is_editing else "System prompt generated and applied!"
                            st.success(success_message)
                            st.rerun()
                                
                        except Exception as e:
                            st.error(f"Failed to {'edit' if is_editing else 'generate'} prompt: {str(e)}")
            
            with col2:
                if st.button("Cancel"):
                    st.rerun()
        
        generate_prompt_dialog()
    
    @staticmethod
    def render_model_parameters(
        visible_models: List[str],
        max_tokens: int
    ) -> Tuple[Optional[str], float, int]:
        """Render model parameter controls."""
        st.subheader("Model Parameters")
        
        selected_model = st.selectbox(
            "Select Model",
            options=visible_models
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Higher values make the output more random, lower values make it more deterministic"
        )
        
        max_tokens_input = st.number_input(
            "Max Tokens",
            min_value=1,
            max_value=max_tokens,
            value=min(1000, max_tokens),
            help=f"Maximum number of tokens to generate (up to {max_tokens})"
        )
        
        return selected_model, temperature, max_tokens_input
    
    @staticmethod
    def render_single_response(response: ModelResponse, show_pricing: bool) -> None:
        """Render a single model response."""
        st.text_area(
            "Response",
            label_visibility='collapsed',
            value=response.content,
            height=300,
            disabled=True,
            key="response_single"
        )
        
        UIComponents._render_token_usage(response, show_pricing)
    
    @staticmethod
    def render_comparison_responses(
        responses: Dict[str, ModelResponse],
        visible_models: List[str],
        show_pricing: bool
    ) -> None:
        """Render multiple model responses for comparison."""
        for model_name in visible_models:
            if model_name in responses:
                response = responses[model_name]
                st.subheader(f"Response from {model_name}")
                st.text_area(
                    "Response",
                    value=response.content,
                    height=200,
                    disabled=True,
                    key=f"response_{model_name}"
                )
                
                UIComponents._render_token_usage(response, show_pricing, compact=True)
    
    @staticmethod
    def _render_token_usage(response: ModelResponse, show_pricing: bool, compact: bool = False) -> None:
        """Render token usage information."""
        usage = response.usage
        token_info = f"Tokens: {usage.prompt_tokens} (input) + {usage.completion_tokens} (output) = {usage.total_tokens}"
        
        if show_pricing and response.cost is not None:
            token_info += f" | Cost: ${response.cost:.6f}"
            
        st.caption(token_info)
        
        if show_pricing and response.cost is not None and not compact:
            # Show projections for single response mode
            pricing = model_registry.get_pricing(response.model_name)
            if pricing:
                projected = pricing.get_projected_costs(response.cost)
                st.caption("Projected costs:")
                for scale, cost in projected.items():
                    st.caption(f"{scale}: ${cost:.4f}")
    @staticmethod
    def render_error(error_message: str) -> None:
        """Render an error message."""
        st.error(f"An error occurred: {error_message}")
    
    @staticmethod
    def render_admin_login(admin_password: str) -> Tuple[str, bool]:
        """Render admin login form."""
        password = st.text_input("Enter Admin Password", type="password")
        login_clicked = st.button("Login")
        
        if login_clicked:
            if password == admin_password:
                st.success("Logged in as admin")
                return password, True
            else:
                st.error("Incorrect password")
        
        return password, False
    
    @staticmethod
    def render_admin_controls(
        current_models: List[str],
        all_models: List[str],
        max_tokens: int,
        show_pricing: bool,
        generate_prompt_enabled: bool
    ) -> Tuple[List[str], int, bool, bool]:
        """Render admin control panel."""
        from ..core.constants import GENERATE_PROMPT_HELP
        
        st.subheader("Model Settings")
        selected_models = st.multiselect(
            "Select models visible to users",
            options=all_models,
            default=current_models
        )
        
        new_max_tokens = st.number_input(
            "Maximum allowed tokens",
            min_value=1,
            max_value=4000,
            value=max_tokens,
            help="Set the maximum number of tokens users can generate"
        )
        
        st.subheader("Display Settings")
        new_show_pricing = st.checkbox(
            "Show pricing details to users",
            value=show_pricing
        )
        
        st.subheader("Feature Settings")
        new_generate_prompt_enabled = st.checkbox(
            "Enable AI-powered prompt generation",
            value=generate_prompt_enabled,
            help=GENERATE_PROMPT_HELP
        )
        
        return selected_models, new_max_tokens, new_show_pricing, new_generate_prompt_enabled
    
    @staticmethod
    def render_page_header(title: str, description: str) -> None:
        """Render page header with title and description."""
        st.title(title)
        st.markdown(description)
