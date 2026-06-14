import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import streamlit as st

st.set_option('client.showErrorDetails', True)


# =========================================================
# SRC IMPORTS
# =========================================================
from src.config import APP_TITLE
from src.utils import load_css
from src.navbar import show_topbar
from src.navigation import init_navigation

# =========================================================
# DATABASE IMPORT
# =========================================================

from database.database import create_tables

# =========================================================
# AUTH IMPORTS
# =========================================================

from Home_Panel.login import show_login
from Home_Panel.register import show_register
from Home_Panel.verify_otp import show_verify_otp

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title=APP_TITLE,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# DATABASE INIT
# =========================================================

if "db_initialized" not in st.session_state:
    create_tables()
    st.session_state.db_initialized = True

# =========================================================
# SESSION STATE
# =========================================================

query_params = st.query_params 
# ---------------------------------------------------------
#  LOGIN STATE 
# --------------------------------------------------------- 

if "logged_in" not in st.session_state: 
    st.session_state.logged_in = ( 
    query_params.get("logged_in", "false") == "true" 
    ) 
# --------------------------------------------------------- 
# USERNAME  
# --------------------------------------------------------- 
 
if "username" not in st.session_state: 
    st.session_state.username = query_params.get( 
        "username", 
        "" 
    ) 

# --------------------------------------------------------- 
# # ROLE 
# # --------------------------------------------------------- 
 
if "role" not in st.session_state: 
    st.session_state.role = query_params.get( 
        "role",
        "" 
    ) 

# =========================================================
# CURRENT PAGE
# =========================================================

if "current_page" not in st.session_state:
    st.session_state.current_page = query_params.get("page", "home")

init_navigation()

page = st.session_state.current_page

# =========================================================
# LOAD CSS
# =========================================================

load_css()


# ========================================================= 
# RESTORE LOGIN STATE FROM URL 
# ========================================================= 




# =========================================================
# TOPBAR
# =========================================================

if page not in [
    "register",
    "verify_otp"
]:
    show_topbar()

page = st.session_state.current_page


#if (
    #st.session_state.get("target_page")
    #and st.session_state.target_page != st.session_state.current_page
#):
    #show_loader()
    
    #st.session_state.current_page = st.session_state.target_page
    #st.query_params["page"] = st.session_state.target_page

    #st.session_state.loading = False

   # st.rerun()
# =========================================================
# PAGE CONTAINER
# =========================================================

page_container = st.empty()


# =========================================================
# PAGE ROUTING
# =========================================================

with page_container.container():

    # =====================================================
    # PUBLIC PAGES (BEFORE LOGIN)
    # =====================================================

    if not st.session_state.logged_in:

        # HOME
        if page == "home":

            from Home_Panel.Home import show_home
            show_home()

        # ABOUT
        elif page == "about":

            from Home_Panel.about import show_about
            show_about()

        # FEATURES
        elif page == "features_public":

            from Home_Panel.features_public import show_features_public
            show_features_public()

        # INSIGHTS
        #elif page == "insights_public":

            #from pages.insights_public import show_insights_public
            #show_insights_public()

        # ADMIN LOGIN
        elif page == "admin_login":

            show_login("admin")

        # CUSTOMER LOGIN
        elif page == "customer_login":

            show_login("customer")

        # REGISTER
        elif page == "register":

            show_register()

        # VERIFY OTP
        elif page == "verify_otp":

            show_verify_otp()

        # DEFAULT
        else:

            from Home_Panel.Home import show_home
            show_home()

    # =====================================================
    # LOGGED-IN ROUTING
    # =====================================================

    else:

        # HOME
        if page == "home":

            from Home_Panel.Home import show_home
            show_home()


        # EXPLORER
        elif page == "explorer":

            from Admin_Panel.Data_Explorer import show_data_explorer
            show_data_explorer()

        # FEATURES
        #elif page == "features":

            #from pages.Feature_Engineering import show_feature_engineering
            #show_feature_engineering()

        # PERFORMANCE
        elif page == "performance":

            from Admin_Panel.Model_Performance import show_model_performance
            show_model_performance()

        # PREDICTION
        elif page == "prediction":

            try:
                from Customer_Panel.Customer_Prediction import show_customer_prediction
                show_customer_prediction()

            except Exception as e:
                import traceback
                st.error(str(e))
                st.code(traceback.format_exc())
                
        # INSIGHTS
        elif page == "insights":

            from Customer_Panel.Cluster_Insights import show_cluster_insights
            show_cluster_insights()

        # DOWNLOAD
        elif page == "download":

            from Customer_Panel.Download_Results import show_download_results
            show_download_results()

        # ANALYZER
        elif page == "analyzer":

            from Admin_Panel.Auto_Analyzer import show_auto_analyzer
            show_auto_analyzer()

        # ADMIN DASHBOARD
        elif page == "admin":

            from Admin_Panel.admin_dashboard import show_admin_dashboard
            show_admin_dashboard()

        # CUSTOMER DASHBOARD
        elif page == "customer_dashboard":

            from Customer_Panel.customer_dashboard import show_customer_dashboard
            show_customer_dashboard()

        # PROFILE
        elif page == "profile":

            from Customer_Panel.profile import show_profile
            show_profile()

        # TICKETS
        elif page == "tickets":

            from Customer_Panel.my_tickets import show_my_tickets
            show_my_tickets()

        # SUPPORT
        elif page == "support":

            from Customer_Panel.support import show_support
            show_support()

        # DEFAULT
        else:

            from Home_Panel.Home import show_home
            show_home()
