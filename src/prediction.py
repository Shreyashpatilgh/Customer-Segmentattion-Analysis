# src/prediction.py

from pathlib import Path
import joblib
import pandas as pd
import sqlite3


# --------------------------------------------------
# Project Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODELS_DIR = BASE_DIR / "models"

DATABASE_DIR = BASE_DIR / "database"

DATABASE_PATH = DATABASE_DIR / "users.db"


# --------------------------------------------------
# Create Logs Table
# --------------------------------------------------

def create_logs_table():

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# --------------------------------------------------
# Save Prediction Log
# --------------------------------------------------

def save_prediction_log(action):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO logs (action)
        VALUES (?)
        """,
        (action,)
    )

    conn.commit()
    conn.close()


# --------------------------------------------------
# Load Required Model Files
# --------------------------------------------------

def load_model_files():
    """
    Load all required model artifacts.
    """

    required_files = {
        "kmeans": MODELS_DIR / "kmeans_model.pkl",
        "scaler": MODELS_DIR / "scaler.pkl",
        "pca": MODELS_DIR / "pca.pkl",
        "features": MODELS_DIR / "feature_columns.pkl",
    }

    # Check for missing files
    missing_files = [
        str(path)
        for path in required_files.values()
        if not path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            "Model files not found. Please train and save the model first.\n\n"
            + "\n".join(missing_files)
        )

    try:

        kmeans = joblib.load(required_files["kmeans"])
        scaler = joblib.load(required_files["scaler"])
        pca = joblib.load(required_files["pca"])
        feature_columns = joblib.load(required_files["features"])

    except Exception as e:

        raise ValueError(
            f"Unable to load model files.\n\n{e}"
        )

    return kmeans, scaler, pca, feature_columns


def predict_customer(input_df: pd.DataFrame) -> pd.DataFrame:
    """
    Predict customer segments for uploaded data.
    """

    # Create logs table
    create_logs_table()

    # Load artifacts
    kmeans, scaler, pca, feature_columns = load_model_files()

    # --------------------------------------------------
    # Ensure all required features exist
    # --------------------------------------------------
    for col in feature_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    # Keep only required columns in correct order
    X = input_df.reindex(columns=feature_columns)

    # Convert safely AFTER alignment
    X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

    # --------------------------------------------------
    # SCALE
    # --------------------------------------------------
    X_scaled = scaler.transform(X)

    # --------------------------------------------------
    # PCA
    # --------------------------------------------------
    X_pca = pca.transform(X_scaled)

    # --------------------------------------------------
    # PREDICT
    # --------------------------------------------------
    clusters = kmeans.predict(X_pca)

    # --------------------------------------------------
    # RESULT
    # --------------------------------------------------
    result_df = input_df.copy()
    result_df["Predicted_Cluster"] = clusters

    return result_df

    # LOG
    #save_prediction_log(
        #f"Prediction performed for {len(result_df)} customers"
    #)

