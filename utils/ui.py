import streamlit as st

def hide_sidebar_and_render_navbar():
    st.markdown("""
<style>
    /* Hide the Streamlit footer and main menu (three dots) */
    #MainMenu { display: none !important; }
    footer { display: none !important; }

    /* Adjust padding to remove blank space from hidden header */
    .block-container {
        padding-top: 2rem !important;
        max-width: 1200px !important;
    }

    /* Style the Logo */
    .logo-text {
        font-size: 1.5rem;
        font-weight: 800;
        color: #f8fafc;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 5px;
    }
    .logo-pill {
        background-color: #5c4dff;
        color: white;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 1.2rem;
        font-weight: 900;
    }

    /* Hide the default Streamlit pages navigation in the sidebar */
    [data-testid="stSidebarNav"] { display: none !important; }

    /* Desktop styles: Hide sidebar & header, top navbar fits on screen without scrolling */
    @media (min-width: 769px) {
        header { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
        [data-testid="stSidebar"] { display: none !important; }
        
        /* Ensure the navbar block doesn't add unnecessary scrollbars */
        div[data-testid="stHorizontalBlock"]:has(.logo-text) {
            align-items: center;
        }
        /* Let Streamlit's native column flex sizing handle the widths */
    }

    /* Mobile styles: Show sidebar, hide top navbar */
    @media (max-width: 768px) {
        /* Keep header transparent so hamburger menu is visible but no background block */
        header { 
            background: transparent !important;
        }
        /* This hides the custom top horizontal navbar block */
        div[data-testid="stHorizontalBlock"]:has(.logo-text) {
            display: none !important;
        }
    }

    /* Target Streamlit page links to style them like a navbar */
    div[data-testid="stPageLink-NavLink"] > a {
        text-decoration: none !important;
        color: #cbd5e1 !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        transition: color 0.3s ease;
    }
    
    div[data-testid="stPageLink-NavLink"] > a:hover {
        color: #5c4dff !important;
    }

    /* Give a specific style to the CTA button column */
    .cta-container div[data-testid="stPageLink-NavLink"] > a {
        background-color: rgba(92, 77, 255, 0.15) !important;
        border: 1px solid #5c4dff !important;
        color: #5c4dff !important;
        border-radius: 30px !important;
        padding: 8px 20px !important;
        font-weight: 600 !important;
        display: inline-block;
        transition: all 0.3s ease;
    }
    
    .cta-container div[data-testid="stPageLink-NavLink"] > a:hover {
        background-color: #5c4dff !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(92, 77, 255, 0.4);
    }
</style>
""", unsafe_allow_html=True)

    # Desktop Top Navbar
    with st.container():
        # Layout columns
        logo_col, space1, nav1, nav2, nav3, nav4, nav5, space2 = st.columns([3, 1, 1.2, 1.2, 1.4, 1.2, 1.2, 2])
        
        with logo_col:
            st.markdown('<div class="logo-text"><span class="logo-pill">&lt;/&gt;</span> Interv0id</div>', unsafe_allow_html=True)
            
        with nav1:
            st.page_link("Home.py", label="Home")
        with nav2:
            st.page_link("pages/1_Onboarding.py", label="Start")
        with nav3:
            st.page_link("pages/2_Interview.py", label="Interview Room")
        with nav4:
            st.page_link("pages/4_Analytics.py", label="Analytics")
        with nav5:
            st.page_link("pages/5_Profile.py", label="Profile")

    # Mobile Sidebar Navbar
    with st.sidebar:
        st.markdown('<div class="logo-text" style="margin-bottom: 20px;"><span class="logo-pill">&lt;/&gt;</span> Interv0id</div>', unsafe_allow_html=True)
        st.page_link("Home.py", label="Home", icon="🏠")
        st.page_link("pages/1_Onboarding.py", label="Start", icon="🚀")
        st.page_link("pages/2_Interview.py", label="Interview Room", icon="🎙️")
        st.page_link("pages/4_Analytics.py", label="Analytics", icon="📊")
        st.page_link("pages/5_Profile.py", label="Profile", icon="👤")
