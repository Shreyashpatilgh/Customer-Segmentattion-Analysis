import streamlit as st

def apply_dark_theme():

    st.markdown("""
    <style>

    .stApp{
        background:#0F172A;
    }

    h1,h2,h3,p,label{
        color:white !important;
    }

    /* Dashboard Title */
    .main-title{
        font-size:48px !important;
        font-weight:800 !important;
        color:white !important;
        text-align:center;
        margin-bottom:20px;
    }

    /* Metric Cards */
    div[data-testid="stMetric"]{
        background:#1E293B;
        border-radius:16px;
        padding:20px;
    }

    /* Metric Label */
    [data-testid="stMetricLabel"]{
        color:white !important;
        font-size:18px !important;
        font-weight:600 !important;
    }

    /* Metric Value */
    [data-testid="stMetricValue"]{
        color:white !important;
        font-size:32px !important;
        font-weight:700 !important;
    }

    /* Force all metric text white */
    div[data-testid="stMetric"] *{
        color:white !important;
    }

    div[data-testid="stDataFrame"]{
        border-radius:16px;
        overflow:hidden;
    }

    div[data-testid="stAlert"]{
        border-radius:12px;
    }

    </style>
    """, unsafe_allow_html=True)