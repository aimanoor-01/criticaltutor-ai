import streamlit as st
import requests
import json

# PASTE YOUR NEW API KEY HERE - INSIDE THE QUOTES
API_KEY = st.secrets.get("GEMINI_API_KEY", "")

st.set_page_config(page_title="CriticalTutor AI", page_icon="🎓", layout="centered")

st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #0F2043 0%, #1A365D 40%, #F8F9FA 40%, #F8F9FA 100%); }
    .top-bar { background: white; padding: 22px 20px; border-radius: 20px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.15); margin-top: 10px; }
    .main-title { font-size: 38px; font-weight: 800; color: #0F2043; margin: 0; }
    .main-title span { color: #C9A227; }
    .subtitle { color: #5A6C7D; font-size: 15px; margin-top: 6px; }
    .badge { display: inline-block; background: #0F2043; color: #FFD700; padding: 7px 16px; border-radius: 20px; font-weight: 700; font-size: 12px; margin-top: 12px; }
    .feature-box { background: white; padding: 16px 10px; border-radius: 16px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.07); border: 1px solid #E9ECEF; height: 110px; }
    .feature-box b { color: #0F2043; font-size: 14px; }
    .feature-box small { color: #6C757D; font-size: 12px; }
    .stChatMessage { border-radius: 16px !important; }
    div[data-testid="stSidebar"] { background: #0F2043 !important; }
    div[data-testid="stSidebar"] p, div[data-testid="stSidebar"] h3 { color: white !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="top-bar"><div class="main-title">🎓 CriticalTutor <span>AI</span></div><div class="subtitle">Socratic English Tutor for Competitive Exams | No Rote Learning, Only Critical Thinking</div><div class="badge">★ BEST YOUTH AI AGENT CATEGORY | CREATE AI AGENTS CHAMPIONSHIP</div></div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1: st.markdown('<div class="feature-box">💭<br><b>Socratic Method</b><br><small>Learn by Questioning<br>Not by Memorizing</small></div>', unsafe_allow_html=True)
with col2: st.markdown('<div class="feature-box">✍️<br><b>CSS • PMS • GRE • IELTS</b><br><small>Exam-Focused<br>Practice & Feedback</small></div>', unsafe_allow_html=True)
with col3: st.markdown('<div class="feature-box">🎯<br><b>Critical Thinking</b><br><small>Analysis • Logic<br>Structured Writing</small></div>', unsafe_allow_html=True)
st.markdown("---")

SYSTEM_PROMPT = """
YOU ARE: "CriticalTutor AI", a professional, encouraging Socratic English Tutor for CSS, PMS, GRE, IELTS aspirants.
RULES:
1. NEVER give a full ready-made essay. Guide the student to write it themselves.
2. ALWAYS use Socratic Method: Ask 2-3 powerful questions first.
3. STRUCTURE EVERY ANSWER:
   🌟 Positive Feedback
   🔍 Critical Analysis
   ❓ Socratic Questions
   🛠️ Next Action Step
4. TONE: Professional, warm, motivational, like a top CSS mentor.
5. If unsure about a fact, write '[Teacher Review Advised]'.
6. Use clear headings and bullet points.
"""

with st.sidebar:
    st.markdown("### 🎓 CriticalTutor AI")
    st.markdown("Welcome! Ask any essay topic, precis, comprehension, or grammar question.")
    st.markdown("---")
    st.markdown("**How it works:**\n1. Type your topic\n2. Get Socratic guidance\n3. Improve step-by-step")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.write("Hello and Welcome! 🎓 I am CriticalTutor AI. I will not give you ready-made answers - I will help you think, analyze, and write like a topper. What topic shall we work on today?")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("Type your essay topic or question here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    with st.spinner("CriticalTutor is thinking..."):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
            history_text = ""
            for m in st.session_state.messages[-5:]:
                history_text += f"{m['role']}: {m['content']}\n"
            payload = {"contents": [{"parts": [{"text": SYSTEM_PROMPT + "\\n\\nConversation:\\n" + history_text}]}]}
            response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
            data = response.json()
            if "candidates" in data:
                bot_reply = data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                bot_reply = f"Sorry, there was an issue. Error: {data}"
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            with st.chat_message("assistant"):
                st.write(bot_reply)
        except Exception as e:
            st.error(f"Error: {str(e)}")
