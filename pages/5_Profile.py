import streamlit as st
from utils.state import init_session_state
from utils.ui import hide_sidebar_and_render_navbar

st.set_page_config(page_title="My Profile", layout="wide", page_icon="👤")
hide_sidebar_and_render_navbar()
init_session_state()

st.title("My Profile")
st.write("View or update your current preferences.")

st.subheader("Personal Information")
name = st.text_input("Name", value=st.session_state.user_data.get("name", ""))
experience_level = st.selectbox("Experience Level", ["Entry-Level", "Mid-Level", "Senior-Level", "Executive"], index=["Entry-Level", "Mid-Level", "Senior-Level", "Executive"].index(st.session_state.user_data.get("experience_level", "Mid-Level")))
target_role = st.text_input("Target Role", value=st.session_state.user_data.get("target_role", ""))
target_company = st.text_input("Target Company", value=st.session_state.user_data.get("target_company", ""))
skills_keywords = st.text_input("Skills Keywords", value=st.session_state.user_data.get("skills_keywords", ""))

if st.button("Update Profile"):
    st.session_state.user_data.update({
        "name": name,
        "experience_level": experience_level,
        "target_role": target_role,
        "target_company": target_company,
        "skills_keywords": skills_keywords
    })
    st.success("Profile updated successfully!")
