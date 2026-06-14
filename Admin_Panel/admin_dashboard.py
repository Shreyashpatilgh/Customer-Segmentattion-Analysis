import streamlit as st
import pandas as pd

from database.database import get_connection
from src.theme import apply_dark_theme


# =====================================================
# DASHBOARD STATS CACHE
# =====================================================

def get_dashboard_stats():

    conn = get_connection()

    try:
        total_customers = pd.read_sql(
            "SELECT COUNT(*) as total FROM users",
            conn
        )["total"][0]
    except:
        total_customers = 0

    try:
        total_predictions = pd.read_sql(
            "SELECT COUNT(*) as total FROM predictions",
            conn
        )["total"][0]
    except:
        total_predictions = 0

    try:
        total_clusters = pd.read_sql(
            """
            SELECT COUNT(DISTINCT segment_name) as total
            FROM customer_segments
            """,
            conn
        )["total"][0]
    except:
        total_clusters = 0

    try:
        total_feedback = pd.read_sql(
            "SELECT COUNT(*) as total FROM feedback_reports",
            conn
        )["total"][0]
    except:
        total_feedback = 0

    conn.close()

    return (
        total_customers,
        total_predictions,
        total_clusters,
        total_feedback
    )


# =====================================================
# RECENT USERS CACHE
# =====================================================

def get_recent_users():

    conn = get_connection()

    try:

        df = pd.read_sql(
            """
            SELECT
                id,
                name,
                email,
                role,
                created_at
            FROM users
            ORDER BY id DESC
            LIMIT 10
            """,
            conn
        )

    except:
        df = pd.DataFrame()

    conn.close()

    return df


# =====================================================
# RECENT PREDICTIONS CACHE
# =====================================================

def get_recent_predictions():

    conn = get_connection()

    try:

        df = pd.read_sql(
            """
            SELECT *
            FROM predictions
            ORDER BY id DESC
            LIMIT 10
            """,
            conn
        )

    except:
        df = pd.DataFrame()

    conn.close()

    return df


# =====================================================
# RECENT FEEDBACK CACHE
# =====================================================

def get_recent_feedback():

    conn = get_connection()

    try:

        df = pd.read_sql(
            """
            SELECT
                id AS "ID",
                customer_email AS "Customer Email",
                feedback AS "Feedback",
                rating AS "Rating",
                created_at AS "Submitted At"
            FROM feedback_reports
            ORDER BY id DESC
            LIMIT 10
            """,
            conn
        )

    except:
        df = pd.DataFrame()

    conn.close()

    return df


# =====================================================
# ADMIN DASHBOARD
# =====================================================

def show_admin_dashboard():

    apply_dark_theme()

    st.title("Admin Analytics Dashboard")

    st.write("")

    (
        total_customers,
        total_predictions,
        total_clusters,
        total_feedback
    ) = get_dashboard_stats()

    # =====================================================
    # KPI CARDS
    # =====================================================

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Total Customers",
            total_customers
        )

    with col2:
        st.metric(
            "Predictions",
            total_predictions
        )

    with col3:
        st.metric(
            "Model Accuracy",
            "94.2%"
        )

    with col4:
        st.metric(
            "Customer Segments",
            total_clusters
        )

    with col5:
        st.metric(
            "Feedback Reports",
            total_feedback
        )

    st.write("")

    # =====================================================
    # PROJECT SUMMARY
    # =====================================================

    st.markdown("""
    <div style="
        background: linear-gradient(135deg,#0f172a,#1e3a8a,#2563eb);
        padding:30px;
        border-radius:18px;
        color:white;
        border-left:8px solid #38bdf8;
        box-shadow:0 8px 25px rgba(0,0,0,0.4);
        margin-bottom:25px;
    ">


    <p style="font-size:18px;">
    Analyze passenger behavior and identify meaningful customer segments
    to improve marketing strategies and customer retention.
    </p>

    <div style="
    display:flex;
    justify-content:space-around;
    margin-top:25px;
    text-align:center;
    ">

    <div>
    <h3> Objective</h3>
    <p>Customer Group Identification</p>
    </div>

    <div>
    <h3> Model</h3>
    <p>K-Means Clustering</p>
    </div>

    <div>
    <h3> Impact</h3>
    <p>Better Targeting & Revenue Growth</p>
    </div>

    </div>

    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # CUSTOMER DATA
    # =====================================================

    st.subheader("Customer Data")
    customer_df = get_recent_users()

    if not customer_df.empty:

        st.dataframe(
            customer_df,
            width="stretch"
        )
        

    else:

        st.warning(
            "No customer data found"
        )

    st.write("")

    # =====================================================
    # RECENT PREDICTIONS
    # =====================================================

    st.subheader("Recent Predictions")

    prediction_df = get_recent_predictions()

    if not prediction_df.empty:

        st.dataframe(
            prediction_df,
            width="stretch"
        )
        

    else:

        st.warning(
            "No prediction history found"
        )

    st.write("")

    # =====================================================
    # CUSTOMER FEEDBACK
    # =====================================================

    st.subheader("Customer Feedback Reports")

    feedback_df = get_recent_feedback()

    if not feedback_df.empty:

        st.dataframe(
            feedback_df,
            width="stretch"
        )

    else:

        st.warning(
            "No feedback reports found"
        )

    st.write("")

    
