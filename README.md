🎓 CriticalTutor AI

A Socratic English tutor for CSS, PMS, GRE and IELTS students. Create AI Agents Championship | Best Youth AI Agent Category | By Aima

It asks, you think. Instead of writing ready-made essays that students memorize (rata marna), CriticalTutor AI guides them with probing questions so they build their own arguments.

🔗 Live demo: https://criticaltutor-ai-5ahhawumcgkkpwadbnyoxk.streamlit.app/

What it does

Every reply has four parts:

🌟 Positive Feedback & Encouragement
🔍 Critical Analysis & Gaps (broad generalizations, missing thesis, evidence or counter-argument)
❓ Socratic Probing Questions (2-3 questions that make the student think)
🛠️ Recommended Action Step (a 10-minute task, with a [Teacher Review Advised] safety check for facts and statistics)
Features
Clean chat interface built with st.chat_input and st.chat_message
Session memory with st.session_state.messages
Saved chats by nickname, and a "Clear my chat" button
Refuses to write essays on request and asks for a thesis and three reasons instead
10 topic areas: climate, technology, education, economy, governance, society, water, health, terrorism and gender
Demo Mode: no API key and no cost, so anyone can test it instantly
Run it locally
pip install -r requirements.txt
streamlit run app.py
How it works

The demo uses a rule-based Socratic engine written in Python. It detects the topic, checks drafts for a thesis, evidence and a counter-argument, and builds the four-part reply.

Roadmap
Connect an LLM that follows the same Socratic rules
Permanent cloud database for saved chats
Roman Urdu mode
Teacher dashboard and more exams
