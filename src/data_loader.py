# src/data_loader.py

from pathlib import Path
import pandas as pd
import streamlit as st

# Root directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Data folder and file path
DATA_DIR = BASE_DIR / "data"
DATA_PATH = DATA_DIR / "processed_data.csv"


@st.cache_data
def load_data():
    """
    Load processed dataset.

    Priority:
    1. data/processed_data.csv
    2. data/Processed_Data.csv
    3. Show user-friendly error if file does not exist
    """

    # Possible file names
    possible_files = [
        DATA_DIR / "processed_data.csv",
        DATA_DIR / "Processed_Data.csv",
    ]

    for file_path in possible_files:
        if file_path.exists():
            return pd.read_csv(file_path)

    # Friendly error message
    st.error("❌ Processed dataset not found.")
    st.info(
        """
        Please make sure one of the following files exists inside the `data` folder:

        - `data/processed_data.csv`
        - `data/Processed_Data.csv`

        If you have not uploaded or generated the processed dataset yet,
        run the data preprocessing step first.
        """
    )
    st.stop()