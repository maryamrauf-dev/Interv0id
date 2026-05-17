import streamlit as st
from utils.state import init_session_state
from utils.ui import hide_sidebar_and_render_navbar
from utils.llm_engine import get_engine
from utils.db import init_db, add_history

st.set_page_config(page_title="Interview Feedback", layout="wide", page_icon="📈")
hide_sidebar_and_render_navbar()
init_session_state()
init_db()

st.title("Interview Feedback & Insights")

if not st.session_state.answers or len(st.session_state.answers) < len(st.session_state.questions):
    st.warning("Please complete an interview first.")
    if st.button("Start Interview"):
        st.switch_page("pages/2_Interview.py")
    st.stop()

if not st.session_state.analysis:
    if st.session_state.get("analysis_loading", False):
        st.info("Analysis in progress. Please wait...")
        st.stop()
        
    st.session_state.analysis_loading = True
    with st.spinner("Analyzing your performance..."):
        analysis = get_engine().evaluate_interview(
            st.session_state.user_data,
            st.session_state.questions,
            st.session_state.answers
        )
        st.session_state.analysis = analysis
        # Save to history for dashboard
        add_history(
            score=analysis.get("score", 0),
            target_role=st.session_state.user_data["target_role"]
        )
    st.session_state.analysis_loading = False

analysis = st.session_state.analysis

col1, col2 = st.columns([1, 2])

with col1:
    st.metric("Overall Score", f"{analysis.get('score', 0)}/10")
    
    st.subheader("Strengths")
    for s in analysis.get("strengths", []):
        st.success(s)

with col2:
    st.subheader("Areas of Improvement")
    for a in analysis.get("areas_of_improvement", []):
        st.warning(a)
    
    st.subheader("Detailed Category Feedback")
    if "category_feedback" in analysis:
        for cat, feedback in analysis["category_feedback"].items():
            with st.expander(f"View {cat.capitalize()} Feedback"):
                st.write(feedback)
    else:
        st.write(analysis.get("review", "Deep review not available."))

st.write("---")
if st.button("Retake Interview"):
    st.session_state.interview_started = False
    st.session_state.current_question_index = 0
    st.session_state.answers = []
    st.session_state.analysis = None
    st.session_state.analysis_loading = False
    st.switch_page("pages/2_Interview.py")
