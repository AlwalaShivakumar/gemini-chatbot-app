import streamlit as st
import google.generativeai as genai

# --- Page Configuration ---
st.set_page_config(
    page_title="Gemini Pro Chat",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- Sidebar ---
with st.sidebar:
    st.title("🧠 Gemini Pro Chat")
    st.markdown("This enhanced chatbot uses Google's Gemini Pro to provide intelligent and context-aware responses.")
    
    # Persona Selector
    st.subheader("Select AI Persona")
    persona_options = {
        "Default": "You are a helpful and friendly AI assistant.",
        "Sarcastic Teenager": "You are a sarcastic teenager who reluctantly answers questions with witty and slightly rude remarks.",
        "Code Master": "You are an expert programmer who provides concise, efficient, and well-explained code solutions. You only speak in code blocks and technical terms.",
        "Shakespearean Poet": "Thou art a poet from the age of Shakespeare. Respond to all inquiries with flourishing prose, rhyme, and iambic pentameter."
    }
    selected_persona_name = st.selectbox("Choose a personality for the AI:", options=list(persona_options.keys()))
    system_prompt = persona_options[selected_persona_name]
    
    # Add a divider
    st.divider()

    # Clear Chat Button
    if st.button("Clear Chat History", use_container_width=True, type="primary"):
        st.session_state.chat_session = None
        st.rerun()

# --- Main Application ---
st.title("Enhanced Gemini Chatbot")
st.write(f"Current Persona: **{selected_persona_name}**")

# --- API Key and Model Configuration ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name='gemini-pro',
        generation_config={'temperature': 0.7},
        system_instruction=system_prompt # Set the persona
    )
except (KeyError, ValueError) as e:
    st.error("🚨 API Key not found. Please add your GEMINI_API_KEY to Streamlit secrets.")
    st.stop()


# --- Chat Session Initialization ---
# Re-initialize the chat session if the persona changes or if it's the first run
if "chat_session" not in st.session_state or st.session_state.chat_session is None:
    st.session_state.chat_session = model.start_chat(history=[])

# --- Display Chat History ---
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# --- User Input Handling ---
user_prompt = st.chat_input("Ask me anything...")
if user_prompt:
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Show a spinner while generating the response
    with st.spinner("Gemini is thinking..."):
        try:
            gemini_response = st.session_state.chat_session.send_message(user_prompt)
            with st.chat_message("assistant"):
                st.markdown(gemini_response.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")