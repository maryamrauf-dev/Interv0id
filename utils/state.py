import streamlit as st

def init_session_state():
    # Global UI Customizations
    st.markdown("""
    <style>
    /* Sidebar proportional sizing and styling */
    [data-testid="stSidebar"] {
        min-width: 260px !important;
        max-width: 280px !important;
        background: linear-gradient(180deg, #1e293b, #0f172a) !important;
        border-right: 1px solid #334155;
    }
    
    [data-testid="stSidebarNav"] {
        padding-top: 2rem;
    }

    [data-testid="stSidebarNav"] span {
        font-size: 1.05rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* Subtle shadow separating sidebar from the main content */
    [data-testid="stSidebar"] > div:first-child {
        box-shadow: 4px 0 15px rgba(0,0,0,0.25);
    }
    </style>
    """, unsafe_allow_html=True)

    if "onboarded" not in st.session_state:
        st.session_state.onboarded = False
    
    if "user_data" not in st.session_state:
        st.session_state.user_data = {
            "name": "",
            "experience_level": "Mid-Level",
            "target_role": "",
            "target_company": "",
            "skills_keywords": "",
            "resume_text": "",
        }
    
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
    
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0
    
    if "questions" not in st.session_state:
        st.session_state.questions = []
    
    if "answers" not in st.session_state:
        st.session_state.answers = []
    
    if "interview_complete" not in st.session_state:
        st.session_state.interview_complete = False
    
    if "analysis" not in st.session_state:
        st.session_state.analysis = None
    
    if "history" not in st.session_state:
        st.session_state.history = []
