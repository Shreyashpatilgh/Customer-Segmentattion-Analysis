import streamlit as st


def init_navigation():
    if "page_history" not in st.session_state:
        st.session_state.page_history = []


def navigate_to(page: str, record_history: bool = True):
    init_navigation()

    current_page = st.session_state.get("current_page", "home")

    if record_history and current_page != page:
        history = st.session_state.page_history

        if not history or history[-1] != current_page:
            history.append(current_page)

    st.session_state.current_page = page
    st.query_params["page"] = page


def clear_history():
    st.session_state.page_history = []


def go_back():
    init_navigation()

    current_page = st.session_state.get("current_page", "home")
    history = st.session_state.page_history

    while history:
        previous_page = history.pop()

        if previous_page != current_page:
            st.session_state.current_page = previous_page
            st.query_params["page"] = previous_page
            break


def show_back_arrow():
    init_navigation()

    st.markdown(
        """
        <style>
        .st-key-app_back_arrow button {
            width: 52px !important;
            min-width: 52px !important;
            height: 44px !important;
            padding: 0 !important;
            border-radius: 50% !important;
            font-size: 22px !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #0ea5e9, #2563eb) !important;
            color: white !important;
            box-shadow: none !important;
        }

        .st-key-app_back_arrow button:disabled {
            opacity: 0.35 !important;
            cursor: not-allowed !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col_back, _ = st.columns([0.6, 9.4])

    with col_back:
        clicked = st.button(
            "←",
            key="app_back_arrow",
            help="Go to previous page",
            disabled=len(st.session_state.page_history) == 0
        )

    if clicked:
        go_back()
        st.rerun()
