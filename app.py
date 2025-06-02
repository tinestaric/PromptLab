import streamlit as st
import logging
from dotenv import load_dotenv
from src.views.main_view import show_main_view
from src.views.admin_view import show_admin_view
from src.views.chain_view import show_chain_view
from src.core.constants import *

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get view parameter from URL (needs to be accessed early for page config)
try:
    view = st.query_params.get("view", DEFAULT_VIEW)
except:
    view = DEFAULT_VIEW

# Set page config based on view
if view == "admin":
    st.set_page_config(
        page_title=ADMIN_PAGE_TITLE,
        page_icon=ADMIN_PAGE_ICON,
        layout=APP_LAYOUT
    )
else:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout=APP_LAYOUT
    )

def main():
    """Main routing function."""
    # Get view parameter from URL (access again within app context)
    view = st.query_params.get("view", DEFAULT_VIEW)
    
    # Access control
    if view not in VALID_VIEWS:
        st.error(f"Invalid view specified: '{view}'. Valid views are: {VALID_VIEWS}")
        st.stop()
    
    # Show appropriate view based on URL
    if view == "main":
        show_main_view()
    elif view == "admin":
        show_admin_view()
    elif view == "chain":
        show_chain_view()
    else:
        st.error(f"Unknown view: '{view}'")

if __name__ == "__main__":
    main() 