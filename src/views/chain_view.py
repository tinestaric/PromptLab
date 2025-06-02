"""
Chain view for the Prompt Engineering Workshop application.
Handles sequential prompt chaining with three stages.
"""
import streamlit as st
from typing import Dict, List, Optional, Tuple
from ..core.config_manager import config_manager
from ..services.azure_ai_service import azure_ai_service, ModelResponse
from ..ui.ui_components import UIComponents
from ..models.models import model_registry
from ..core.constants import *


def show_chain_view():
    """Chain application function for sequential prompt processing."""
    # Render page header
    UIComponents.render_page_header("Prompt Chaining Workshop", "Process prompts sequentially through three stages")
    
    # Get settings from config
    visible_models = config_manager.get_visible_models()
    show_pricing = config_manager.get_pricing_visibility()
    max_tokens = config_manager.get_max_tokens()
    
    # Initialize session state for chain
    if 'chain_state' not in st.session_state:
        st.session_state.chain_state = {
            'stage': 1,  # Current active stage (1, 2, or 3)
            'responses': {},  # Store responses from each stage
            'user_prompt': '',  # The input prompt that flows through the chain
        }
      # Configuration section
    st.subheader("Chain Configuration")
    
    # Add helpful explanation
    st.info("💡 **How it works:** Each stage processes the output from the previous stage. Configure different models, temperatures, and system prompts for each stage to create sophisticated processing pipelines.")
    
    # Global settings row
    col1, col2 = st.columns(2)
    with col1:
        global_max_tokens = st.number_input(
            "Max Tokens (applies to all stages)",
            min_value=1,
            max_value=max_tokens,
            value=min(1000, max_tokens),
            help=f"Maximum number of tokens to generate for each stage (up to {max_tokens})"
        )
    with col2:
        # Show chain progress
        chain_state = st.session_state.chain_state
        current_stage = chain_state['stage']
        completed_stages = len(chain_state.get('responses', {}))
        
        st.metric(
            label="Chain Progress", 
            value=f"Stage {current_stage}/3",
            delta=f"{completed_stages} completed"
        )
      # Three stage configuration
    stages_config = []
    for i in range(3):
        stage_num = i + 1
        
        # Add visual separator between stages
        if stage_num > 1:
            st.markdown("**↓ Flows to ↓**")
        
        st.markdown(f"### Stage {stage_num}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_model = st.selectbox(
                "Model",
                options=visible_models,
                key=f"stage_{stage_num}_model",
                help=f"Select model for stage {stage_num}"
            )
        
        with col2:
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=2.0,
                value=0.7,
                step=0.1,
                key=f"stage_{stage_num}_temperature",
                help="Higher values make the output more random"
            )
        
        with col3:
            # Show input source
            if stage_num == 1:
                st.markdown("**Input Source**")
                st.markdown("📝 User Prompt")
            else:
                st.markdown("**Input Source**")
                if stage_num == 3:
                    # Special handling for Stage 3
                    include_original = st.checkbox(
                        "Include original prompt",
                        key=f"stage_3_include_original",
                        help="Include the original user prompt alongside Stage 2 output for review/adjustment workflows"
                    )
                    if include_original:
                        st.markdown("🔗 Stage 2 Output + 📝 Original Prompt")
                    else:
                        st.markdown("🔗 Stage 2 Output")
                else:
                    st.markdown(f"🔗 Stage {stage_num - 1} Output")
        
        # System prompt for each stage
        system_prompt = st.text_area(
            f"Stage {stage_num} System Prompt",
            height=100,
            placeholder=f"System prompt for stage {stage_num}...",
            key=f"stage_{stage_num}_system_prompt",
            help=f"This prompt will guide how stage {stage_num} processes its input"
        )
        
        stages_config.append({
            'model': selected_model,
            'temperature': temperature,
            'system_prompt': system_prompt
        })
        
        # Show stage status and response
        _render_stage_status_and_response(stage_num, show_pricing)
    
    # User prompt input
    st.subheader("User Prompt")
    user_prompt = st.text_area(
        "Enter your initial prompt that will flow through the chain",
        height=150,
        placeholder="What would you like to process through the prompt chain?",
        key="chain_user_prompt"
    )
      # Control buttons
    st.subheader("Chain Controls")
    
    current_stage = st.session_state.chain_state['stage']
    responses = st.session_state.chain_state.get('responses', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Start/Restart button
        start_disabled = not user_prompt.strip()
        start_text = "Restart Chain" if responses else "Start Chain"
        if st.button(start_text, disabled=start_disabled, type="primary"):
            _start_chain(user_prompt, stages_config[0], global_max_tokens)
    
    with col2:
        # Stage 2 button
        stage2_disabled = not (current_stage >= 2 and 1 in responses)
        stage2_completed = 2 in responses
        stage2_text = "✅ Stage 2 Done" if stage2_completed else "Continue to Stage 2"
        if st.button(stage2_text, disabled=stage2_disabled or stage2_completed):
            _continue_chain(2, stages_config[1], global_max_tokens)
    
    with col3:
        # Stage 3 button
        stage3_disabled = not (current_stage >= 3 and 2 in responses)
        stage3_completed = 3 in responses
        stage3_text = "✅ Stage 3 Done" if stage3_completed else "Continue to Stage 3"
        if st.button(stage3_text, disabled=stage3_disabled or stage3_completed):
            _continue_chain(3, stages_config[2], global_max_tokens)
    
    with col4:
        # Reset button
        if st.button("Reset Chain", type="secondary"):
            st.session_state.chain_state = {
                'stage': 1,
                'responses': {},
                'user_prompt': '',
            }
            st.rerun()
    
    # Show completion message
    if len(responses) == 3:
        st.success("🎉 Chain completed! All three stages have been processed.")
        
        # Optional: Show total cost if pricing is enabled
        if show_pricing:
            total_cost = sum(response.cost for response in responses.values() if response.cost)
            if total_cost > 0:
                st.metric("Total Chain Cost", f"${total_cost:.6f}")


def _render_stage_status_and_response(stage_num: int, show_pricing: bool) -> None:
    """Render the status and response for a specific stage."""
    chain_state = st.session_state.chain_state
    current_stage = chain_state['stage']
    responses = chain_state.get('responses', {})
    
    # Determine stage status
    if stage_num in responses:
        status = "✅ Completed"
        status_color = "green"
    elif stage_num == current_stage and (stage_num == 1 or (stage_num - 1) in responses):
        status = "⏳ Ready to run"
        status_color = "orange"
    elif stage_num < current_stage:
        status = "⚠️ Skipped"
        status_color = "red"
    else:
        status = "⏸️ Waiting"
        status_color = "gray"
    
    # Create a nice status display
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"**Status:**")
    with col2:
        st.markdown(f":{status_color}[{status}]")
    
    # Show response if available
    if stage_num in responses:
        response = responses[stage_num]
        
        with st.expander(f"📄 Stage {stage_num} Response", expanded=(stage_num == current_stage)):
            # Model info
            st.caption(f"Generated by: **{response.model_name}**")
            
            # Response content
            st.text_area(
                "Output",
                value=response.content,
                height=200,
                disabled=True,
                key=f"stage_{stage_num}_response_display",
                label_visibility="collapsed"
            )
            
            # Show token usage and cost
            UIComponents._render_token_usage(response, show_pricing, compact=True)
            
            # Show character count for reference
            char_count = len(response.content)
            word_count = len(response.content.split())
            st.caption(f"Output: {char_count} characters, ~{word_count} words")
    else:
        with st.expander(f"📄 Stage {stage_num} Response", expanded=False):
            if stage_num == 1:
                st.info("Will process the user prompt you enter below")
            elif stage_num == 3:
                # Check if original prompt inclusion is enabled
                include_original_key = "stage_3_include_original"
                if include_original_key in st.session_state and st.session_state[include_original_key]:
                    st.info("Will process Stage 2 output combined with the original user prompt")
                else:
                    st.info("Will process the output from Stage 2")
            else:
                st.info(f"Will process the output from Stage {stage_num - 1}")
    
    st.markdown("---")  # Visual separator between stages


def _start_chain(user_prompt: str, stage_config: Dict, max_tokens: int) -> None:
    """Start the chain with the first stage."""
    try:
        with st.spinner("Processing Stage 1..."):
            response = azure_ai_service.generate_response(
                model_name=stage_config['model'],
                system_prompt=stage_config['system_prompt'],
                user_prompt=user_prompt,
                temperature=stage_config['temperature'],
                max_tokens=max_tokens
            )
        
        # Update chain state
        st.session_state.chain_state['responses'][1] = response
        st.session_state.chain_state['stage'] = 2
        st.session_state.chain_state['user_prompt'] = user_prompt
        
        st.success("Stage 1 completed! Ready for Stage 2.")
        st.rerun()
        
    except Exception as e:
        st.error(f"Error in Stage 1: {str(e)}")


def _continue_chain(stage_num: int, stage_config: Dict, max_tokens: int) -> None:
    """Continue the chain to the next stage."""
    try:
        # Get input from previous stage
        prev_stage = stage_num - 1
        prev_response = st.session_state.chain_state['responses'][prev_stage]
        
        # For Stage 3, check if we should include the original prompt
        if stage_num == 3 and st.session_state.get('stage_3_include_original', False):
            original_prompt = st.session_state.chain_state.get('user_prompt', '')
            input_prompt = f"Original Request:\n{original_prompt}\n\n---\n\nPrevious Stage Output:\n{prev_response.content}"
        else:
            input_prompt = prev_response.content
        
        with st.spinner(f"Processing Stage {stage_num}..."):
            response = azure_ai_service.generate_response(
                model_name=stage_config['model'],
                system_prompt=stage_config['system_prompt'],
                user_prompt=input_prompt,
                temperature=stage_config['temperature'],
                max_tokens=max_tokens
            )
        
        # Update chain state
        st.session_state.chain_state['responses'][stage_num] = response
        if stage_num < 3:
            st.session_state.chain_state['stage'] = stage_num + 1
        else:
            st.session_state.chain_state['stage'] = 3  # Final stage
        
        success_msg = f"Stage {stage_num} completed!"
        if stage_num < 3:
            success_msg += f" Ready for Stage {stage_num + 1}."
        else:
            success_msg += " Chain complete!"
        
        st.success(success_msg)
        st.rerun()
        
    except Exception as e:
        st.error(f"Error in Stage {stage_num}: {str(e)}")
