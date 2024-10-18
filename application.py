import streamlit as st
import requests
import json

# Set page configuration
st.set_page_config(page_title="Blockchain Query Assistant", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        font-family: Arial, sans-serif;
        font-size: 18px;
    }
    .stTextInput > div > div > input {
        font-size: 18px;
    }
    .stMarkdown {
        font-size: 18px;
    }
    .json-response {
        background-color: #f0f0f0;
        border-radius: 5px;
        padding: 10px;
        white-space: pre-wrap;
        font-family: monospace;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Blockchain Query Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            try:
                # Try to parse and format JSON response
                formatted_response = json.dumps(json.loads(message["content"]), indent=2)
                st.markdown(f"<div class='json-response'>{formatted_response}</div>", unsafe_allow_html=True)
            except json.JSONDecodeError:
                # If not JSON, display as regular markdown
                st.markdown(message["content"])
        else:
            st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question about blockchain transactions:"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send request to backend API
    api_url = "http://localhost:8002/api/v1/query"  # Update with your actual API endpoint
    response = requests.post(api_url, json={"query": prompt})

    if response.status_code == 200:
        assistant_response = response.json()
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            try:
                # Try to parse and format JSON response
                formatted_response = json.dumps(assistant_response, indent=2)
                st.markdown(f"<div class='json-response'>{formatted_response}</div>", unsafe_allow_html=True)
            except json.JSONDecodeError:
                # If not JSON, display as regular markdown
                st.markdown(assistant_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": json.dumps(assistant_response)})
    else:
        error_message = f"Error: {response.status_code} - {response.text}"
        with st.chat_message("assistant"):
            st.error(error_message)
        st.session_state.messages.append({"role": "assistant", "content": error_message})

# Add some space at the bottom to improve readability
st.markdown("<br><br>", unsafe_allow_html=True)