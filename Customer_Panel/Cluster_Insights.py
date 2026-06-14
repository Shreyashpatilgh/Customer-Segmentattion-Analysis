import streamlit as st
from src.utils import page_header
from src.theme import apply_dark_theme

def show_cluster_insights():
    apply_dark_theme()

    page_header(
        " Cluster Insights",
        "Business interpretation of each customer segment."
    )

    # --------------------------------------------------
    # Cluster Definitions
    # --------------------------------------------------
    cluster_insights = {
        0: {
            "name": " High-Value Premium Flyers",
            "description": """
            Customers with very high spend, frequent travel, and strong loyalty engagement.
            """,
            "actions": [
                "Offer premium memberships",
                "Provide concierge services",
                "Target with luxury upgrades",
            ],
        },
        1: {
            "name": " Frequent Economy Travelers",
            "description": """
            Travel often but have moderate spending behavior.
            """,
            "actions": [
                "Upsell business class",
                "Offer loyalty bonuses",
                "Promote annual travel plans",
            ],
        },
        2: {
            "name": " New Customers",
            "description": """
            Recently acquired customers with limited travel history.
            """,
            "actions": [
                "Send onboarding campaigns",
                "Provide welcome offers",
                "Encourage first loyalty redemption",
            ],
        },
        3: {
            "name": " Churn-Risk Customers",
            "description": """
            Customers with long inactivity and declining engagement.
            """,
            "actions": [
                "Send win-back campaigns",
                "Offer targeted discounts",
                "Conduct satisfaction surveys",
            ],
        },
        4: {
            "name": " Price-Sensitive Travelers",
            "description": """
            Low spend and highly responsive to promotions.
            """,
            "actions": [
                "Promote discounted fares",
                "Bundle value offers",
                "Use flash sales",
            ],
        },
    }

    # --------------------------------------------------
    # Render Insights
    # --------------------------------------------------
    for cluster_id, info in cluster_insights.items():
        with st.expander(f"Cluster {cluster_id}: {info['name']}", expanded=False):
            st.markdown("### Description")
            st.write(info["description"])

            st.markdown("### Recommended Business Actions")
            for action in info["actions"]:
                st.write(f"- {action}")

    st.success(
        "These insights help translate technical clusters into actionable business strategies."
    )