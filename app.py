"""
CriticalTutor AI - a Socratic English tutor for CSS / PMS / GRE / IELTS students.
Create AI Agents Championship - Youth AI Agent Category.

Runs in DEMO MODE: no API key, no internet, no credits needed.
The agent uses a rule-based "Socratic engine" so judges can test it instantly.

Run:  pip install -r requirements.txt
      streamlit run app.py
"""

import re
import time
import random
import streamlit as st

# --------------------------------------------------------------------------
# Page setup
# --------------------------------------------------------------------------
st.set_page_config(page_title="CriticalTutor AI", page_icon="🎓", layout="centered")

REVIEW_TAG = (
    "**[Teacher Review Advised: Please verify this historical/statistical fact "
    "with your subject instructor].**"
)

WELCOME = (
    "Assalam o Alaikum! 👋 I'm **CriticalTutor AI**. I won't write your essay "
    "for you, because exams test *your* thinking. Instead, I'll ask the questions "
    "that help you build it yourself.\n\n"
    "**Try one of these:**\n"
    "- Send an essay topic, e.g. *\"Is climate change a threat to developing economies?\"*\n"
    "- Paste a paragraph or thesis you've written (60+ words works best)\n"
    "- Tell me your exam (CSS, PMS, GRE or IELTS) and what you're stuck on"
)

# --------------------------------------------------------------------------
# Knowledge base for the demo Socratic engine
# --------------------------------------------------------------------------
TOPICS = {
    "climate": {
        "keys": ["climate", "global warming", "environment", "flood", "carbon", "emission"],
        "gaps": [
            "'Developing economies' is not one group. A flood-prone agrarian country and an oil exporter face very different risks.",
            "'Threat' is undefined. Is it a threat to growth, food security, health or political stability?",
        ],
        "questions": [
            "How would you define 'threat' in one sentence? Is it only GDP loss, or something wider?",
            "Countries that emit the least often suffer the most. How does that shape your thesis, and what responsibility falls on richer nations?",
            "Could climate change also create an opportunity for developing countries (green finance, renewable energy)? How would you answer a critic who says it can't?",
        ],
    },
    "technology": {
        "keys": ["technology", "artificial intelligence", " ai ", "social media", "internet", "digital", "automation"],
        "gaps": [
            "Essays on technology often treat it as automatically good or bad. Examiners reward the argument that depends on *context*.",
            "'Technology' is too broad. Which kind, and whose lives does it change?",
        ],
        "questions": [
            "Who benefits from this technology and who is left behind? What does that reveal about the real issue?",
            "Is the problem the technology itself, or how institutions and people use it?",
            "What would a skeptic say, and what is the strongest evidence you could offer in reply?",
        ],
    },
    "education": {
        "keys": ["education", "literacy", "school", "university", "curriculum", "rote", "learning"],
        "gaps": [
            "Generalizations like 'education solves everything' invite the question: which education, delivered how?",
            "Access, quality and relevance are three different problems, and they are often blended together.",
        ],
        "questions": [
            "If a country doubled school enrolment but quality stayed poor, what would actually change?",
            "What is the difference between being *educated* and being *certified*? Where does your topic sit between them?",
            "Which stakeholder (state, family, teacher, market) is most responsible, and what would the others say?",
        ],
    },
    "economy": {
        "keys": ["poverty", "economy", "economic", "inflation", "unemployment", "debt", "inequality", "trade"],
        "gaps": [
            "Economic essays can drift into listing statistics. A strong essay explains *causes* and *trade-offs*.",
            "Growth and development are not the same thing. Which one is your essay really about?",
        ],
        "questions": [
            "If GDP rises but inequality worsens, has the country improved? How does your answer shape your thesis?",
            "What is the root cause here, and what are merely symptoms?",
            "Which policy would you defend, and what would it cost? Who would lose out?",
        ],
    },
    "governance": {
        "keys": ["democracy", "governance", "corruption", "politics", "constitution", "rule of law", "justice", "terror", "extremism", "security"],
        "gaps": [
            "Political topics tempt writers into one-sided opinion. Examiners want balance and evidence together.",
            "Terms like 'democracy' or 'security' carry many meanings. Choosing one definition and defending it is a strength.",
        ],
        "questions": [
            "What does this term mean to you, and would a political theorist agree with your definition?",
            "Can you find a historical or regional case that contradicts your main claim? How does your essay survive it?",
            "Which institution, rather than which individual, is the real source of the problem or the solution?",
        ],
    },
    "society": {
        "keys": ["women", "gender", "youth", "population", "culture", "society", "family", "religion", "tolerance", "media"],
        "gaps": [
            "Social topics invite sweeping claims about 'society' or 'people'. Who exactly are you describing?",
            "Culture and policy interact. Is your essay treating one as fixed while the other changes?",
        ],
        "questions": [
            "Which group is most affected, and have you represented their perspective fairly?",
            "What is the difference between a *tradition* and a *barrier* in this issue?",
            "If a policymaker read your essay, what single action would they take after finishing it?",
        ],
    },
}

GENERIC = {
    "gaps": [
        "'{t}' needs a clear *position*. A yes/no or descriptive framing often hides the real argument.",
        "Key terms in this topic need defining in your own words, or the essay will rely on assumptions.",
    ],
    "questions": [
        "What is your one-sentence position on this topic, and what would make you change it?",
        "Which key term in this topic is the most debatable, and how would you define it?",
        "Who would disagree with you most strongly, and what is the best version of their argument?",
    ],
}

PRAISE_TOPIC = [
    "Great choice of topic! Picking something with real depth already shows exam awareness.",
    "Zabardast start! Bringing a clear topic to the table is the first step to a structured argument.",
    "Excellent: you've chosen a topic that lets you show analysis instead of memorized points.",
]
PRAISE_GENERIC = [
    "Thank you for sharing your thinking. Showing me your attempt is what makes real learning possible.",
    "Good effort! Asking for guidance instead of memorizing is exactly the right habit.",
]

EXAM_TIPS = {
    "css": "CSS examiners reward a clear thesis, balanced arguments and a Pakistan-relevant example.",
    "pms": "PMS essays value clear structure and practical, policy-minded reasoning.",
    "gre": "For the GRE Analyze an Issue task, take a position and address the opposing view explicitly.",
    "ielts": "For IELTS Task 2, answer the exact question asked and keep each paragraph to one main idea.",
}

# --------------------------------------------------------------------------
# Demo Socratic engine
# --------------------------------------------------------------------------

def classify(text: str) -> str:
    t = text.lower().strip()
    if re.search(r"\b(write|likh|likho|draft|give me)\b.*\b(essay|paragraph|answer|precis|summary)\b", t) \
            or "write my essay" in t or "complete essay" in t:
        return "essay_request"
    if len(t.split()) >= 60:
        return "draft"
    if len(t.split()) <= 3 and re.match(r"^(hi|hello|salam|assalam|hey|aoa)", t):
        return "greeting"
    return "topic"


def find_topic(text: str):
    t = f" {text.lower()} "
    for name, data in TOPICS.items():
        if any(k in t for k in data["keys"]):
            return name, data
    return None, None


def analyze_draft(text: str):
    """Return (strengths, gaps) from simple structural checks on a draft."""
    t = text.lower()
    strengths, gaps = [], []

    if re.search(r"\b(this essay|i argue|i contend|this paper|thesis|in this essay)\b", t):
        strengths.append("you state a clear position, which gives the reader a direction")
    else:
        gaps.append("I can't find an explicit **thesis**. Where, in one sentence, do you take a stand?")

    if re.search(r"\b(for example|for instance|such as|according to|in \d{4})\b|\d{2,}", t):
        strengths.append("you support your points with examples or figures")
    else:
        gaps.append("Your claims lack **evidence**. Which concrete example would make each claim hard to dismiss?")

    if re.search(r"\b(however|although|critics|on the other hand|nevertheless|while some)\b", t):
        strengths.append("you acknowledge an opposing view, a hallmark of critical writing")
    else:
        gaps.append("There is no **counter-argument**. What would your strongest critic say, and how do you respond?")

    if len(re.findall(r"\b(always|never|everyone|all people|nobody|undoubtedly)\b", t)) >= 1:
        gaps.append("Absolute words (*always, never, everyone*) are **broad generalizations**. Where might they fail?")

    if not strengths:
        strengths.append("you completed a full draft, which is the hardest step to start")
    return strengths, gaps


def detect_exam(text: str):
    t = text.lower()
    for k, tip in EXAM_TIPS.items():
        if re.search(rf"\b{k}\b", t):
            return k.upper(), tip
    return None, None


def build_response(text: str, turn: int) -> str:
    kind = classify(text)
    exam, exam_tip = detect_exam(text)
    topic_name, topic = find_topic(text)
    seed = random.Random(len(text) + turn)

    # ---- Section 1: Positive feedback
    if kind == "essay_request":
        praise = ("I love the ambition! Wanting a finished essay shows you care about the result. "
                  "But a memorized essay won't survive an unfamiliar exam question, so let's build *yours*.")
    elif kind == "draft":
        strengths, _ = analyze_draft(text)
        praise = "Real effort here: you wrote a full draft, and " + "; ".join(strengths) + "."
    elif topic:
        praise = seed.choice(PRAISE_TOPIC)
    else:
        praise = seed.choice(PRAISE_GENERIC)

    # ---- Section 2: Critical analysis & gaps
    if kind == "essay_request":
        gaps = ["A ready-made essay is **someone else's thinking**. Examiners can spot templated arguments quickly.",
                "The skill being tested is how you build a position, not how well you recall one."]
    elif kind == "draft":
        _, gaps = analyze_draft(text)
        if not gaps:
            gaps = ["Your structure is solid. The next level is **depth**: which of your claims is the weakest link?"]
    elif topic:
        gaps = topic["gaps"]
    else:
        short = text.strip().rstrip("?.!")[:80]
        gaps = [g.format(t=short) for g in GENERIC["gaps"]]

    # ---- Section 3: Socratic questions
    if kind == "draft":
        qs = [
            "Which single sentence in your draft would you defend hardest, and why?",
            "If your opponent only had 30 seconds, which weakness in your argument would they attack?",
            "What example have you *not* used yet that would surprise a reader?",
        ]
    elif topic:
        qs = topic["questions"]
    else:
        qs = GENERIC["questions"]

    # ---- Section 4: Action step
    if kind == "essay_request":
        action = ("Spend **10 minutes** writing: (1) the topic, (2) your position in one sentence, "
                  "(3) three bullet-point reasons. Send me those, not an essay, and we'll test them together.")
    elif kind == "draft":
        action = ("Spend **10 minutes** revising: add one missing element from the gaps above "
                  "(thesis, evidence or counter-argument), then send me the new version.")
    else:
        action = ("Spend **10 minutes** on a rough outline: (1) your thesis in one sentence, "
                  "(2) three supporting arguments, (3) one counter-argument with your reply. "
                  "No full sentences needed.")
    if exam_tip:
        action += f"\n\n*{exam} tip:* {exam_tip}"
    action += f"\n\nIf you use statistics or historical facts, double-check them. {REVIEW_TAG}"

    gaps_md = "\n".join(f"- {g}" for g in gaps)
    qs_md = "\n".join(f"{i}. {q}" for i, q in enumerate(qs, 1))

    return (
        f"### 🌟 Positive Feedback & Encouragement\n{praise}\n\n"
        f"### 🔍 Critical Analysis & Gaps\n{gaps_md}\n\n"
        f"### ❓ Socratic Probing Questions\n{qs_md}\n\n"
        f"### 🛠️ Recommended Action Step\n{action}"
    )


def stream_text(text: str):
    """Typing effect for the demo agent."""
    for chunk in re.findall(r"\S+\s*", text):
        yield chunk
        time.sleep(0.015)


# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
with st.sidebar:
    st.title("🎓 CriticalTutor AI")
    st.caption("Create AI Agents Championship")
    st.markdown("**Category:** Youth AI Agent")
    st.success("🟢 Status: Active (Demo Mode)")
    st.info("No API key needed. Everything runs locally for instant testing.")
    st.markdown(
        "**Mission:** Replace *rata marna* (rote learning) with critical thinking "
        "for CSS, PMS, GRE and IELTS students."
    )
    st.markdown(
        "**How it works**\n"
        "1. Share a topic or draft\n"
        "2. Get feedback, gaps and Socratic questions\n"
        "3. Do the 10-minute task, then reply\n"
    )
    if st.button("🗑️ Start new session", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": WELCOME}]
        st.rerun()

# --------------------------------------------------------------------------
# Chat UI with session memory
# --------------------------------------------------------------------------
st.title("🎓 CriticalTutor AI")
st.caption("Your Socratic English tutor: it asks, you think.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": WELCOME}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type a topic, thesis or draft paragraph..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    turn = sum(1 for m in st.session_state.messages if m["role"] == "user")
    reply = build_response(prompt, turn)

    with st.chat_message("assistant"):
        st.write_stream(stream_text(reply))
    st.session_state.messages.append({"role": "assistant", "content": reply})
