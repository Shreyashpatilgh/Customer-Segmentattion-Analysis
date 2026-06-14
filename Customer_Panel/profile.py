from database.database import get_connection
import pandas as pd
import streamlit as st
from src.theme import apply_dark_theme


# =====================================================
# EDIT PROFILE POPUP
# =====================================================

@st.dialog("Edit Profile")
def edit_profile_dialog(user, email):
    conn = get_connection()

    st.markdown("""
    <style>

    /* Dialog Backdrop Blur */
    [data-testid="stDialogBackdrop"] {
        backdrop-filter: blur(8px) !important;
        background: rgba(0, 0, 0, 0.6) !important;
    }

    /* Dialog Container */
    [data-testid="stDialog"] {
        display: flex;
        align-items: center;
        justify-content: center;
        position: fixed;
        inset: 0;
        z-index: 9999;
    }

    /* Dialog Content */
    [data-testid="stDialog"] > div {
        max-width: 700px !important;
        width: 90% !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5) !important;
        padding: 40px !important;
    }

    /* Dialog Close Button */
    [data-testid="stDialog"] button[aria-label="Close"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border: none !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        padding: 8px 12px !important;
    }

    [data-testid="stDialog"] button[aria-label="Close"]:hover {
        background: rgba(255, 255, 255, 0.2) !important;
    }

    /* Form Labels */
    [data-testid="stDialog"] label p {
        color: #dbeafe !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }

    /* Form Inputs */
    [data-testid="stDialog"] input,
    [data-testid="stDialog"] textarea,
    [data-testid="stDialog"] [data-testid="stDateInput"] input {
        background: #0f172a !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
    }

    [data-testid="stDialog"] input:focus,
    [data-testid="stDialog"] textarea:focus {
        border: 1px solid #06b6d4 !important;
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1) !important;
    }

    /* Textarea */
    [data-testid="stDialog"] textarea {
        min-height: 120px !important;
    }

    /* Form Buttons */
    [data-testid="stDialog"] button[type="submit"] {
        padding: 12px 24px !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        cursor: pointer !important;
        font-size: 15px !important;
        transition: all 0.2s ease !important;
    }

    /* Save Button */
    [data-testid="stDialog"] button[type="submit"]:first-of-type {
        background: linear-gradient(135deg, #06b6d4, #2563eb) !important;
        color: #ffffff !important;
    }

    [data-testid="stDialog"] button[type="submit"]:first-of-type:hover {
        box-shadow: 0 8px 24px rgba(6, 182, 212, 0.4) !important;
        transform: translateY(-2px) !important;
    }

    /* Cancel Button */
    [data-testid="stDialog"] button[type="submit"]:last-of-type {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #dbeafe !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    [data-testid="stDialog"] button[type="submit"]:last-of-type:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }

    </style>
    """, unsafe_allow_html=True)

    with st.form("update_profile_form"):

        name = st.text_input(
            "Full Name",
            value=user.get("name") or ""
        )

        new_email = st.text_input(
            "Email Address",
            value=user.get("email") or ""
        )

        phone = st.text_input(
            "Phone Number",
            value=user.get("phone") or ""
        )

        dob = st.date_input(
        "Date of Birth",
        value=pd.to_datetime(
            user.get("dob")
        ).date() if user.get("dob") else None
    )

        address = st.text_area(
            "Address",
            value=user.get("address") or "",
            height=120
        )

        st.write("")

        st.markdown("<br>", unsafe_allow_html=True)

        update_btn = st.form_submit_button(
            "Save Changes",
            use_container_width=True
        )

        cancel_btn = st.form_submit_button(
            "Cancel",
            use_container_width=True
        )

        if update_btn:

            cursor = conn.cursor()

            update_query = f"""
            UPDATE users
            SET
                name='{name}',
                email='{new_email}',
                phone='{phone}',
                dob='{dob}',
                address='{address}'
            WHERE email='{email}'
            """

            cursor.execute(update_query)
            conn.commit()
            cursor.close()

            st.session_state.username = new_email

            st.success(
                "Profile Updated Successfully"
            )

            st.rerun()

        if cancel_btn:
            st.rerun()


# =====================================================
# CUSTOMER PROFILE
# =====================================================

def show_profile():

    apply_dark_theme()

    conn = get_connection()

    email = st.session_state.username

    query = f"""
    SELECT
        name,
        email,
        phone,
        dob,
        address,
        created_at
    FROM users
    WHERE email='{email}'
    """

    df = pd.read_sql(
        query,
        conn
    )

    # =====================================================
    # PROFILE DETAILS
    # =====================================================

    if not df.empty:

        user = df.iloc[0]

        st.markdown(
            f"""
            <div style="
                max-width:850px;
                margin:auto;
                background:#1E293B;
                padding:5px 40px;
                border-radius:20px;
                color:white;
                box-shadow:0 4px 20px rgba(0,0,0,0.25);
            ">

            <h1 style="
                text-align:center;
                margin-bottom:10px;
                font-size:40px;
                color:white;
            ">
                My Profile
            </h1>

            <p style="
                text-align:center;
                font-size:20px;
                color:#CBD5E1;
                margin-bottom:35px;
            ">
                Welcome to your Airlines Travel Dashboard
                <br>
                Manage your travel profile, booking details,
                and customer information professionally.
            </p>

            <hr style="border:1px solid #334155;">

            <p style="font-size:22px; margin-top:20px;">
                <b>Name:</b> {user.get('name') or 'Not Updated'}
            </p>

            <p style="font-size:22px;">
                <b>Email:</b> {user.get('email') or 'Not Updated'}
            </p>

            <p style="font-size:22px;">
                <b>Phone:</b> {user.get('phone') or 'Not Updated'}
            </p>

            <p style="font-size:22px;">
                <b>Date of Birth:</b> {user.get('dob') or 'Not Updated'}
            </p>

            <p style="font-size:22px;">
                <b>Address:</b> {user.get('address') or 'Not Updated'}
            </p>

            <p style="font-size:22px;">
                <b>Account Created:</b> {user.get('created_at')}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")
        st.write("")

        # =====================================================
        # EDIT PROFILE BUTTON
        # =====================================================

        col1, col2, col3 = st.columns([2, 2, 2])

        with col2:

            if st.button(
                " Edit Profile",
                use_container_width=True
            ):
                edit_profile_dialog(
                    user,
                    email
                )

    else:

        st.warning(
            "Profile not found"
        )   

    conn.close()