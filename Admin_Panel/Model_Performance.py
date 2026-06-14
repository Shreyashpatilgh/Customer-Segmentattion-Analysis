
import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
import traceback

from src.utils import page_header
from src.theme import apply_dark_theme

def show_model_performance():
    apply_dark_theme()

    st.set_page_config(page_title="Model Performance", layout="wide")
    st.title(" Model Performance")

    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    MODELS_DIR = os.path.join(BASE_DIR, "models")

    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)

    PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "processed_data.csv")

    # Check processed data
    if not os.path.exists(PROCESSED_DATA_PATH):
        st.error(f"File not found: {PROCESSED_DATA_PATH}")
        st.stop()

    # Load data
    df = pd.read_csv(PROCESSED_DATA_PATH)
    st.success("Processed data loaded successfully.")
    st.write("Shape:", df.shape)

    # Numeric columns
    X = df.select_dtypes(include=[np.number])

    if X.empty:
        st.error("No numeric columns found.")
        st.stop()

    st.write("Numeric columns used for clustering:")
    st.write(X.columns.tolist())

    # Number of clusters
    n_clusters = st.slider("Select Number of Clusters", 2, 10, 4)

    # Train button
    if st.button("Train KMeans Model"):
        from sklearn.preprocessing import StandardScaler
        from sklearn.decomposition import PCA
        from sklearn.cluster import KMeans

        try:
            st.info("Step 1: Scaling data...")
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            st.info("Step 2: Applying PCA...")
            n_components = min(2, X_scaled.shape[1])
            pca = PCA(n_components=n_components)
            X_pca = pca.fit_transform(X_scaled)

            st.info("Step 3: Training KMeans...")
            kmeans = KMeans(
                n_clusters=n_clusters,
                random_state=42,
                n_init=10
            )
            clusters = kmeans.fit_predict(X_pca)


            st.info("Step 4: Saving cluster results...")
            df["Cluster"] = clusters
            cluster_results_path = os.path.join(DATA_DIR, "cluster_results.csv")
            df.to_csv(cluster_results_path, index=False)

            st.info("Step 5: Saving model files...")
            feature_columns = X.columns.tolist()

            joblib.dump(kmeans, os.path.join(MODELS_DIR, "kmeans_model.pkl"))
            joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.pkl"))
            joblib.dump(pca, os.path.join(MODELS_DIR, "pca.pkl"))
            joblib.dump(feature_columns, os.path.join(MODELS_DIR, "feature_columns.pkl"))

            st.success(" Model trained and saved successfully!")
          
            st.subheader("Saved Files")
            st.write("✅ data/cluster_results.csv")
            st.write("✅ models/kmeans_model.pkl")
            st.write("✅ models/scaler.pkl")
            st.write("✅ models/pca.pkl")
            st.write("✅ models/feature_columns.pkl")

        except Exception as e:
            st.error("An error occurred during model training.")
            st.exception(e)
            st.code(traceback.format_exc())
