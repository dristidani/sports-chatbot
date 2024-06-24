import streamlit as st
import openai
import os.path

# Loading your API key  directly in the script
openai.api_key = 'OPEN-API-KEY'  
os.environ["OPENAI_API_KEY"] = openai.api_key

# Define the name for the app
st.title("🏏⚽ Sports Chatbot 🏀🎾")
st.write("Ask me anything about sports!")

# Prompting Patterns
persona = "You are a knowledgeable and friendly sports analyst with expertise in all major sports."
chain_of_thought = "Explain your answer step-by-step, considering historical context, player statistics, and game rules."
examples = [
    {"role": "user", "content": "Who won the first Superbowl?"},
    {"role": "assistant", "content": "The Green Bay Packers won the first Superbowl in 1967."},
    {"role": "user", "content": "Explain the offside rule in soccer."},
    {"role": "assistant", "content": "The offside rule in soccer states that a player is offside if they are closer to the opponent's goal line than both the ball and the second last opponent when the ball is passed to them."}
]

def format_messages(history, user_message):
    messages = [{"role": "system", "content": f"{persona} {chain_of_thought}"}] + examples
    for message in history:
        messages.append({"role": message["role"], "content": message["content"]})
    messages.append({"role": "user", "content": user_message})
    return messages

def get_gpt3_response(messages):
    complete_response = ""
    max_response_length = 500  # Define an upper limit for the total response length
    total_tokens_used = 0

    while total_tokens_used < max_response_length:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,  # Moderate token limit
            temperature=0.7
        )
        response_text = response.choices[0].message['content'].strip()
        complete_response += response_text
        total_tokens_used += len(response_text.split())

        # Break if the response seems complete or reaches the token limit
        if len(response_text) < 200 or not response_text.endswith(('...', 'more')):
            break

        # Append the current response to the message history and continue
        messages.append({"role": "assistant", "content": response_text})
        messages.append({"role": "user", "content": "Continue."})

    return complete_response

# Initialize chat history in session state
if 'history' not in st.session_state:
    st.session_state.history = []

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
