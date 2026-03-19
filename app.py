import streamlit as st
import random
import re

st.set_page_config(page_title="Hobby Chatbot", page_icon="🎯", layout="centered")

# ----------------------------
# PAGE HEADER
# ----------------------------
st.title("🎯 Hobby Chatbot")
st.write("Tell me about your hobbies and I’ll have a real conversation with you about them!")

# ----------------------------
# HOBBY DATA
# ----------------------------
HOBBIES = {
    "gaming": {
        "keywords": [
            "gaming", "game", "games", "gamer", "video game", "playstation", "xbox",
            "nintendo", "pc gaming", "minecraft", "fortnite", "valorant", "fifa",
            "call of duty", "cod", "roblox"
        ],
        "openers": [
            "Gaming sounds fun. What kinds of games do you enjoy most?",
            "Nice, gaming is a great hobby. Do you like competitive games or more relaxed ones?",
            "That’s cool. Do you usually play on console, PC, or mobile?"
        ],
        "followups": [
            "What’s your favorite game right now?",
            "Do you play mostly alone or with friends?",
            "What do you enjoy most about gaming?"
        ]
    },
    "sports": {
        "keywords": [
            "sport", "sports", "football", "soccer", "basketball", "tennis", "running",
            "gym", "fitness", "workout", "swimming", "volleyball", "cycling",
            "boxing", "martial arts", "cricket", "baseball"
        ],
        "openers": [
            "Sports are awesome. Which sport do you enjoy the most?",
            "Nice, sports are a great way to stay active. What do you usually play?",
            "That’s great. Do you play for fun, fitness, or competition?"
        ],
        "followups": [
            "How often do you play or train?",
            "What do you enjoy most about it?",
            "How long have you been into sports?"
        ]
    },
    "music": {
        "keywords": [
            "music", "singing", "song", "songs", "artist", "artists", "band", "bands",
            "guitar", "piano", "drums", "violin", "rap", "produce", "producing",
            "beats", "dj", "playlist"
        ],
        "openers": [
            "Music is a great hobby. What kind of music do you like?",
            "Nice, are you more into listening to music or making it?",
            "That’s cool. Do you have a favorite artist or genre?"
        ],
        "followups": [
            "What song have you been listening to a lot lately?",
            "Do you play any instruments?",
            "What do you like most about music?"
        ]
    },
    "art": {
        "keywords": [
            "art", "draw", "drawing", "paint", "painting", "sketch", "sketching",
            "design", "digital art", "illustration", "creative", "craft", "crafting"
        ],
        "openers": [
            "Art is really creative. What kind of art do you make?",
            "Nice, do you prefer drawing, painting, or digital art?",
            "That sounds interesting. What do you usually like to create?"
        ],
        "followups": [
            "What inspires your art?",
            "How long have you been doing it?",
            "Do you usually share your work with others?"
        ]
    },
    "coding": {
        "keywords": [
            "coding", "programming", "developer", "python", "java", "javascript",
            "html", "css", "streamlit", "software", "web development", "build apps",
            "build websites", "react"
        ],
        "openers": [
            "Coding is a really cool hobby. What do you like building?",
            "Nice, what programming languages do you use most?",
            "That’s awesome. Do you enjoy web apps, games, or automation projects?"
        ],
        "followups": [
            "What project are you most proud of?",
            "How did you get into coding?",
            "What do you enjoy most about programming?"
        ]
    },
    "reading": {
        "keywords": [
            "reading", "books", "book", "novel", "novels", "manga", "comics",
            "fiction", "nonfiction", "stories", "literature"
        ],
        "openers": [
            "Reading is a great hobby. What kind of books do you like?",
            "Nice, do you prefer fiction, nonfiction, or manga?",
            "That’s cool. Do you have a favorite book or author?"
        ],
        "followups": [
            "What’s something good you’ve read recently?",
            "What genre do you enjoy most?",
            "What do you like most about reading?"
        ]
    },
    "cooking": {
        "keywords": [
            "cooking", "cook", "baking", "bake", "recipes", "recipe", "food",
            "dessert", "desserts", "kitchen"
        ],
        "openers": [
            "Cooking is such a fun hobby. What do you like making?",
            "Nice, are you more into cooking meals or baking desserts?",
            "That sounds good. What’s your favorite thing to cook?"
        ],
        "followups": [
            "Do you like experimenting with recipes?",
            "What dish are you best at making?",
            "What do you enjoy most about cooking?"
        ]
    },
    "photography": {
        "keywords": [
            "photography", "photos", "photo", "camera", "pictures", "photographer",
            "editing photos", "portraits", "landscape photography"
        ],
        "openers": [
            "Photography is a lovely hobby. What do you like taking pictures of?",
            "Nice, do you use a camera or your phone most of the time?",
            "That’s cool. Do you enjoy taking photos more, or editing them afterward?"
        ],
        "followups": [
            "What kind of photos do you enjoy most?",
            "What got you into photography?",
            "Do you share your photos online?"
        ]
    }
}

GENERIC_INTEREST_RESPONSES = [
    "That sounds really interesting. Tell me a bit more about it.",
    "Nice, what do you enjoy most about that?",
    "That’s cool. How did you get into it?",
    "I’d love to hear more. What makes it fun for you?"
]

# ----------------------------
# HELPERS
# ----------------------------
def clean_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def detect_hobbies(user_input: str):
    text = clean_text(user_input)
    found = []

    for hobby, info in HOBBIES.items():
        for keyword in info["keywords"]:
            kw = clean_text(keyword)
            if kw in text:
                found.append(hobby)
                break

    return list(dict.fromkeys(found))

def contains_any(text: str, words):
    return any(word in text for word in words)

def already_used(reply: str):
    return reply in st.session_state.bot_replies

def pick_new(options):
    shuffled = options[:]
    random.shuffle(shuffled)
    for option in shuffled:
        if not already_used(option):
            return option
    return random.choice(options)

def get_last_user_message():
    for sender, msg in reversed(st.session_state.messages):
        if sender == "You":
            return msg
    return ""

def reply_to_short_followup(user_input: str):
    """
    Handle short answers like:
    - everyday
    - for fun
    - with friends
    - because it helps me improve
    """
    text = clean_text(user_input)
    current_topic = st.session_state.current_hobby

    if not current_topic:
        return None

    # Frequency-style answers
    if contains_any(text, ["everyday", "every day", "daily", "often", "a lot", "weekly"]):
        if current_topic == "sports":
            return "That’s awesome. Training that often can really help you improve. What do you enjoy most about sports?"
        if current_topic == "gaming":
            return "Nice, you play a lot then. What kind of games keep you coming back?"
        return "That’s great consistency. What do you enjoy most about it?"

    # Motivation / reason
    if contains_any(text, ["for fun", "fun", "enjoy", "because", "improve", "relax", "relaxing", "stress"]):
        if current_topic == "sports":
            return "That makes sense. Sports can be fun and also a great way to improve yourself. What sport do you feel strongest in?"
        if current_topic == "gaming":
            return "That makes sense. Gaming can be a great way to have fun and relax. What games do you enjoy the most?"
        return "That makes sense. What part of it do you enjoy the most?"

    # Social answers
    if contains_any(text, ["friends", "family", "team", "teammates", "with people"]):
        return "That makes it even better. Doing hobbies with other people can be really fun. What’s your favorite moment you’ve had with it?"

    # Skill / preference answers
    if contains_any(text, ["i like", "my favorite", "favourite", "love"]):
        if current_topic == "sports":
            return "Nice! What do you like most about that sport?"
        if current_topic == "gaming":
            return "Nice! What do you like most about those games?"
        return "Nice! What do you like most about it?"

    return None

def generate_reply(user_input: str):
    text = clean_text(user_input)
    detected = detect_hobbies(user_input)

    # Greeting
    if text in ["hi", "hello", "hey", "hey there"]:
        return "Hey! Tell me about a hobby you enjoy, and I’ll chat with you about it."

    # Detect hobbies from current message
    if detected:
        for hobby in detected:
            if hobby not in st.session_state.user_hobbies:
                st.session_state.user_hobbies.append(hobby)

        # Update current topic
        st.session_state.current_hobby = detected[0]

        if len(detected) == 1:
            hobby = detected[0]
            opener = pick_new(HOBBIES[hobby]["openers"])
            followup = pick_new(HOBBIES[hobby]["followups"])
            return f"{opener} {followup}"

        hobby_names = ", ".join([h.title() for h in detected[:-1]]) + f" and {detected[-1].title()}"
        return f"You’re into {hobby_names}. That’s a really nice mix. Which one do you enjoy the most?"

    # Try to respond to short follow-ups using remembered context
    short_followup_reply = reply_to_short_followup(user_input)
    if short_followup_reply:
        return short_followup_reply

    # Handle recommendation-type questions better
    if "what is" in text or "what's" in text or "recommend" in text or "suggest" in text:
        if "game" in text:
            st.session_state.current_hobby = "gaming"
            return "If you want something fun that doesn’t require running, you could try board games, card games, puzzle games, or casual video games. Do you want ideas for mobile, console, or real-life games?"
        if "sport" in text:
            st.session_state.current_hobby = "sports"
            return "There are lots of fun sports depending on what you like. Some easier ones to start with are football, basketball, badminton, or swimming. Do you want something competitive or just for fun?"

    # Handle yes/no/very short vague answers with context
    if len(text.split()) <= 3:
        current = st.session_state.current_hobby
        if current == "sports":
            return pick_new([
                "Nice. What sport do you play the most?",
                "Cool. Do you play mainly for fun or to improve?",
                "Got it. What do you enjoy most about sports?"
            ])
        elif current == "gaming":
            return pick_new([
                "Nice. What games do you play most?",
                "Cool. Do you prefer action, sports, or story games?",
                "Got it. Do you usually play alone or with friends?"
            ])
        elif current == "music":
            return pick_new([
                "Nice. What kind of music do you enjoy most?",
                "Cool. Do you have a favorite artist?",
                "Got it. Do you listen to music a lot every day?"
            ])

    # If there is a current topic, continue naturally instead of repeating one sentence
    current = st.session_state.current_hobby
    if current == "sports":
        return pick_new([
            "That’s really cool. What got you interested in sports in the first place?",
            "Nice. Do you have a favorite sport or team?",
            "That sounds great. What part of sports do you enjoy most?"
        ])
    elif current == "gaming":
        return pick_new([
            "That sounds fun. What type of games do you usually enjoy most?",
            "Nice. Do you like playing competitively or just casually?",
            "That’s cool. What game have you been playing the most lately?"
        ])
    elif current == "coding":
        return pick_new([
            "That’s awesome. What kind of things do you like building?",
            "Nice. Which programming language do you enjoy using most?",
            "Very cool. Are you working on any projects right now?"
        ])
    elif current == "music":
        return pick_new([
            "That’s nice. What kind of music do you enjoy most?",
            "Cool. Is there an artist you never get tired of listening to?",
            "Nice. Do you like listening, singing, or making music more?"
        ])

    # Final fallback
    return pick_new(GENERIC_INTEREST_RESPONSES)

# ----------------------------
# SESSION STATE
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_hobbies" not in st.session_state:
    st.session_state.user_hobbies = []

if "current_hobby" not in st.session_state:
    st.session_state.current_hobby = None

if "bot_replies" not in st.session_state:
    st.session_state.bot_replies = []

# ----------------------------
# INPUT
# ----------------------------
user_input = st.text_input("You:", placeholder="Example: I like football and gaming")

if user_input:
    bot_reply = generate_reply(user_input)

    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Bot", bot_reply))
    st.session_state.bot_replies.append(bot_reply)

# ----------------------------
# CHAT DISPLAY
# ----------------------------
st.markdown("---")
for sender, message in st.session_state.messages:
    st.markdown(f"**{sender}:** {message}")

# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.header("About")
    st.write("This chatbot recognizes hobbies, keeps track of the current topic, and avoids repeating the same reply.")

    if st.session_state.user_hobbies:
        st.subheader("Recognized hobbies")
        for hobby in st.session_state.user_hobbies:
            st.write(f"- {hobby.title()}")

    if st.session_state.current_hobby:
        st.subheader("Current topic")
        st.write(st.session_state.current_hobby.title())

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.session_state.user_hobbies = []
        st.session_state.current_hobby = None
        st.session_state.bot_replies = []
        st.rerun()
