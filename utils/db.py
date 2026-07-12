import streamlit as st
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def init_db():
    if 'history' not in st.session_state:
        st.session_state.history = []

def add_history(score, target_role):
    try:
        init_db()
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.history.append({
            "date": date_str,
            "score": score,
            "target_role": target_role
        })
    except Exception as e:
        logger.error(f"Error adding history: {e}", exc_info=True)

def get_history():
    try:
        init_db()
        return list(reversed(st.session_state.history))
    except Exception as e:
        logger.error(f"Error fetching history: {e}", exc_info=True)
        return []
