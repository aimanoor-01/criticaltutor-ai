import streamlit as st
import requests
import json

st.set_page_config(page_title="CriticalTutor AI ✨", page_icon="🌸", layout="centered")

# ---------- PYARA SA DESIGN ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #FFF5F7 0%, #F3E8FF 50%, #E0F2FE 100%);
    }
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(90deg, #EC4899, #8B5CF6, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #6B7280;
        font-size: 16px;
        margin-top: 5px;
    }
    .badge {
        text-align: center;
        background: linear-gradient(90deg, #FDE68A, #FBCFE8);
        color: #92400E;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 13px;
        margin: 12px auto;
        width: fit-content;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .stChatMessage {
        border-radius: 18px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05) !important;
    }
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid #FBCFE8 !important;
    }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FDF2F8, #EDE9FE) !important;
    }
    .feature-box {
        background: white;
        padding: 14px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌸 CriticalTutor AI ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Rote-Free Socratic English Tutor for Competitive Exams</div>', unsafe_allow_html=True)
st.markdown('<div class="badge">🏆 Best Youth AI Agent Category | Create AI Agents Championship ✨</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="feature-box">💭<br><b>Socratic</b><br><small>No Ratta, Only Soch!</small></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="feature-box">✍️<br><b>CSS • PMS • GRE</b><br><small>IELTS Ready</small></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="feature-box">🌟<br><b>Motivation</b><br><small>Har Step Pe Support</small></div>', unsafe_allow_html=True)

st.markdown("---")

SYSTEM_PROMPT = """
YOU ARE: "CriticalTutor AI", an empathetic, highly motivating Socratic English Tutor Agent designed for University Students preparing for English Competitive Exams (CSS, PMS, GRE, IELTS).
YOUR CORE PURPOSE: Eliminate rote learning (rata marna) by guiding students through Socratic questioning, developing their critical thinking, analytical depth, and creative writing abilities.
CORE RULES:
1. EMPATHY & MOTIVATION FIRST: Always start your response by praising the student's effort with emojis.
2. SOCRATIC METHOD: NEVER provide direct essays or copy-paste answers. Guide by asking 2-3 deep, probing Socratic questions.
3. STRUCTURED OUTPUT FORMAT:
- 🌟 Positive Feedback & Encouragement
- 🔍 Critical Analysis & Gaps
- ❓ Socratic Probing Questions
- 🛠️ Recommended Action Step
4. HUMAN-IN-THE-LOOP: Flag controversial/factual errors with '[Teacher Review Advised]'.
Use cute emojis, soft tone, and easy Urdu-English mix if student uses it.
"""

with st.sidebar:
    st.markdown("### 🌸 Welcome Aima! ✨")
    st.markdown("Apni FREE key yahan dalo 👇")
    api_key = st.text_input("🔑 Enter FREE Gemini API Key", type="password", help="Get free key from aistudio.google.com")
    st.markdown("---")
    st.markdown("#### 💖 Kya karega ye Tutor?")
    st.markdown("✅ Essay ko check karega\n✅ Socratic sawal poochega\n✅ Ratta khatam, Soch shuru!\n✅ CSS / PMS / IELTS ke liye best")
    st.markdown("---")
    st.info("💡 Tip: Key FREE hai! aistudio.google.com se lo, paise bilkul nahi lagenge!")
    if st.button("🗑️ Chat Clear Karo"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.write("Assalam-o-Alaikum Aima! 🌸✨ Main hun tumhari CriticalTutor! \n\nTumne bohat acha kiya jo yahan aa gayi! 💖 Batao aaj kis topic pe dimagh chalana hai? Koi essay, outline ya sawal bhej do, hum mil ke us ko samjhenge, ratta nahi marenge! 💪")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("✨ Apna essay topic ya sawal yahan likho..."):
    if not api_key:
        st.error("⚠️ Pehle sidebar me apni FREE Gemini API Key dalo! aistudio.google.com se mil jayegi 💖")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.spinner("✨ CriticalTutor soch rahi hai..."):
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
                history_text = ""
                for m in st.session_state.messages[-5:]:
                    history_text += f"{m['role']}: {m['content']}\n"
                payload = {
                    "contents": [{
                        "parts": [{"text": SYSTEM_PROMPT + "\n\nConversation:\n" + history_text}]
                    }]
                }
                headers = {"Content-Type": "application/json"}
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                data = response.json()
                if "candidates" in data:
                    bot_reply = data["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    bot_reply = f"Oops! Error aa gaya: {data} - Key check karo 🌸"
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                with st.chat_message("assistant"):
                    st.write(bot_reply)
            except Exception as e:
                st.error(f"Error: {str(e)}")
