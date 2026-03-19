
import streamlit as st
import random
import re

st.set_page_config(page_title="Hobby Chatbot", page_icon="🎯", layout="centered")

# ----------------------------
# PAGE HEADER
# ----------------------------
st.title("🎯 Hobby Chatbot")
st.write("Tell me about your hobbies, and I’ll chat with you about them in a smarter way!")

# ----------------------------
# HOBBY KNOWLEDGE BASE
# ----------------------------
HOBBY_DATA = {
    "gaming": {
        "keywords": [
            "gaming", "game", "games", "gamer", "playstation", "xbox", "nintendo",
            "pc gaming", "video game", "valorant", "minecraft", "fortnite", "fifa",
            "cod", "call of duty", "roblox"
        ],
        "responses": [
            "Gaming sounds fun! What kind of games do you enjoy most?",
            "Nice — are you more into competitive games, story games, or casual games?",
            "That’s cool! Do you usually play on PC, console, or mobile?"
        ],
        "followups": [
            "What’s your favorite game right now?",
            "Do you mostly play alone or with friends?",
            "What got you into gaming?"
        ]
    },
    "sports": {
        "keywords": [
            "sport", "sports", "football", "soccer", "basketball", "tennis", "running",
            "gym", "workout", "fitness", "volleyball", "cricket", "baseball", "swimming",
            "cycling", "boxing", "martial arts"
        ],
        "responses": [
            "Sports are a great hobby! Which one do you enjoy the most?",
            "Nice! Do you play just for fun, for fitness, or competitively?",
            "That’s awesome — how long have you been into it?"
        ],
        "followups": [
            "Do you have a favorite team or athlete?",
            "How often do you play or train?",
            "What do you enjoy most about it?"
        ]
    },
    "music": {
        "keywords": [
            "music", "singing", "songwriting", "guitar", "piano", "drums", "violin",
            "rap", "produce", "producing", "beat", "beats", "dj", "playlist", "artist",
            "band", "karaoke"
        ],
        "responses": [
            "Music is such a great hobby. Do you listen, sing, or play an instrument?",
            "Nice! What kind of music are you into?",
            "That’s awesome — do you have a favorite artist or genre?"
        ],
        "followups": [
            "Do you make music yourself or mainly listen to it?",
            "What song have you been replaying lately?",
            "How did you get into music?"
        ]
    },
    "art": {
        "keywords": [
            "art", "drawing", "draw", "painting", "paint", "sketch", "sketching",
            "illustration", "design", "digital art", "anime art", "craft", "crafting",
            "sculpting", "creative"
        ],
        "responses": [
            "Art is a wonderful hobby. What kind of art do you enjoy making?",
            "That’s really creative! Do you prefer digital art or traditional art?",
            "Nice! What do you usually like to draw or create?"
        ],
        "followups": [
            "What inspires your art?",
            "How long have you been doing it?",
            "Do you share your work online or keep it personal?"
        ]
    },
    "coding": {
        "keywords": [
            "coding", "programming", "developer", "python", "java", "javascript",
            "html", "css", "web development", "app development", "software",
            "streamlit", "react", "build websites", "build apps"
        ],
        "responses": [
            "Coding is a fantastic hobby! What do you like building?",
            "Nice — do you enjoy web development, apps, automation, or something else?",
            "That’s cool! Which programming languages do you use most?"
        ],
        "followups": [
            "Are you working on any project right now?",
            "What got you interested in coding?",
            "Do you prefer frontend, backend, or full-stack work?"
        ]
    },
    "reading": {
        "keywords": [
            "reading", "books", "novels", "manga", "comics", "fiction", "nonfiction",
            "story", "stories", "literature"
        ],
        "responses": [
            "Reading is a great hobby. What kind of books do you enjoy?",
            "Nice! Do you prefer fiction, nonfiction, manga, or something else?",
            "That sounds interesting — who’s one author you really like?"
        ],
        "followups": [
            "What’s the best thing you’ve read recently?",
            "Do you read every day or just when you have time?",
            "What genre do you always come back to?"
        ]
    },
    "cooking": {
        "keywords": [
            "cooking", "baking", "cook", "bake", "kitchen", "recipes", "food",
            "desserts", "meal prep"
        ],
        "responses": [
            "Cooking is such a useful and fun hobby. What do you like making?",
            "Nice! Are you more into cooking meals or baking sweets?",
            "That sounds delicious — do you experiment with recipes or follow them closely?"
        ],
        "followups": [
            "What’s your favorite thing to cook?",
            "Have you made anything recently that turned out really well?",
            "Do you cook more for fun or for everyday life?"
        ]
    },
    "photography": {
        "keywords": [
            "photography", "photos", "camera", "pictures", "editing photos", "photographer",
            "portrait", "landscape photography"
        ],
        "responses": [
            "Photography is a lovely hobby. What do you usually like taking photos of?",
            "Nice! Do you shoot on a phone or a camera?",
            "That’s cool — do you enjoy taking photos more, or editing them afterward?"
        ],
        "followups": [
            "What kind of photography interests you most?",
            "Do you post your photos anywhere?",
            "What got you into photography?"
        ]
    }
}

GENERAL_QUESTIONS = [
    "That sounds interesting! What do you enjoy most about it?",
    "Nice! How did you get into that hobby?",
    "That’s cool — how long have you been doing it?",
    "I’d love to hear more. What makes that hobby fun for you?"
]

# ----------------------------
# HELPER FUNCTIONS
# ----------------------------
def clean_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def detect_hobbies(user_input: str):
    """
    Detect one or more hobbies from the user message
    using simple keyword and phrase matching.
    """
    text = clean_text(user_input)
    found = []

    for hobby, info in HOBBY_DATA.items():
        for keyword in info["keywords"]:
            kw = clean_text(keyword)

            # Exact phrase match
            if kw in text:
                found.append(hobby)
                break

            # Flexible word-by-word match
            kw_parts = kw.split()
            if all(part in text.split() for part in kw_parts):
                found.append(hobby)
                break

    return list(dict.fromkeys(found))  # remove duplicates while keeping order

def detect_question_type(user_input: str):
    text = clean_text(user_input)

    if any(word in text for word in ["favorite", "favourite", "best"]):
        return "favorite"
    if any(word in text for word in ["how long", "since when"]):
        return "duration"
    if any(word in text for word in ["why", "what do you like", "what do you enjoy"]):
        return "reason"
    if any(word in text for word in ["hello", "hi", "hey"]):
        return "greeting"

    return "general"

def generate_reply(user_input: str):
    hobbies = detect_hobbies(user_input)
    question_type = detect_question_type(user_input)

    # Greeting
    if question_type == "greeting" and not hobbies:
        return "Hey! Tell me about a hobby you enjoy — like gaming, music, sports, coding, art, reading, cooking, or anything else."

    # If hobbies detected
    if hobbies:
        # Save recognized hobbies in session state memory
        for hobby in hobbies:
            if hobby not in st.session_state.user_hobbies:
                st.session_state.user_hobbies.append(hobby)

        if len(hobbies) == 1:
            hobby = hobbies[0]
            base_response = random.choice(HOBBY_DATA[hobby]["responses"])
            followup = random.choice(HOBBY_DATA[hobby]["followups"])
            return f"{base_response} {followup}"

        else:
            hobby_list = ", ".join(hobbies[:-1]) + f" and {hobbies[-1]}" if len(hobbies) > 1 else hobbies[0]
            return f"You’re into {hobby_list} — that’s a really cool mix. Which one do you spend the most time on?"

    # If no hobby detected but previous hobbies exist, stay conversational
    if st.session_state.user_hobbies:
        remembered = ", ".join(st.session_state.user_hobbies)
        return f"I remember you mentioned {remembered}. Tell me a bit more about what you like doing with that."

    # Fallback
    return random.choice(GENERAL_QUESTIONS)

# ----------------------------
# SESSION STATE
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_hobbies" not in st.session_state:
    st.session_state.user_hobbies = []

# ----------------------------
# CHAT INPUT
# ----------------------------
user_input = st.text_input("You:", placeholder="Example: I like football, gaming, and music")

if user_input:
    bot_reply = generate_reply(user_input)
    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Bot", bot_reply))

# ----------------------------
# DISPLAY CHAT
# ----------------------------
st.markdown("---")
for sender, message in st.session_state.messages:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**Bot:** {message}")

# ----------------------------
# OPTIONAL SIDEBAR
# ----------------------------
with st.sidebar:
    st.header("About")
    st.write("This chatbot recognizes hobbies more naturally and remembers the conversation.")
    
    if st.session_state.user_hobbies:
        st.subheader("Recognized hobbies")
        for hobby in st.session_state.user_hobbies:
            st.write(f"- {hobby.title()}")

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.session_state.user_hobbies = []
        st.rerun()
