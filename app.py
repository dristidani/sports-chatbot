import streamlit as st
import openai
import os.path

# Loading your API key  directly in the script
openai.api_key = 'your-api-key'  
os.environ["OPENAI_API_KEY"] = openai.api_key

# Define the name for the app
st.title("🏏⚽ Sports Chatbot 🏀🎾")
st.write("Ask me anything about sports!")

# Prompting Patterns
persona = "You are a friendly sports expert."
chain_of_thought = "Think through the problem step-by-step before providing the answer."

# Initialize chat history in session state
if 'history' not in st.session_state:
    st.session_state.history = []

def get_gpt3_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()

# Function to format messages for conversation
def format_messages(history, user_message):
    messages = [{"role": "system", "content": persona}]
    for message in history:
        messages.append({"role": message["role"], "content": message["content"]})
    messages.append({"role": "user", "content": user_message})
    return messages

# Display conversation history
st.write("### Conversation History")
for message in st.session_state.history:
    if message["role"] == "user":
        st.chat_message("user").markdown(message["content"])
    else:
        st.chat_message("assistant").markdown(message["content"])

# React to user input
if query := st.chat_input("Ask your question here:"):
    # Display user message in chat message container
    st.chat_message("user").markdown(query)
    # Add user message to chat history
    st.session_state.history.append({"role": "user", "content": query})

    # Format messages for the conversation
    messages = format_messages(st.session_state.history, query)
    
    # Get response from GPT-3
    response = get_gpt3_response(messages)
    
    # Append assistant response to history
    st.session_state.history.append({"role": "assistant", "content": response})
    
    # Display assistant response in chat message container
    st.chat_message("assistant").markdown(response)

# Button to clear chat messages
def clear_messages():
    st.session_state.history = []

st.button("Clear", help="Click to clear the chat", on_click=clear_messages)
