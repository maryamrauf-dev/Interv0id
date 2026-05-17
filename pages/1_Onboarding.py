import streamlit as st
import PyPDF2
from utils.state import init_session_state
from utils.ui import hide_sidebar_and_render_navbar
import streamlit.components.v1 as components

st.set_page_config(page_title="Interv0id", layout="centered", page_icon=None)
hide_sidebar_and_render_navbar()
init_session_state()

# Custom CSS
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Custom form container background overlay logic */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #161b2e;
    border-radius: 12px;
    border: 1px solid #2d3748 !important;
}

/* Make button wide and purple */
button[kind="primary"] {
    background-color: #5c4dff !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    width: 100% !important;
    font-weight: 600 !important;
}
button[kind="primary"]:hover {
    background-color: #7b6efa !important;'
    box-shadow: 0 0 10px #5c4dff !important;
}

</style>
""", unsafe_allow_html=True)
# Main Title Area
col_logo, col_title = st.columns([1, 10])
with col_logo:
    st.markdown("<h2 style='margin:0; padding:0; color:#5c4dff;'>👩🏻‍💻</h2>", unsafe_allow_html=True)
with col_title:
    st.markdown("<h3 style='margin:0; padding:0;'>Interv0id</h3>", unsafe_allow_html=True)
    st.markdown("<p style='margin:0; padding:0; color:#cbd5e1; font-size:14px;'>Interview Preparation Pro</p>", unsafe_allow_html=True)

st.write("---")

def extract_pdf_text(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
    except Exception:
        return ""

if "skills_list" not in st.session_state:
    st.session_state.skills_list = []
    if st.session_state.user_data.get("skills_keywords"):
        st.session_state.skills_list = [s.strip() for s in st.session_state.user_data["skills_keywords"].split(",") if s.strip()]

def add_skill():
    skill = st.session_state.new_skill_input.strip()
    if skill and skill not in st.session_state.skills_list:
        st.session_state.skills_list.append(skill)
    st.session_state.new_skill_input = ""

# Use a visual container
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(" Your Name", placeholder="Enter your name", value=st.session_state.user_data["name"], key="name_in")
    with col2:
        experience_level = st.selectbox(" Experience Level", ["Entry-Level", "Mid-Level", "Senior-Level", "Executive"], index=1, key="exp_in")
        
    col3, col4 = st.columns(2)
    with col3:
        target_role = st.text_input(" Target Role", placeholder="e.g. Senior Frontend Engineer", value=st.session_state.user_data["target_role"], key="role_in")
    with col4:
        target_company = st.text_input(" Target Company (Optional)", placeholder="e.g. Google, Meta", value=st.session_state.user_data["target_company"], key="company_in")
        
    # Skills input
    st.text_input("</> Add a Skill Keyword and Press Enter", key="new_skill_input", on_change=add_skill, placeholder="e.g. React, Python")
    
    # Render skills
    if st.session_state.skills_list:
        st.markdown("**Added Skills:**")
        cols = st.columns(6)
        for idx, skill in enumerate(st.session_state.skills_list):
            with cols[idx % 6]:
                if st.button(f"{skill} ✖", key=f"del_skill_{idx}"):
                    st.session_state.skills_list.remove(skill)
                    st.rerun()

    st.write("---")
    resume_file = st.file_uploader(" Upload Resume (Optional)", type=["pdf", "txt"])

    submit_button = st.button("Start 30-Min Interview >", type="primary", use_container_width=True)

if submit_button:
    if name and target_role and st.session_state.skills_list:
        resume_text = ""
        if resume_file:
            if resume_file.name.endswith(".pdf"):
                resume_text = extract_pdf_text(resume_file)
                if not resume_text.strip():
                    st.warning("Could not extract text from the PDF. It might be a scanned document or image-based. Proceeding without resume context.")
            else:
                resume_text = str(resume_file.read(), "utf-8")
        

        skills_str = ", ".join(st.session_state.skills_list)
        
        st.session_state.user_data = {
            "name": name,
            "experience_level": experience_level,
            "target_role": target_role,
            "target_company": target_company,
            "skills_keywords": skills_str,
            "resume_text": resume_text
        }
        st.session_state.onboarded = True
        st.switch_page("pages/2_Interview.py")
    else:
        st.error("Please fill in Name, Target Role, and at least one Skill Keyword to proceed.")

# JS interop for the "warning on empty enter" and "jump to next field" behaviors
js_code = """
<script>
setTimeout(function() {
    const doc = window.parent.document;
    const inputs = Array.from(doc.querySelectorAll('input[type="text"]'));

    inputs.forEach((input, index) => {
        if (input.dataset.enterBound === 'true') return;
        input.dataset.enterBound = 'true';

        input.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                const isSkillInput = input.getAttribute('aria-label') && input.getAttribute('aria-label').includes('Add a Skill Keyword');
                
                if (this.value.trim() === '') {
                    event.preventDefault();
                    event.stopPropagation();
                    alert('Please add some info here before pressing Enter.\\nThis field is empty.');
                    return;
                }
                
                if (!isSkillInput) {
                    event.preventDefault();
                    event.stopPropagation();
                    this.blur();
                    if (index + 1 < inputs.length) {
                        setTimeout(() => Object.assign(inputs[index + 1], { value: inputs[index + 1].value }).focus(), 50);
                    }
                }
            }
        });
    });
}, 1500);
</script>
"""
components.html(js_code, height=0, width=0)

