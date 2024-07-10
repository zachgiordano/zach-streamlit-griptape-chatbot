import os
import requests
import streamlit as st

endpoint = os.environ["CHAT_ENDPOINT"]

# Show title and description.
st.title("💬 Griptape Structure Chatbot")
st.write(
    "This is a simple chatbot that uses a Griptape Structure to generate responses"
)

if "session_id" not in st.session_state:
    resp = requests.post(endpoint, json={"operation": "create_session"})
    st.session_state["session_id"] = resp.json()["session_id"]

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What is up?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = requests.post(endpoint, json={"operation": "message", "session_id": st.session_state["session_id"], "input": prompt})
    response_message = response.json()["output"]["value"]
    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write(response_message)
    st.session_state.messages.append({"role": "assistant", "content": response_message})
