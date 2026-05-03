import streamlit as st

def hide_sidebar_and_render_navbar():
    st.markdown("""
<style>
    /* Hide the Streamlit sidebar, header, and footer */
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    #MainMenu { display: none !important; }
    header { display: none !important; }
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

    /* Make the navigation horizontally scrollable on mobile */
    @media (max-width: 768px) {
        div[data-testid="stHorizontalBlock"]:has(.logo-text) {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            padding-bottom: 5px;
            /* Hide scrollbar for a cleaner look */
            -ms-overflow-style: none;  /* IE and Edge */
            scrollbar-width: none;  /* Firefox */
        }
        div[data-testid="stHorizontalBlock"]:has(.logo-text)::-webkit-scrollbar {
            display: none;
        }
        div[data-testid="stHorizontalBlock"]:has(.logo-text) > div {
            min-width: max-content !important;
            flex: 0 0 auto !important;
            width: max-content !important;
        }
    }
</style>
""", unsafe_allow_html=True)

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
