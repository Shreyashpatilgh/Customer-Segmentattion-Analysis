
# src/navbar.py

import streamlit as st
from src.config import APP_TITLE
from src.navigation import clear_history, navigate_to


def show_topbar():

    # =====================================================
    # PAGE STATE
    # =====================================================

    # Default URL page
    if "page" not in st.query_params:

        st.query_params["page"] = "home"

    # Session sync
    if "current_page" not in st.session_state:

        st.session_state.current_page = st.query_params.get(
            "page",
            "home"
        )


    # =====================================================
    # ROLE STATE
    # =====================================================

    if "role" not in st.session_state:

        st.session_state.role = ""

    current_page = st.session_state.current_page

    role = st.session_state.role
    

    # =====================================================
    # ROLE DISPLAY
    # =====================================================

    if role != "":

        st.markdown(
            f"""
            <div style="
                color: white;
                font-size: 18px;
                font-weight: 700;
                margin-bottom: 14px;
                padding-left: 2px;
            ">
                CURRENT ROLE: {role.upper()}
            </div>
            """,
            unsafe_allow_html=True
        )

    def logout_user():

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        clear_history()
        navigate_to("home", record_history=False)

        if "email" in st.session_state:
            del st.session_state["email"]

    # =====================================================
    # PUBLIC NAVBAR
    # =====================================================

    if role == "":

        nav_items = [

            ("home", " Home"),
            ("about", " About"),
            ("features_public", " Features"),
            ("admin_login", " Admin Login"),
            ("customer_login", " Customer Login")
        ]

    # =====================================================
    # ADMIN NAVBAR
    # =====================================================

    elif role == "admin":

        nav_items = [

            ("admin", " Dashboard"),
            ("explorer", " Explorer"),
            ("performance", " Performance"),
            ("analyzer", " Analyzer"),
            ("logout", " Logout")
        ]

    # =====================================================
    # CUSTOMER NAVBAR
    # =====================================================

    else:

        nav_items = [

            ("customer_dashboard", " Dashboard"),
            ("profile", " Profile"),
            ("tickets", " My Tickets"),
            ("prediction", " Prediction"),
            ("insights", " Insights"),
            ("download", " Download"),
            ("support", " Support"),
            ("logout", " Logout")
        ]

    # =====================================================
    # CSS
    # =====================================================

    st.markdown(
        """
        <style>

        [data-testid="stSidebar"] {
            display: none !important;
        }

        header {
            visibility: hidden !important;
        }

        .topbar {
            width: 100%;
            background: #1E293B;
            border: 1px solid rgba(255,255,255,0.08);
            padding: 20px 28px;
            border-radius: 24px;
            margin-bottom: 24px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        }

        .logo {
            color: white;
            font-size: 24px;
            font-weight: 700;
        }

        .nav-spacing {
            margin-bottom: 25px;
        }

        [class*="st-key-nav_btn_"] button {
            height: 56px !important;
            border: none !important;
            border-radius: 16px !important;
            color: white !important;
            font-size: 15px !important;
            font-weight: 700 !important;
            box-shadow: none !important;
            transform: none !important;
        }

        [class*="st-key-nav_btn_"] button[kind="primary"] {
            background: #475569 !important;
        }

        [class*="st-key-nav_btn_"] button[kind="secondary"] {
            background: linear-gradient(135deg, #0ea5e9, #2563eb) !important;
        }

        [class*="st-key-nav_btn_"] button:hover {
            color: white !important;
            filter: brightness(1.06);
            transform: none !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # TOPBAR
    # =====================================================

    st.markdown(
        f"""
        <div class="topbar">
            <div class="logo">
                 {APP_TITLE}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # NAVBAR RENDERING
    # =====================================================

    # Create navigation buttons in columns
    nav_cols = st.columns([1] * len(nav_items))
    
    for idx, (page_name, label) in enumerate(nav_items):
        with nav_cols[idx]:
            is_active = st.session_state.current_page == page_name
            
            if page_name == "logout":
                st.button(
                    label,
                    key=f"nav_btn_{page_name}",
                    use_container_width=True,
                    type="primary",
                    on_click=logout_user
                )
            else:
                st.button(
                    label,
                    key=f"nav_btn_{page_name}",
                    use_container_width=True,
                    type="secondary" if is_active else "primary",
                    on_click=navigate_to,
                    args=(page_name,)
                )
    
    st.markdown("<div class='nav-spacing'></div>", unsafe_allow_html=True)
