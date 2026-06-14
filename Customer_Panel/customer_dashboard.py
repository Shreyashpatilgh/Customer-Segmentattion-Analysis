
import streamlit as st
import matplotlib.pyplot as plt
from src.theme import apply_dark_theme

# =====================================================
# CUSTOMER DASHBOARD
# =====================================================

def show_customer_dashboard():
    apply_dark_theme()

    st.markdown(
        """
        <style>
        html, body, .stApp, [data-testid="stAppViewContainer"] {
            overflow-y: auto !important;
            min-height: auto !important;
            max-height: none !important;
        }

        .block-container {
            overflow: visible !important;
            max-height: none !important;
            padding-bottom: 2rem !important;
        }

        .stApp {
            min-height: auto !important;
        }

        [data-testid="stVerticalBlock"] {
            overflow: visible !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # TITLE
    # =====================================================

    st.markdown(
    """
    <div class="main-title">
         Airlines Analytics Dashboard
    </div>

    
    <div style="height:40px;"></div>
    """,
    unsafe_allow_html=True
)
    # =====================================================
    # METRICS
    # =====================================================

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric("Customers", "12,540")

    with metric2:
        st.metric("Bookings", "8,920")

    with metric3:
        st.metric("Routes", "124")

    with metric4:
        st.metric("Satisfaction", "94%")

    st.write("")
    st.write("")

    # =====================================================
    # COMMON CHART SETTINGS
    # =====================================================

    chart_width = 5.2
    chart_height = 3.2

    # =====================================================
    # CHART ROW 1
    # =====================================================

    col1, col2 = st.columns(
        2,
        gap="large"
    )

    # -----------------------------------------------------
    # BOOKING STATUS - LINE CHART
    # -----------------------------------------------------

    with col1:

        st.subheader(" Booking Status")

        status = [
            "Confirmed",
            "Cancelled",
            "Pending"
        ]

        bookings = [
            72,
            18,
            10
        ]

        fig1, ax1 = plt.subplots(
            figsize=(chart_width, chart_height)
        )

        ax1.plot(
            status,
            bookings,
            marker='o',
            linewidth=3,
            color="#00C897"
        )

        ax1.fill_between(
            status,
            bookings,
            color="#00C897",
            alpha=0.20
        )

        ax1.set_xlabel(
            "Booking Status",
            fontsize=9
        )

        ax1.set_ylabel(
            "Booking Percentage",
            fontsize=9
        )

        ax1.tick_params(
            axis='x',
            labelsize=8
        )

        ax1.tick_params(
            axis='y',
            labelsize=8
        )

        ax1.grid(
            alpha=0.3
        )

        plt.tight_layout(
            pad=2
        )

        st.pyplot(fig1)

    # -----------------------------------------------------
    # MONTHLY BOOKINGS
    # -----------------------------------------------------

    with col2:

        st.subheader(" Monthly Bookings")

        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun"
        ]

        monthly_bookings = [
            1200,
            1500,
            1800,
            2100,
            2500,
            3000
        ]

        fig2, ax2 = plt.subplots(
            figsize=(chart_width, chart_height)
        )

        ax2.bar(
            months,
            monthly_bookings,
            color=[
                "#38BDF8",
                "#0EA5E9",
                "#0284C7",
                "#0369A1",
                "#075985",
                "#0C4A6E"
            ],
            width=0.55
        )

        ax2.set_xlabel(
            "Months",
            fontsize=9
        )

        ax2.set_ylabel(
            "Total Bookings",
            fontsize=9
        )

        ax2.set_title(
            "Travel Growth",
            fontsize=11
        )

        ax2.tick_params(
            axis='x',
            labelsize=8
        )

        ax2.tick_params(
            axis='y',
            labelsize=8
        )

        ax2.grid(
            axis='y',
            alpha=0.3
        )

        plt.tight_layout(
            pad=2
        )

        st.pyplot(fig2)

    

    # =====================================================
    # AI INSIGHTS
    # =====================================================

    col1, col2 = st.columns(
        2,
        gap="large"
    )

    insights = [

        " High demand detected for Dubai routes",

        " Best booking period: Next 2 weeks",

        " Peak season expected in July",

        " Premium users eligible for discounts"
    ]

    colors = [
        "success",
        "info",
        "warning"
    ]


    with col1:
        st.subheader(" AI Smart Recommendations")

        for i, insight in enumerate(insights):

            color = colors[i % len(colors)]

            st.success(insight) if color == "success" else st.info(insight) if color == "info" else st.warning(insight)

    # =====================================================
    # QUICK INSIGHTS
    # =====================================================

    with col2:

        st.subheader(" Quick Insights")

        insights = [

            " 25% increase in summer bookings",

            " Dubai is the top destination",

            " Weekend bookings highest on Fridays",

            " Online payments increased by 40%",

            " Customer satisfaction improved"
        ]

        for i, insight in enumerate(insights):

            color = colors[i % len(colors)]

            st.success(insight) if color == "success" else st.info(insight) if color == "info" else st.warning(insight)

        
