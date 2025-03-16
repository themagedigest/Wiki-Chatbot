import streamlit as st
import requests

# Streamlit Page Config
st.set_page_config(page_title="Wikipedia Chatbot", layout="centered")

st.title("🤖 Wikipedia Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input (Text Box)
user_input = st.chat_input("Ask me a question about Amazon Company...")

# If user submits a message
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    payload = {"user_query": user_input}

    # Display User's Message Immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send request to FastAPI backend
    response = requests.post("http://127.0.0.1:8000/wiki_search/", json=payload)

    # Parse response
    if response.status_code == 200:
        bot_response = response.json().get("result", "I couldn't find an answer.")
    else:
        bot_response = "Sorry, something went wrong."

    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Display bot response
    with st.chat_message("assistant"):
        st.markdown(bot_response)
