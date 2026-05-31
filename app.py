import streamlit as st
import requests
from pypdf import PdfReader

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Om AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# SESSION STATE
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

# ----------------------------
# HEADER
# ----------------------------
st.markdown("""
# 🤖 Om AI Assistant

### Your Personal AI + PDF Assistant
Ask questions, upload PDFs, and chat locally with AI.
""")

st.info(
    "🟢 Local AI Running | 💬 Chat Mode | 📄 PDF Support Enabled"
)

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("🤖 Om AI Assistant")
st.sidebar.caption("Built with Python + Streamlit + Ollama")

st.sidebar.write("---")

st.sidebar.write("Model: qwen2.5:0.5b")

st.sidebar.metric(
    "Total Messages",
    len(st.session_state.messages)
)

# ----------------------------
# CLEAR CHAT
# ----------------------------
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ----------------------------
# SAVE CHAT
# ----------------------------
if st.sidebar.button("💾 Save Chat"):
    with open("chat_history.txt", "w", encoding="utf-8") as f:
        for msg in st.session_state.messages:
            f.write(
                f"{msg['role']}: {msg['content']}\n\n"
            )

    st.sidebar.success("Chat Saved!")

# ----------------------------
# PDF UPLOAD
# ----------------------------
uploaded_file = st.sidebar.file_uploader(
    "📄 Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    pdf_reader = PdfReader(uploaded_file)

    text = ""

    for page in pdf_reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    st.session_state.pdf_text = text

    st.sidebar.success("✅ PDF Loaded")

    st.sidebar.write(
        f"📊 Characters loaded: {len(text)}"
    )

    st.subheader("📄 PDF Preview")

    st.text_area(
        "Extracted Text",
        st.session_state.pdf_text[:2000],
        height=250
    )

# ----------------------------
# CHAT HISTORY
# ----------------------------
for message in st.session_state.messages:

    avatar = (
        "🧑"
        if message["role"] == "user"
        else "🤖"
    )

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.write(message["content"])

# ----------------------------
# CHAT INPUT
# ----------------------------
user_input = st.chat_input(
    "Ask me anything or ask questions about your PDF..."
)

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message(
        "user",
        avatar="🧑"
    ):
        st.write(user_input)

    # ------------------------
    # PDF MODE
    # ------------------------
    if st.session_state.pdf_text:

        prompt = f"""
Below is content extracted from a PDF document.

PDF CONTENT:
{st.session_state.pdf_text[:3000]}

Answer the user's question briefly and clearly.

Do not copy large sections of the PDF.
Summarize information in your own words.

User Question:
{user_input}

Answer:
"""

        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "qwen2.5:0.5b",
                "prompt": prompt,
                "stream": False
            }
        )

        bot_reply = response.json()["response"]

    # ------------------------
    # NORMAL CHAT MODE
    # ------------------------
    else:

        response = requests.post(
            "http://127.0.0.1:11434/api/chat",
            json={
                "model": "qwen2.5:0.5b",
                "messages": st.session_state.messages,
                "stream": False
            }
        )

        bot_reply = response.json()["message"]["content"]

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):
        st.write(bot_reply)

# ----------------------------
# FOOTER
# ----------------------------
st.write("---")

st.caption(
    "🚀 Om AI Assistant | Local AI Powered by Ollama"
)