
import streamlit as st

from database.database import get_connection
from src.navigation import clear_history, navigate_to


# =====================================================
# LOGIN PAGE
# =====================================================

def show_login(role):

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = ""

    if "current_page" not in st.session_state:
        st.session_state.current_page = "customer_login"

    # =====================================================
    # STOP IF ALREADY LOGGED IN
    # =====================================================

    if st.session_state.logged_in:
        return

    # =====================================================
    # CUSTOM CSS
    # =====================================================

    st.markdown(
        """
        <style>

        /* =====================================================
           HIDE STREAMLIT DEFAULTS
        ===================================================== */

        [data-testid="stSidebar"] {
            display: none;
        }

        [data-testid="collapsedControl"] {
            display: none;
        }

        header {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        #MainMenu {
            visibility: hidden;
        }

        /* =====================================================
           FULL PAGE AIRLINE BACKGROUND
        ===================================================== */

        .stApp {

            background-image:
                linear-gradient(
                    rgba(5,10,25,0.82),
                    rgba(5,10,25,0.88)
                ),

                url("https://images.unsplash.com/photo-1436491865332-7a61a109cc05?q=80&w=1920&auto=format&fit=crop");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        /* =====================================================
           MAIN CONTAINER
        ===================================================== */

        .block-container {

            padding-top: 12rem;

            max-width: 100%;
        }

        /* =====================================================
           INPUT CONTAINER
        ===================================================== */

        div[data-testid="stTextInput"] {

            max-width: 550px;

            margin: auto;
        }

        .st-key-login_btn,
        .st-key-create_account_btn {

            max-width: 550px;

            margin: auto;
        }

        /* =====================================================
           INPUT FIELDS
        ===================================================== */

        div[data-testid="stTextInput"] input {

            height: 52px;

            border-radius: 14px;

            border: 1px solid rgba(255,255,255,0.12);

            background: rgba(15,23,42,0.78);

            color: white;

            padding-left: 14px;

            



        }

        div[data-testid="stTextInput"] input:focus {

            border: 1px solid #38bdf8 !important;

            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        
        }

        div[data-testid="stTextInput"]:first-of-type {
        margin-top: 10px !important;
        }

        /* =====================================================
           LABELS
        ===================================================== */

        label p {

            color: #e2e8f0 !important;

            font-size: 15px !important;

            font-weight: 600 !important;
        }

        /* =====================================================
           BUTTONS
        ===================================================== */

        .st-key-login_btn button,
        .st-key-create_account_btn button {

            width: 100%;

            height: 52px;

            border-radius: 14px;

            border: none;

            font-size: 17px;

            font-weight: 700;

            color: white;

            background: linear-gradient(
                135deg,
                #0ea5e9,
                #2563eb
            );

            transition: 0.3s ease;

            margin-top: 10px;

            box-shadow:none;
        }

        .st-key-login_btn button:hover,
        .st-key-create_account_btn button:hover {

            transform: translateY(-2px);

            box-shadow:none;
        }

        /* =====================================================
           TITLE
        ===================================================== */

        .login-title {

            text-align: center;

            color: white;

            font-size: 52px;

            font-weight: 800;

            margin-bottom: 20px;
        }

        /* =====================================================
           SUBTITLE
        ===================================================== */

        .login-subtitle {

            text-align: center;

            color: #cbd5e1;

            font-size: 25px;

            font-weight: 500;

            margin-top: 15px;

            margin-bottom: 60px;
        }

        /* =====================================================
           FOOTER
        ===================================================== */

        .login-footer {

            text-align: center;

            margin-top: 60px;

            color: #94a3b8;

            font-size: 14px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # LOGIN TITLE
    # =====================================================

    if role == "admin":

        login_title = " Admin Login"

        login_subtitle = (
            "Secure Enterprise Administration & Analytics Portal"
        )

    else:

        login_title = " Customer Login"

        login_subtitle = (
            "Secure Enterprise Customer Intelligence Portal"
        )

    # =====================================================
    # LOGIN HEADING
    # =====================================================


    st.markdown(
        """
        <div style="height:50px;"></div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <h1 class="login-title">{login_title}</h1>
        """,
        unsafe_allow_html=True
    )

    
    st.markdown(
        f"""
        <p class="login-subtitle">
            {login_subtitle}
        </p>

        <div style="height:5px;"></div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # INPUT LABELS
    # =====================================================

    if role == "admin":

        email_label = "Admin Username"

        email_placeholder = "Enter Username"

        password_placeholder = "Enter Password"

    else:

        email_label = "Customer Email"

        email_placeholder = "Enter Email"

        password_placeholder = "Enter Password"


    st.markdown("""
    <style>

    /* Center placeholder */

    div[data-testid="stTextInput"] input::placeholder{

        color:#94A3B8 !important;

        text-align:center !important;

        opacity:1 !important;
    }

    /* Password field placeholder */

    div[data-testid="stTextInput"] input[type="password"]::placeholder{

        text-align:center !important;
    }

    /* User entered text remains left aligned */

    div[data-testid="stTextInput"] input{

        text-align:left !important;
    }

    </style>
    """, unsafe_allow_html=True)
    # =====================================================
    # INPUTS
    # =====================================================

    username = st.text_input(
        email_label,
        placeholder=email_placeholder
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder=password_placeholder
    )

    # =====================================================
    # LOGIN BUTTON
    # =====================================================

    login_clicked = st.button(
        "Login",
        key="login_btn",
        width="stretch"
    )

    # =====================================================
    # REGISTER BUTTON
    # =====================================================

    if role != "admin":

        register_clicked = st.button(
                "Create New Account",
                key="create_account_btn",
                use_container_width=True
            )


        if register_clicked:

            navigate_to("register")

            st.rerun()
    # =====================================================
    # LOGIN LOGIC
    # =====================================================

    if login_clicked:

        username = username.strip()
        password = password.strip()

        # =================================================
        # ADMIN LOGIN
        # =================================================

        if role == "admin":

            if username.lower() == "admin" and password == "123":

                st.session_state.logged_in = True

                st.session_state.username = "admin"

                st.session_state.role = "admin"

                clear_history()
                navigate_to("admin", record_history=False)

                st.query_params["page"] = "admin" 
                st.query_params["logged_in"] = "true" 
                st.query_params["role"] = "admin" 
                st.query_params["username"] = "admin"

                st.success(" Admin Login Successful")

                st.rerun()

            else:

                st.error(" Invalid Admin Credentials")

        # =================================================
        # CUSTOMER LOGIN
        # =================================================

        else:

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT * FROM users
                WHERE email=? AND password=? AND is_verified=1
                """,
                (
                    username,
                    password
                )
            )

            user = cursor.fetchone()

            conn.close()

            if user:

                st.session_state.logged_in = True

                st.session_state.username = username

                st.session_state.role = "customer"

                st.session_state.email = username

                clear_history()
                navigate_to(
                    "customer_dashboard",
                    record_history=False
                )

                st.query_params["page"] = (
                    "customer_dashboard"
                )
                st.query_params["logged_in"] = "true" 
                st.query_params["role"] = "customer" 
                st.query_params["username"] = username

                st.success(
                    " Customer Login Successful"
                )

                st.rerun()

            else:

                st.error(
                    " Invalid Customer Credentials"
                )

  
