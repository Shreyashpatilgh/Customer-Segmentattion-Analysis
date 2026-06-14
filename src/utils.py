from pathlib import Path
import streamlit as st


def load_css():

    # Project root folder
    current_dir = Path(__file__).parent.parent

    # CSS file path
    css_file = current_dir / "assets" / "styles.css"

    # Load CSS
    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    else:
        st.error(f"CSS file not found: {css_file}")


def page_header(title: str, subtitle: str):
    """
    Render a professional hero header.
    """
    st.markdown(
        f"""
        <div class="hero-card">
            <h1 style="margin-bottom:0.5rem;">{title}</h1>
            <p style="color:#64748B; font-size:1.05rem;">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def metric_card(label: str, value: str):
    """
    Render a custom metric card.
    """
    st.markdown(
        f"""
        <div class="metric-card">
            <h4 style="margin-bottom:0.3rem; color:#64748B;">
                {label}
            </h4>
            <h2 style="margin:0;">{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )