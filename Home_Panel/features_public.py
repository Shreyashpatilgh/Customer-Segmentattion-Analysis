import streamlit as st


def add_bg():

    st.markdown(
        """
        <style>

        .stApp {

            background-image:
                linear-gradient(
                    rgba(4, 10, 25, 0.82),
                    rgba(4, 10, 25, 0.85)
                ),

                url("https://images.unsplash.com/photo-1436491865332-7a61a109cc05?q=80&w=1920&auto=format&fit=crop");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }

        h1,h2,h3,p {
            color:white;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def feature_card(icon_url, title, description):

    st.image(icon_url, width=90)

    st.markdown(
        f"""
        #### {title}
        """
    )

    st.write(description)


def show_features_public():

    add_bg()

    # ==========================================
    # HERO SECTION
    # ==========================================

    st.title(" Airline Customer Segmentation & Analytics System")

    st.write(
        """
        Discover powerful Machine Learning, Customer Segmentation,
        Predictive Analytics, Dataset Exploration and Business
        Intelligence capabilities designed for the airline industry.
        """
    )

    st.markdown("---")


    # ==========================================
    # MODERN FEATURE SHOWCASE
    # ==========================================

    st.markdown("""
    <h2 style='text-align:center;color:white;'>
    Airline Analytics Platform Modules
    </h2>

    <p style='text-align:center;color:#d1d5db;font-size:18px;'>
    Comprehensive AI-powered customer intelligence ecosystem
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>

    .feature-box{
        background:rgba(255,255,255,0.06);
        border-radius:22px;
        padding:25px;
        margin-bottom:20px;
        border:1px solid rgba(255,255,255,0.12);
        backdrop-filter:blur(10px);
        min-height:330px;
        text-align:center;
    }

    .feature-title{
        color:white;
        font-size:24px;
        font-weight:700;
        margin-top:15px;
        margin-bottom:10px;
    }

    .feature-desc{
        color:#d1d5db;
        font-size:15px;
        line-height:1.7;
    }

    </style>
    """, unsafe_allow_html=True)

    cards = [
        (
            "https://cdn-icons-png.flaticon.com/512/2103/2103633.png",
            "AI Customer Prediction",
            "Predict customer segments using machine learning, behavioral analytics and airline travel patterns."
        ),
        (
            "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            "Cluster Insights",
            "Discover Premium Travelers, Frequent Flyers, Budget Customers and Occasional Travelers."
        ),
        (
            "https://cdn-icons-png.flaticon.com/512/2920/2920277.png",
            "Dataset Explorer",
            "Explore airline customer datasets with filtering, visualization and statistical analysis tools."
        ),
        (
            "https://cdn-icons-png.flaticon.com/512/4149/4149647.png",
            "Analytics & ML Platform",
            "Build, evaluate and monitor machine learning models with advanced airline analytics dashboards."
        ),
        (
            "https://cdn-icons-png.flaticon.com/512/1055/1055687.png",
            "Model Performance",
            "Train K-Means models, evaluate clustering quality, visualize performance metrics and compare results."
        ),
        (
            "https://cdn-icons-png.flaticon.com/512/724/724933.png",
            "Download Results",
            "Export predictions, customer segments, reports and business intelligence outputs instantly."
        ),
        (
            "https://cdn-icons-png.flaticon.com/512/3064/3064197.png",
            "Secure Authentication",
            "Admin login, customer login, OTP verification and role-based access control."
        ),
        (
            "https://cdn-icons-png.flaticon.com/512/3059/3059518.png",
            "Customer Support",
            "Raise support requests, submit feedback, track issues and get instant assistance."
        )
    ]

    for i in range(0, len(cards), 2):

        col1, col2 = st.columns(2)

        with col1:

            icon, title, desc = cards[i]

            st.markdown(f"""
            <div class="feature-box">
            <img src="{icon}" width="140">
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:

            icon, title, desc = cards[i + 1]

            st.markdown(f"""
            <div class="feature-box">
            <img src="{icon}" width="140">
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("---")

    st.subheader(" Platform Highlights")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Dataset Records", "10M+")
    m2.metric("Customer Clusters", "6")
    m3.metric("ML Algorithm", "K-Means")
    m4.metric("Dashboards", "Admin & Customer")

    st.success(
        "Smart Insights • Better Decisions • AI Powered Airline Analytics"
    )