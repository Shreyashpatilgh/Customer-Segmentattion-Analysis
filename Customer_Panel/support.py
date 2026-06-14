import streamlit as st
from src.utils import page_header
from src.theme import apply_dark_theme

def show_support():
    apply_dark_theme()

    # ==========================================
    # PAGE HEADER
    # ==========================================
    page_header(
        " Customer Support Center",
        "Need help with predictions, downloads, account access, or technical issues?"
    )


    # ==========================================
    # SUPPORT OVERVIEW
    # ==========================================
    st.markdown("""
    <div class="support-card">
        <h3> How Can We Help?</h3>
        <p>
        Our support team is available to assist with customer segmentation
        predictions, dashboard issues, report downloads, and account-related
        queries.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # SUPPORT REQUEST FORM
    # ==========================================
    st.subheader(" Submit Support Request")

    with st.form("support_form"):

        issue_type = st.selectbox(
            "Issue Category",
            [
                "Prediction Issue",
                "Account Access",
                "Download Problem",
                "Technical Support",
                "General Inquiry"
            ]
        )

        subject = st.text_input(
            "Subject"
        )

        description = st.text_area(
            "Describe Your Issue",
            height=150
        )

        submit = st.form_submit_button(
            "Submit Request",
            use_container_width=True
        )

        if submit:

            if not subject.strip():
                st.error("Please enter a subject.")
            elif not description.strip():
                st.error("Please describe your issue.")
            else:
                st.success(
                    " Your support request has been submitted successfully."
                )

    st.markdown("---")

    # ==========================================
    # CONTACT INFORMATION
    # ==========================================
    st.subheader(" Contact Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("""
        **Email Support**

        support@airlineanalytics.com
        """)

    with col2:
        st.info("""
        **Phone Support**

        +91 1800-123-4567
        """)

    with col3:
        st.info("""
        **Working Hours**

        Monday - Friday

        9:00 AM - 6:00 PM
        """)

    st.markdown("---")

    # ==========================================
    # SYSTEM STATUS
    # ==========================================
    st.subheader(" System Status")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success("""
        **Prediction Engine**

        Operational
        """)

    with col2:
        st.success("""
        **Customer Dashboard**

        Operational
        """)

    with col3:
        st.success("""
        **Download Services**

        Operational
        """)

    st.markdown("---")

    # ==========================================
    # FAQ
    # ==========================================
    st.subheader(" Frequently Asked Questions")

    with st.expander(
        "How do I predict a customer segment?"
    ):
        st.write(
            "Navigate to the Prediction page, enter customer information and click Predict Customer Segment."
        )

    with st.expander(
        "Why is my prediction taking time?"
    ):
        st.write(
            "Large datasets and model processing may take additional time depending on system resources."
        )

    with st.expander(
        "How can I download prediction results?"
    ):
        st.write(
            "Visit the Download page and export your generated reports."
        )

    with st.expander(
        "Who can access the dashboard?"
    ):
        st.write(
            "Registered users with valid credentials can access the customer dashboard."
        )

    # ==========================================
    # FOOTER
    # ==========================================
    st.markdown("---")

    st.caption(
        " Airlines Customer Segmentation System | Customer Support Portal"
    )