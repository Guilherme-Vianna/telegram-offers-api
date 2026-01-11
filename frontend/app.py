import streamlit as st
import requests
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Telegram Offers", layout="wide")

st.title("Telegram Offers Search")

# Search bar
search_term = st.text_input("Search offers...", "")

import os

# Fetch data from API
# Use environment variable for Docker compatibility
api_url = os.environ.get("API_URL", "http://127.0.0.1:8000/offers")
params = {"limit": 100}
if search_term:
    params["search"] = search_term

try:
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    offers = response.json()
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to API: {e}")
    offers = []

# Display results
st.write(f"Found {len(offers)} offers")

# Custom CSS for cards
st.markdown("""
<style>
    .offer-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
    }
    .offer-message {
        font-size: 16px;
        margin-bottom: 10px;
        white-space: pre-wrap; /* Preserve newlines */
    }
    .offer-link {
        color: #0066cc;
        text-decoration: none;
        font-weight: bold;
    }
    .offer-link:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# Grid layout for cards
for offer in offers:
    with st.container(border=True): # Use native container with border
        message = offer.get("message", "No message")
        link = offer.get("link")
        
        st.markdown(message)
        
        if link:
            # Use native link_button if available, or markdown link
            try:
                st.link_button("Open Link", link)
            except AttributeError:
                # Fallback for older Streamlit versions
                st.markdown(f"[Open Link]({link})", unsafe_allow_html=True)
