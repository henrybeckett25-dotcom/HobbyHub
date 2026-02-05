import streamlit as st
import random

st.set_page_config(page_title="Hobby Chatbot", page_icon="🎯")

st.title("🎯 Hobby Chatbot")
st.write("Tell me your hobbies and I’ll chat with you about them!")

# Simple hobby responses
hobby_responses = {
    "gaming": [
        "Gaming is awesome! What games do you like?",
        "Nice! Are you into multiplayer or single player games?",
        "Do you play on PC, console, or mobile?"
    ],
    "sports": [
        "Sports keep you active! Which sport do you enjoy most?",
        "Do you play for fun or competitively?",
        "Who's your favorite team or athlete?"
    ],
    "music": [
        "Music is life! What kind of music do you like?",
        "Do you play any instruments?",
        "Who’s your favorite artist?"
    ],
    "art": [
        "Art is super creative! Do you draw, paint, or design?",
        "Digital art or traditional?",
        "What inspires your artwork?"
    ],
    "coding": [
        "Coding is a great hobby! What languages do you use?",
        "Are you building any cool projects?",
        "Do you prefer web, apps, or games?"
    ]
}

def chatbot_reply(user_input):
    user_input = user_input.lower()
    for hobby in hobby_responses:
        if hobby in user_input:
            return random.choice(hobby_responses[hobby])
    return "That sounds interesting! Tell me more about it 😊"

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("You:", key="input")

if user_input:
    reply = chatbot_reply(user_input)
    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Bot", reply))

for sender, message in st.session_state.messages:
    st.write(f"**{sender}:** {message}")
