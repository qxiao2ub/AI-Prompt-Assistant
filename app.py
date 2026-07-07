from __future__ import annotations

import json
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path

import pandas as pd
import streamlit as st

from src.assistant_engine import BanditRanker, SuggestionEngine, clean_history_df, default_history_df

APP_NAME = "Yashvi AI Prompt Assistant"
DATA_PATH = Path("data/sample_user_history.csv")


@st.cache_data(show_spinner=False)
def load_default_history() -> pd.DataFrame:
    if DATA_PATH.exists():
        return clean_history_df(pd.read_csv(DATA_PATH))
    return default_history_df()


def read_uploaded_history(uploaded_file) -> pd.DataFrame:
    if uploaded_file is None:
        return load_default_history()
    try:
        return clean_history_df(pd.read_csv(uploaded_file))
    except Exception as exc:
        st.error(f"Could not read the uploaded CSV: {exc}")
        return load_default_history()


def current_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


st.set_page_config(page_title=APP_NAME, page_icon="YA", layout="wide")

if "session_history" not in st.session_state:
    st.session_state.session_history = []
if "last_suggestions" not in st.session_state:
    st.session_state.last_suggestions = []
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""
if "last_context" not in st.session_state:
    st.session_state.last_context = "email"

st.title(APP_NAME)
st.caption(
    "A portfolio-ready Streamlit prototype that learns from approved writing examples "
    "and suggests next phrases for email, notes, reports, and searches."
)

with st.sidebar:
    st.header("Project controls")
    uploaded = st.file_uploader("Optional: upload writing history CSV", type=["csv"])
    st.markdown(
        "CSV format: one required column named `user_input`; optional column named `context`. "
        "The app runs without uploading any file by using sample demo data."
    )
    st.divider()
    st.subheader("Privacy-first design")
    st.write(
        "This prototype does not use external APIs, does not require an API key, and does not store data in a database. "
        "Session history exists only for the active Streamlit session unless you download it."
    )
    st.divider()
    st.subheader("Model pieces")
    st.markdown(
        "- N-gram next phrase predictor\n"
        "- TF-IDF similarity personalization\n"
        "- Template fallback suggestions\n"
        "- Bandit-style accept/reject feedback ranking"
    )

history = read_uploaded_history(uploaded)
if st.session_state.session_history:
    history = pd.concat([history, pd.DataFrame(st.session_state.session_history)], ignore_index=True)
    history = clean_history_df(history)

engine = SuggestionEngine(history)
ranker = BanditRanker(st.session_state)

main_col, insight_col = st.columns([2.1, 1])

with main_col:
    st.subheader("Write with AI suggestions")
    context = st.selectbox(
        "Writing context",
        ["email", "search", "note", "report", "general"],
        index=["email", "search", "note", "report", "general"].index(st.session_state.last_context)
        if st.session_state.last_context in ["email", "search", "note", "report", "general"]
        else 0,
    )
    prompt = st.text_area(
        "Start typing",
        value=st.session_state.last_prompt,
        height=170,
        placeholder="Example: Dear team, thank you for...",
    )
    controls = st.columns([1, 1, 1])
    with controls[0]:
        top_k = st.slider("Number of suggestions", min_value=3, max_value=8, value=5)
    with controls[1]:
        add_to_history = st.checkbox("Learn from this session text", value=True)
    with controls[2]:
        st.write("")
        st.write("")
        generate = st.button("Generate suggestions", type="primary", use_container_width=True)

    if generate:
        st.session_state.last_prompt = prompt
        st.session_state.last_context = context
        if add_to_history and prompt.strip():
            st.session_state.session_history.append(
                {"context": context, "user_input": prompt.strip(), "created_at": current_utc_iso()}
            )
            # Rebuild after adding the new example.
            history = pd.concat([history, pd.DataFrame([{"context": context, "user_input": prompt.strip()}])], ignore_index=True)
            engine = SuggestionEngine(history)
        suggestions = engine.suggestions(prompt, context, top_k=top_k)
        st.session_state.last_suggestions = ranker.rank(suggestions)

    suggestions = st.session_state.get("last_suggestions", [])
    if suggestions:
        st.markdown("### Suggested continuations")
        for i, item in enumerate(suggestions, start=1):
            with st.container(border=True):
                st.markdown(f"**Suggestion {i}:** {item['text']}")
                st.caption(f"Source: {item['source']} | Why: {item['reason']} | Current score: {ranker.score(item['source']):.2f}")
                st.code(item["text"], language="text")
                feedback_left, feedback_right = st.columns(2)
                with feedback_left:
                    if st.button(f"Accept suggestion {i}", key=f"accept_{i}", use_container_width=True):
                        ranker.update(item["source"], accepted=True)
                        st.success("Feedback saved. This source will rank higher next time.")
                with feedback_right:
                    if st.button(f"Reject suggestion {i}", key=f"reject_{i}", use_container_width=True):
                        ranker.update(item["source"], accepted=False)
                        st.info("Feedback saved. This source will rank lower next time.")
    else:
        st.info("Type a prompt and click Generate suggestions to see the assistant in action.")

with insight_col:
    st.subheader("Behavior insights")
    insights = engine.behavior_insights()
    st.metric("Training examples", insights["num_examples"])
    st.write("Contexts learned")
    st.json(insights["contexts"])
    common_terms = [word for word, _ in insights["common_terms"]]
    st.write("Common terms")
    st.write(", ".join(common_terms) if common_terms else "No common terms yet.")

    st.divider()
    st.subheader("Feedback ranker")
    st.json(st.session_state.get("bandit", {}))

    st.divider()
    st.subheader("Download session")
    profile = {
        "created_at": current_utc_iso(),
        "session_history": st.session_state.get("session_history", []),
        "bandit": st.session_state.get("bandit", {}),
    }
    st.download_button(
        "Download profile JSON",
        data=json.dumps(profile, indent=2),
        file_name="yashvi_prompt_assistant_profile.json",
        mime="application/json",
        use_container_width=True,
    )

    session_df = pd.DataFrame(st.session_state.get("session_history", []))
    csv_buffer = StringIO()
    session_df.to_csv(csv_buffer, index=False)
    st.download_button(
        "Download session CSV",
        data=csv_buffer.getvalue(),
        file_name="session_user_history.csv",
        mime="text/csv",
        use_container_width=True,
        disabled=session_df.empty,
    )

st.divider()
with st.expander("Prototype notes and limitations"):
    st.markdown(
        "This app is a working web prototype based on the uploaded Colab notebook. "
        "It demonstrates the AI product idea with lightweight ML so it can run on Streamlit hosting. "
        "A production typing assistant or iOS keyboard would require native app development, stronger privacy controls, "
        "security review, user consent flows, and substantially larger training/evaluation data."
    )
