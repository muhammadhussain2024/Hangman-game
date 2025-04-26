import streamlit as st
import random

# Hangman visuals
HANGMAN_PICS = [
    "😃", "😯", "😦", "😣", "😫", "😵", "💀",
]

# Word list
WORDS = ["python", "streamlit", "hangman", "banana", "elephant", "notebook", "keyboard"]

# Sidebar with rules and scoreboard
st.sidebar.title("📜 Rules")
st.sidebar.markdown("""
- Guess the word one letter at a time.
- You have 6 chances.
- Each wrong guess brings you closer to 💀.
- Win by guessing all letters first!
""")

# Initialize scoreboard
if "wins" not in st.session_state:
    st.session_state.wins = 0
if "losses" not in st.session_state:
    st.session_state.losses = 0

# Display scoreboard
total_games = st.session_state.wins + st.session_state.losses
st.sidebar.title("📊 Scoreboard")
st.sidebar.markdown(f"**Total Games:** {total_games}")
st.sidebar.markdown(f"✅ Wins: {st.session_state.wins}")
st.sidebar.markdown(f"❌ Losses: {st.session_state.losses}")

# Game title
st.title("🎯 Hangman Game")

# Initialize game state
if "word" not in st.session_state:
    st.session_state.word = random.choice(WORDS)
    st.session_state.guessed = []
    st.session_state.wrong_guesses = 0
    st.session_state.game_over = False
    st.session_state.win = False
    st.session_state.guess = ""

# Handle guess function
def handle_guess():
    guess = st.session_state.guess.lower()
    if not guess.isalpha() or len(guess) != 1:
        st.warning("Please enter a single alphabet letter.")
    elif guess in st.session_state.guessed:
        st.info("You already guessed that letter.")
    elif guess in st.session_state.word:
        st.session_state.guessed.append(guess)
        if all(letter in st.session_state.guessed for letter in st.session_state.word):
            st.session_state.win = True
            st.session_state.game_over = True
    else:
        st.session_state.guessed.append(guess)
        st.session_state.wrong_guesses += 1
        if st.session_state.wrong_guesses >= 6:
            st.session_state.game_over = True
    st.session_state.guess = ""  # Clear input

# Display current word progress
word_display = " ".join([letter if letter in st.session_state.guessed else "_" for letter in st.session_state.word])
st.markdown(f"## Word: `{word_display}`")
st.markdown(f"### {HANGMAN_PICS[st.session_state.wrong_guesses]}")

# Input (auto-submits on Enter)
if not st.session_state.game_over:
    st.text_input("Enter a letter", key="guess", max_chars=1, on_change=handle_guess)

# Game result
if st.session_state.game_over:
    if st.session_state.win:
        st.success(f"🎉 You won! The word was **{st.session_state.word}**.")
    else:
        st.error(f"💀 Game Over! The word was **{st.session_state.word}**.")

    if st.button("🔄 Play Again"):
        if st.session_state.win:
            st.session_state.wins += 1
        else:
            st.session_state.losses += 1
        for key in ["word", "guessed", "wrong_guesses", "game_over", "win", "guess"]:
            del st.session_state[key]
