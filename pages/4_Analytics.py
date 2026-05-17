import streamlit as st
import pandas as pd
from utils.state import init_session_state
from utils.ui import hide_sidebar_and_render_navbar
from utils.db import init_db, get_history

st.set_page_config(page_title="Analytics Dashboard", layout="wide", page_icon="📊")
hide_sidebar_and_render_navbar()
init_session_state()
init_db()

st.title("Interview Analytics")

history_data = get_history()

if not history_data:
    st.info("No interview history yet. Complete an interview to see your progress!")
    if st.button("Start Now"):
        st.switch_page("pages/2_Interview.py")
else:
    df = pd.DataFrame(history_data)
    
    st.subheader("Performance over time")
    if 'score' in df.columns:
        st.line_chart(df['score'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("History Table")
            st.dataframe(df, use_container_width=True)
        
        with col2:
            avg_score = df['score'].mean()
            st.metric("Average Score", f"{avg_score:.1f}/10")
            st.write(f"Total Interviews: {len(df)}")
