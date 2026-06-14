import streamlit as st
import random

from database.database import get_connection
from src.email_service import send_otp_email
from src.navigation import navigate_to


# =====================================================
# REGISTER PAGE
# =====================================================

def show_register():

    left_space, form_col, right_space = st.columns([1, 1.2, 1])

    with form_col:

        st.markdown(
            """
            <h2 style='text-align:center; color:white;'>
                 Customer Registration
            </h2>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        # =====================================================
        # REGISTER FORM
        # =====================================================

        with st.form("registration_form"):

            # =====================================================
            # INPUTS
            # =====================================================

            name = st.text_input(
                "Full Name",
                placeholder="Enter your full name"
            )

            email = st.text_input(
                "Email",
                placeholder="Enter your email"
            )

            phone = st.text_input(
                "Phone Number",
                placeholder="Enter phone number"
            )

            from datetime import date

            dob = st.date_input(
                "DOB",
                value=date(2001, 8, 16),
                min_value=date(1950, 1, 1),
                max_value=date.today()
            )

            address = st.text_area(
                "Address",
                placeholder="Enter your address"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Confirm password"
            )

            st.write("")

            register_clicked = st.form_submit_button(
                " Register",
                use_container_width=True
            )

            if register_clicked:

                # Strip whitespace from all inputs
                name = name.strip() if name else ""
                email = email.strip() if email else ""
                phone = phone.strip() if phone else ""
                address = address.strip() if address else ""
                password = password.strip() if password else ""
                confirm_password = confirm_password.strip() if confirm_password else ""

                # Detailed validation - check each required field
                if not name:
                    st.error("❌ Full Name is required")
                    st.stop()
                
                if not email:
                    st.error("❌ Email is required")
                    st.stop()
                
                if not password:
                    st.error("❌ Password is required - Please enter a password")
                    st.stop()

                if not confirm_password:
                    st.error("❌ Confirm Password is required - Please confirm your password")
                    st.stop()

                # Phone and address validation (optional but warn if empty)
                if not phone:
                    st.warning("⚠️  Phone number is recommended for booking confirmation")
                
                if not address:
                    st.warning("⚠️  Address is recommended for delivery verification")

                # Password Match
                if password != confirm_password:
                    st.error("❌ Passwords do not match")
                    st.stop()

                conn = get_connection()

                cursor = conn.cursor()


                # =====================================================
                # CHECK EXISTING USER
                # =====================================================

                cursor.execute(
                    "SELECT * FROM users WHERE email=?",
                    (email,)
                )

                existing_user = cursor.fetchone()

                if existing_user:

                    st.error(" Email already registered")

                    conn.close()

                    st.stop()

                # =====================================================
                # GENERATE OTP
                # =====================================================

                otp = str(random.randint(100000, 999999))

                # =====================================================
                # SAVE USER
                # =====================================================

                cursor.execute(
                        """
                        INSERT INTO users
                        (name, email, password, otp, phone, dob, address)

                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            name,
                            email,
                            password,
                            otp,
                            phone,
                            str(dob),
                            address
                        )
                    )

                conn.commit()

                conn.close()

                # =====================================================
                # STORE SESSION DATA
                # =====================================================

                st.session_state.pending_email = email

                st.session_state.pending_otp = otp

                # =====================================================
                # SEND OTP EMAIL
                # =====================================================

                send_otp_email(email, otp)

                # =====================================================
                # SUCCESS MESSAGE
                # =====================================================

                # SUCCESS MESSAGE

                st.success(" Registration Successful")

                st.success("OTP sent to your email")

                # Redirect Automatically

                
                navigate_to("verify_otp")


                st.rerun()
