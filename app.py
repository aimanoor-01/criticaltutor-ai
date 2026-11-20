import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="CriticalTutor AI", page_icon="🎓", layout="centered")

st.title("🎓 CriticalTutor AI")
st.subheader("Rote-Free Socratic English Tutor for Competitive Exams")
st.caption("🏆 Best Youth AI Agent Category | Create AI Agents Championship")

SYSTEM_PROMPT = """
YOU ARE: "CriticalTutor AI", an empathetic, highly motivating Socratic English Tutor Agent designed for University Students preparing for English Competitive Exams (CSS, PMS, GRE, IELTS).

YOUR CORE PURPOSE: Eliminate rote learning (rata marna) by guiding students through Socratic questioning, developing their critical thinking, analytical depth, and creative writing abilities.

CORE RULES & BEHAVIORS:
1. EMPATHY & MOTIVATION FIRST: Always start your response by praising the student's effort.
2. SOCRATIC METHOD (NO ROTE LEARNING): NEVER provide direct essays or copy-paste answers. Guide by asking 2-3 deep, probing Socratic questions.
3. STRUCTURED OUTPUT FORMAT:
- 🌟 Positive Feedback & Encouragement
- 🔍 Critical Analysis & Gaps
- ❓ Socratic Probing Questions
- 🛠️ Recommended Action Step
4. HUMAN-IN-THE-LOOP: Flag controversial/factual errors with '[Teacher Review Advised]'.
"""

with st.sidebar:
    st.header("⚙️ Agent Settings")
    api_key = st.text_input("Enter OpenAI API Key", type="password", help="Enter your OpenAI API key to activate the agent.")
    st.markdown("---")
    st.info("CriticalTutor AI helps university students build critical thinking skills through Socratic questioning - without rote learning!")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": SYSTEM_PROMPT}]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if user_input := st.chat_input("Enter your essay topic, outline, or question here..."):
    if not api_key:
        st.error("⚠️ Please enter your OpenAI API Key in the sidebar to start interacting with CriticalTutor AI!")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.spinner("CriticalTutor AI is analyzing your input..."):
            try:
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages,
                    temperature=0.7
                )
                bot_reply = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                with st.chat_message("assistant"):
                    st.write(bot_reply)
            except Exception as e:
                st.error(f"Error executing agent response: {str(e)}")
