
# pages/3_Data_Explorer.py

import streamlit as st
import pandas as pd
import plotly.express as px
import os

from src.utils import page_header
from src.theme import apply_dark_theme

@st.cache_data
def load_data():
    """
    Load processed dataset from data/processed_data.csv
    """
    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    DATA_PATH = os.path.join(
        BASE_DIR,
        "data",
        "processed_data.csv"
    )

    if not os.path.exists(DATA_PATH):
        st.error(
            f"""
            Processed data file not found.

            Expected path:
            {DATA_PATH}

            Please complete the Data Preprocessing step first.
            """
        )
        st.stop()

    return pd.read_csv(DATA_PATH)


@st.cache_data
def get_summary(df):
    return df.describe()


@st.cache_data
def get_correlation(df):

    numeric_cols = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if len(numeric_cols) >= 2:
        return df[numeric_cols].corr()

    return None


def show_data_explorer():

    apply_dark_theme()

    page_header(
        " Data Explorer",
        "Explore the processed airline customer dataset."
    )

    df = load_data()

    summary_df = get_summary(df)

    corr = get_correlation(df)

    # --------------------------------------------------
    # Load Data
    # --------------------------------------------------
    df = load_data()

    page = st.container()

    with page:

        # --------------------------------------------------
        # Dataset Overview
        # --------------------------------------------------

        st.markdown("## Dataset Overview")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rows", f"{df.shape[0]:,}")

        with col2:
            st.metric("Columns", f"{df.shape[1]:,}")

        # --------------------------------------------------
        # Data Preview
        # --------------------------------------------------

        st.markdown("## Data Preview")

        st.dataframe(
            df.head(10),
            width="stretch"
        )

        # --------------------------------------------------
        # Missing Values
        # --------------------------------------------------

        st.markdown("## Missing Values")

        missing_df = df.isnull().sum().reset_index()
        missing_df.columns = ["Column", "Missing Values"]

        missing_df = missing_df[
            missing_df["Missing Values"] > 0
        ]

        if missing_df.empty:
            st.success("No missing values found.")
        else:
            st.dataframe(
                missing_df,
                width="stretch"
            )

        # --------------------------------------------------
        # Summary Statistics
        # --------------------------------------------------

        st.markdown("## Summary Statistics")

        summary_df = get_summary(df)

        st.dataframe(
            summary_df,
            width="stretch"
        )

        # --------------------------------------------------
        # Feature Distribution
        # --------------------------------------------------

        st.markdown("## Feature Distribution")

        numeric_cols = df.select_dtypes(
            include="number"
        ).columns.tolist()

        if numeric_cols:

            selected_col = st.selectbox(
                "Select a numeric feature",
                numeric_cols
            )

            fig = px.histogram(
                df,
                x=selected_col,
                nbins=30,
                title=f"Distribution of {selected_col}",
                template="plotly_white"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        else:
            st.warning("No numeric columns found.")

        # --------------------------------------------------
        # Correlation Matrix
        # --------------------------------------------------

        st.markdown("## Correlation Matrix")

        corr = get_correlation(df)

        if corr is not None:

            fig = px.imshow(
                corr,
                text_auto=".2f",
                aspect="auto",
                title="Correlation Matrix"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        else:
            st.warning(
                "Not enough numeric columns for correlation analysis."
            )