import streamlit as st

def show_loader():

    st.markdown("""
    <style>

    .loader-container {
        display:flex;
        justify-content:center;
        align-items:center;
        padding:50px;
    }

    .loader {
        width:70px;
        height:70px;
        border:8px solid rgba(255,255,255,0.2);
        border-top:8px solid #38bdf8;
        border-radius:50%;
        animation:spin 1s linear infinite;
    }

    @keyframes spin {
        0% {transform:rotate(0deg);}
        100% {transform:rotate(360deg);}
    }

    </style>

    <div class="loader-container">
        <div class="loader"></div>
    </div>
    """, unsafe_allow_html=True)


def show_fullscreen_loader():

    st.markdown("""
    <style>

    .loader-overlay {
        position:fixed;
        top:0;
        left:0;
        width:100vw;
        height:100vh;
        background:rgba(15,23,42,0.95);
        z-index:999999;
        display:flex;
        justify-content:center;
        align-items:center;
    }

    .loader {
        width:90px;
        height:90px;
        border:8px solid rgba(255,255,255,0.2);
        border-top:8px solid #38bdf8;
        border-radius:50%;
        animation:spin 1s linear infinite;
    }

    @keyframes spin {
        0% {transform:rotate(0deg);}
        100% {transform:rotate(360deg);}
    }

    </style>

    <div class="loader-overlay">
        <div class="loader"></div>
    </div>
    """, unsafe_allow_html=True)