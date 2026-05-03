import streamlit as st
from utils.state import init_session_state
from utils.ui import hide_sidebar_and_render_navbar

st.set_page_config(
    page_title="Interv0id",
    layout="centered"
)

# Render Global Navbar
hide_sidebar_and_render_navbar()

# Initialize Session State
init_session_state()

# Custom Styling for Home Page
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Enhanced Heading with Glow and Moving Gradient */
.main-title {
    font-size: 4rem;
    font-weight: 900;
    text-align: center;
    margin-bottom: 0px;
    background: linear-gradient(90deg, #5c4dff 0%, #a291ff 40%, #ffffff 50%, #a291ff 60%, #5c4dff 100%);
    background-size: 200% auto;
    color: transparent;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 25px rgba(92, 77, 255, 0.4);
    padding-bottom: 10px;
    animation: shine 3s linear infinite;
}

@keyframes shine {
    to {
        background-position: 200% center;
    }
}
.sub-title {
    font-size: 1.4rem;
    text-align: center;
    color: #a0aec0;
    margin-top: -10px;
    margin-bottom: 40px;
    font-weight: 500;
}

/* Glowing Purple Push Button */
button[kind="primary"] {
    background-color: #5c4dff !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    padding: 0px !important;
    box-shadow: 0 4px 20px rgba(92, 77, 255, 0.4) !important;
    transition: all 0.3s ease !important;
}
button[kind="primary"]:hover {
    background-color: #7b6efa !important;
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 8px 25px rgba(92, 77, 255, 0.6) !important;
}

/* Premium Gradient Box Cards */
.feature-card {
    background: linear-gradient(145deg, #1e2538, #141926);
    border-radius: 20px;
    padding: 30px 20px;
    text-align: center;
    border: 1px solid #2d3748;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    min-height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-bottom: 20px;
}
.feature-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 6px;
}
/* Different glowing top borders for each card */
.card-1::before { background: linear-gradient(90deg, #ff8a00, #e52e71); }
.card-2::before { background: linear-gradient(90deg, #2193b0, #6dd5ed); }
.card-3::before { background: linear-gradient(90deg, #8E2DE2, #4A00E0); }

.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.4);
    border-color: #4a5568;
}
.feature-card h3 {
    margin: 0 0 10px 0;
    color: #ffffff;
    font-size: 1.6rem;
    font-weight: 700;
}
.feature-card p {
    color: #cbd5e1;
    font-size: 1rem;
    margin: 0;
    line-height: 1.4;
}
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<div class="main-title">Interv0id</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Your ultimate AI-powered journey to mastering interviews</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        if st.button("Start Your Journey", type="primary", use_container_width=True):
            if st.session_state.onboarded:
                st.switch_page("pages/2_Interview.py")
            else:
                st.switch_page("pages/1_Onboarding.py")

    st.write("")
    st.write("")
    st.write("")

    feat_col1, feat_col2, feat_col3 = st.columns(3)
    
    with feat_col1:
        st.markdown("""
        <div class="feature-card card-1">
            <h3>Behavioral</h3>
            <p>Master culture-fit questions tailored to your unique background.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with feat_col2:
        st.markdown("""
        <div class="feature-card card-2">
            <h3>Technical</h3>
            <p>Conquer domain-specific concepts targeted at your exact skills.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with feat_col3:
        st.markdown("""
        <div class="feature-card card-3">
            <h3>Coding Lab</h3>
            <p>A real-time IDE environment to test your logic natively in Python.</p>
        </div>
        """, unsafe_allow_html=True)

    # --- NEW SECTIONS FOR SCROLLING WEB LAYOUT ---
    
    st.markdown("""
    <style>
    .section-title {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin-top: 100px;
        margin-bottom: 10px;
        color: #f8fafc;
    }
    .section-subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #a0aec0;
        margin-bottom: 50px;
    }
    .steps-container {
        display: flex;
        flex-direction: column;
        gap: 20px;
        margin-top: 30px;
    }
    .step-card {
        background-color: #1e2538;
        border-radius: 15px;
        padding: 30px;
        border: 1px solid #2d3748;
        display: flex;
        align-items: center;
        gap: 25px;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .step-card:hover {
        transform: translateX(10px);
        border-color: #5c4dff;
    }
    .step-number {
        background: linear-gradient(135deg, #5c4dff, #a291ff);
        color: white;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.8rem;
        font-weight: bold;
        flex-shrink: 0;
        box-shadow: 0 4px 15px rgba(92, 77, 255, 0.4);
    }
    .step-content h4 {
        margin: 0 0 8px 0;
        color: #ffffff;
        font-size: 1.4rem;
        font-weight: 700;
    }
    .step-content p {
        margin: 0;
        color: #cbd5e1;
        font-size: 1.05rem;
        line-height: 1.5;
    }

    .stats-container {
        background: linear-gradient(135deg, #1e2538, #141926);
        border-radius: 20px;
        padding: 50px 30px;
        margin-top: 100px;
        border: 1px solid #2d3748;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .stat-item h2 {
        font-size: 3.5rem;
        color: #a291ff;
        margin: 0;
        font-weight: 900;
    }
    .stat-item p {
        color: #cbd5e1;
        font-size: 1.2rem;
        margin: 5px 0 0 0;
        font-weight: 500;
    }

    .bottom-cta {
        text-align: center;
        margin-top: 100px;
        margin-bottom: 40px;
        padding: 80px 20px;
        background: radial-gradient(ellipse at center, #1e2538 0%, #0f172a 80%);
        border-radius: 20px;
        border: 1px solid #2d3748;
    }

    /* Custom Footer */
    .custom-footer {
        text-align: center;
        padding: 40px 20px 20px 20px;
        border-top: 1px solid #1e293b;
        color: #64748b;
        font-size: 0.95rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">How It Works</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Three simple steps to interview mastery</div>', unsafe_allow_html=True)
    
    col_steps1, col_steps2, col_steps3 = st.columns([1, 4, 1])
    with col_steps2:
        st.markdown("""
        <div class="steps-container">
            <div class="step-card">
                <div class="step-number">1</div>
                <div class="step-content">
                    <h4>Build Your Profile</h4>
                    <p>Upload your resume, set your target role, and define your experience level to get started.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <div class="step-content">
                    <h4>Take the AI Interview</h4>
                    <p>Engage in a dynamic, real-time interactive interview tailored precisely to your background.</p>
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <div class="step-content">
                    <h4>Analyze & Improve</h4>
                    <p>Get instant deep-dive feedback on your answers with actionable areas for continuous improvement.</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="stats-container">
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 30px;">
            <div class="stat-item">
                <h2>10x</h2>
                <p>Faster Prep Time</p>
            </div>
            <div class="stat-item">
                <h2>100%</h2>
                <p>Personalized</p>
            </div>
            <div class="stat-item">
                <h2>24/7</h2>
                <p>Availability</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="text-align: center; margin-top: 120px; margin-bottom: 30px;">', unsafe_allow_html=True)
    
    
    st.markdown("""
    <div class="custom-footer">
        <p>© 2026 Interv0id Interview Prep. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
