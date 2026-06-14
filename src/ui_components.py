import streamlit as st
from pathlib import Path


def load_css():
    css_path = Path(__file__).resolve().parents[1] / "assets" / "styles.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def hero(title, subtitle, icon="✈️"):
    st.markdown(
        f"""
        <div class='hero'>
            <h1>{icon} {title}</h1>
            <p style='font-size:18px;'>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
 )


def section(title):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)


def card(content):
    st.markdown(f"<div class='card'>{content}</div>", unsafe_allow_html=True)