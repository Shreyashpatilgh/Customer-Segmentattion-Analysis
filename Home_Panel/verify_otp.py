import streamlit as st

from database.database import get_connection
from src.navigation import navigate_to


# =====================================================
# OTP VERIFICATION PAGE
# =====================================================

def show_verify_otp():

    st.markdown(
        """
        <h2 style='text-align:center; color:white;'>
             Verify OTP
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    otp_input = st.text_input(
        "Enter OTP",
        placeholder="Enter 6-digit OTP"
    )

    verify_clicked = st.button(
        " Verify Account",
        width="stretch"
    )

    # =====================================================
    # VERIFY LOGIC
    # =====================================================

    if verify_clicked:

        email = st.session_state.get("pending_email")

        saved_otp = st.session_state.get("pending_otp")

        if not email or not saved_otp:

            st.error(" Session expired")

            return

        # =====================================================
        # OTP MATCH
        # =====================================================

        if otp_input == saved_otp:

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE users
                SET is_verified=1
                WHERE email=?
                """,
                (st.session_state.pending_email,)
            )

            conn.commit()

            conn.close()

            # =====================================================
            # SUCCESS MESSAGE
            # =====================================================

            st.success(" Account Verified Successfully")

            st.success(" Registration Completed")

            # =====================================================
            # GO TO LOGIN
            # =====================================================

        # Clear Session
            st.session_state.pending_email = ""

            st.session_state.pending_otp = ""

            # Redirect To Login
            st.session_state.logged_in = False

            navigate_to("customer_login")

            st.rerun()

        else:

            st.error(" Invalid OTP")
