
from narwhals import col
import streamlit as st
import os
import zipfile
from io import BytesIO
from src.utils import page_header
from src.theme import apply_dark_theme

def show_download_results():
    apply_dark_theme()
  
    page_header(" Download Results", "Download the results of the customer segmentation analysis.")

    #st.set_page_config(page_title="Download Results", layout="wide")
    #st.title(" Download Results")

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    FILES_TO_INCLUDE = [
        os.path.join(BASE_DIR, "data", "processed_data.csv"),
        os.path.join(BASE_DIR, "data", "cluster_results.csv"),
        os.path.join(BASE_DIR, "models", "kmeans_model.pkl"),
        os.path.join(BASE_DIR, "models", "scaler.pkl"),
        os.path.join(BASE_DIR, "models", "pca.pkl"),
        os.path.join(BASE_DIR, "models", "feature_columns.pkl"),
    ]

    # --------------------------------------------------
    # DEBUG SECTION: Show which files are available
    # --------------------------------------------------
    st.subheader("Available Files")

    for file_path in FILES_TO_INCLUDE:
        if os.path.exists(file_path):
            st.success(f"Found: {os.path.relpath(file_path, BASE_DIR)}")
        else:
            st.error(f"Missing: {os.path.relpath(file_path, BASE_DIR)}")

    # --------------------------------------------------
    # ZIP Creation Function
    # --------------------------------------------------
    def create_zip():
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for file_path in FILES_TO_INCLUDE:
                if os.path.exists(file_path):
                    arcname = os.path.relpath(file_path, BASE_DIR)
                    zip_file.write(file_path, arcname)

        zip_buffer.seek(0)
        return zip_buffer

    # --------------------------------------------------
    # Individual Download Buttons
    # --------------------------------------------------
    cols = st.columns(len(FILES_TO_INCLUDE))

    for col, file_path in zip(cols, FILES_TO_INCLUDE):
        with col:
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    st.download_button(
                        label=f"⬇ {os.path.basename(file_path)}",
                        data=f,
                        file_name=os.path.basename(file_path),
                        width="stretch"
                    )

    # --------------------------------------------------
    # ZIP Download Button
    # --------------------------------------------------
    zip_data = create_zip()

    st.download_button(
        label=" Download Complete Project Results (ZIP)",
        data=zip_data,
        file_name="customer_segmentation_results.zip",
        mime="application/zip"
    )
