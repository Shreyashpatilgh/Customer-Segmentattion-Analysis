# pages/9_AutoAnalyzer.py
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from src.utils import page_header
from src.theme import apply_dark_theme

def show_auto_analyzer():
    apply_dark_theme()

    st.markdown("""
    <style>

    /* Auto Analyzer - Browse Files Button Text Fix */

    div[data-testid="stFileUploader"] button,
    div[data-testid="stFileUploader"] button * {

        color: #111827 !important;
        font-weight: 700 !important;
    }

    /* Auto Analyzer - Vibrant styled tables with sticky headers */

    div[data-testid="stDataFrame"],
    div[data-testid="stTable"] {
        background-color: transparent !important;
        padding: 6px !important;
        overflow-x: auto !important;
    }

    /* Inner table wrapper */
    div[data-testid="stDataFrame"] div[role="table"],
    div[data-testid="stDataFrame"] div[role="grid"],
    div[data-testid="stTable"] div[role="table"],
    div[data-testid="stTable"] div[role="grid"] {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%) !important;
        border-radius: 12px !important;
        box-shadow: 0 6px 18px rgba(2,6,23,0.35) inset !important;
        border: 1px solid rgba(59,130,246,0.18) !important;
        padding: 6px !important;
    }

    /* Table header styling */
    div[data-testid="stDataFrame"] th,
    div[data-testid="stTable"] th {
        background: linear-gradient(90deg, #60a5fa, #2563eb) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        font-size: 12px !important;
        position: sticky !important;
        top: 0 !important;
        z-index: 5 !important;
        box-shadow: 0 3px 6px rgba(37,99,235,0.12) !important;
        border-bottom: 1px solid rgba(255,255,255,0.12) !important;
    }

    /* Cells */
    div[data-testid="stDataFrame"] td,
    div[data-testid="stTable"] td {
        background-color: transparent !important;
        color: #0f172a !important;
        padding: 10px 12px !important;
        border-bottom: 1px solid rgba(226,232,240,0.6) !important;
        vertical-align: middle !important;
    }

    /* Zebra rows */
    div[data-testid="stDataFrame"] tr:nth-child(even) td,
    div[data-testid="stTable"] tr:nth-child(even) td {
        background: rgba(59,130,246,0.04) !important;
    }

    /* Hover */
    div[data-testid="stDataFrame"] tr:hover td,
    div[data-testid="stTable"] tr:hover td {
        background: rgba(59,130,246,0.08) !important;
    }

    /* Rounded table container */
    div[data-testid="stDataFrame"] > div:first-child,
    div[data-testid="stTable"] > div:first-child {
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* Small screens: reduce padding */
    @media (max-width: 900px) {
        div[data-testid="stDataFrame"] td,
        div[data-testid="stTable"] td {
            padding: 8px 6px !important;
        }
    }

    </style>
    """, unsafe_allow_html=True)

# PAGE CONFIGURATION

   
    page_header(
        " Customer Analytics Engine",
        "Upload any dataset and automatically perform data understanding, "
        "cleaning, EDA, model selection, evaluation and prediction."
    )

    # HELPER FUNCTIONS

    def load_uploaded_file(uploaded_file):
        """Load CSV or Excel file."""
        if uploaded_file.name.endswith(".csv"):
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            return pd.read_excel(uploaded_file)
        else:
            raise ValueError("Unsupported file format.")


    def detect_problem_type(df, target_col):
        """
        Detect whether the problem is:
        - Clustering
        - Classification
        - Regression
        """
        if target_col is None:
            return "Clustering"

        y = df[target_col]

        # Object / category => classification
        if y.dtype == "object" or str(y.dtype) == "category":
            return "Classification"

        # Small number of unique values => classification
        if y.nunique() <= 20:
            return "Classification"

        # Otherwise regression
        return "Regression"


    def clean_data(df):
        """
        Automatically:
        - Remove duplicates
        - Remove all-null columns
        - Fill numeric nulls with median
        - Fill categorical nulls with mode
        """
        clean_df = df.copy()

        # Remove duplicates
        duplicate_count = int(clean_df.duplicated().sum())
        if duplicate_count > 0:
            clean_df = clean_df.drop_duplicates()

        # Remove all-null columns
        all_null_cols = clean_df.columns[clean_df.isna().all()].tolist()
        if all_null_cols:
            clean_df = clean_df.drop(columns=all_null_cols)

        # Missing before
        missing_before = int(clean_df.isna().sum().sum())

        # Numeric columns
        numeric_cols = clean_df.select_dtypes(include=np.number).columns.tolist()

        # Categorical columns
        categorical_cols = clean_df.select_dtypes(exclude=np.number).columns.tolist()

        # Fill numeric
        for col in numeric_cols:
            if clean_df[col].isna().sum() > 0:
                clean_df[col] = clean_df[col].fillna(clean_df[col].median())

        # Fill categorical
        for col in categorical_cols:
            if clean_df[col].isna().sum() > 0:
                mode = clean_df[col].mode()
                fill_value = mode.iloc[0] if not mode.empty else "Unknown"
                clean_df[col] = clean_df[col].fillna(fill_value)

        # Missing after
        missing_after = int(clean_df.isna().sum().sum())

        summary = {
            "duplicates_removed": duplicate_count,
            "columns_removed": len(all_null_cols),
            "missing_before": missing_before,
            "missing_after": missing_after,
            "removed_columns": all_null_cols
        }

        return clean_df, summary


    def build_preprocessor(X):
        """
        Build preprocessing pipeline.
        """
        numeric_cols = X.select_dtypes(include=np.number).columns.tolist()
        categorical_cols = X.select_dtypes(exclude=np.number).columns.tolist()

        numeric_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])

        categorical_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore"))
        ])

        preprocessor = ColumnTransformer([
            ("num", numeric_pipeline, numeric_cols),
            ("cat", categorical_pipeline, categorical_cols)
        ])

        return preprocessor


    def safe_train_test_split(X, y):
        """
        Safer train/test split.
        """
        test_size = 0.2 if len(X) >= 10 else 0.3

        stratify = None

        if y.nunique() > 1 and y.nunique() <= 20:
            min_class_count = y.value_counts().min()
            if min_class_count >= 2:
                stratify = y

        return train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=42,
            stratify=stratify
        )


    # FILE UPLOAD + DATA UNDERSTANDING + DATA CLEANING + EDA

    # FILE UPLOAD

    st.markdown(
    """
    <div style="height:20px;"></div>
    """,
    unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        " Upload CSV or Excel File",
        type=["csv", "xlsx"]
    )

    

    if uploaded_file is None:
        st.info(" Upload a CSV or Excel file to begin the automated analysis.")
        st.stop()

    # Load data
    try:
        df = load_uploaded_file(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    st.success(f"✅ Dataset loaded successfully! Shape: {df.shape}")

    # 1️: DATA UNDERSTANDING

    st.header("1️⃣ Data Understanding")

    st.subheader(" Dataset Preview")
    st.dataframe(df.head(), width="stretch")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{df.shape[0]:,}")
    c2.metric("Columns", df.shape[1])
    c3.metric("Missing Values", int(df.isna().sum().sum()))
    c4.metric("Duplicate Rows", int(df.duplicated().sum()))

    # Column information
    st.subheader(" Column Information")

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isna().sum().values,
        "Unique Values": [df[col].nunique() for col in df.columns]
    })

    st.dataframe(info_df, width="stretch")

    # Summary statistics
    st.subheader(" Summary Statistics")
    st.dataframe(
        df.describe(),
        width="stretch"
    )

    # 2️: DATA CLEANING

    st.header(" Data Cleaning")

    clean_df, cleaning_summary = clean_data(df)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Duplicates Removed", cleaning_summary["duplicates_removed"])
    c2.metric("Columns Removed", cleaning_summary["columns_removed"])
    c3.metric("Missing Before", cleaning_summary["missing_before"])
    c4.metric("Missing After", cleaning_summary["missing_after"])

    if cleaning_summary["missing_after"] == 0:
        st.success(" All missing values have been handled automatically.")

    st.write(f"Cleaned dataset shape: **{clean_df.shape}**")

    if cleaning_summary["removed_columns"]:
        with st.expander(" Removed Columns"):
            st.write(cleaning_summary["removed_columns"])

    # Show cleaned preview
    with st.expander(" Cleaned Data Preview"):
        st.dataframe(clean_df.head(), width="stretch")

    # 3️: EXPLORATORY DATA ANALYSIS

    st.header(" Exploratory Data Analysis")

    numeric_cols = clean_df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = clean_df.select_dtypes(exclude=np.number).columns.tolist()

    # Visualization 1: Correlation Heatmap

    if len(numeric_cols) >= 2:
        st.subheader(" Correlation Heatmap")

        corr = clean_df[numeric_cols].corr()

        fig = px.imshow(
            corr,
            text_auto=".2f",
            aspect="auto",
            title="Correlation Matrix"
        )
        st.plotly_chart(fig, width="stretch")


    # Visualization 2: Histogram

    if numeric_cols:
        st.subheader(" Distribution Histogram")

        hist_col = st.selectbox(
            "Select Numeric Column",
            numeric_cols,
            key="hist_col"
        )

        fig = px.histogram(
            clean_df,
            x=hist_col,
            nbins=30,
            title=f"Distribution of {hist_col}"
        )

        st.plotly_chart(fig, width="stretch")


    # Visualization 3: Box Plot

    if numeric_cols:
        st.subheader(" Box Plot")

        box_col = st.selectbox(
            "Select Column for Box Plot",
            numeric_cols,
            key="box_col"
        )

        fig = px.box(
            clean_df,
            y=box_col,
            title=f"Box Plot of {box_col}"
        )

        st.plotly_chart(fig, width="stretch")


    # Visualization 4: Scatter Plot

    if len(numeric_cols) >= 2:
        st.subheader(" Scatter Plot")

        x_col = st.selectbox(
            "X-Axis",
            numeric_cols,
            key="scatter_x"
        )

        y_col = st.selectbox(
            "Y-Axis",
            numeric_cols,
            index=1 if len(numeric_cols) > 1 else 0,
            key="scatter_y"
        )

        fig = px.scatter(
            clean_df,
            x=x_col,
            y=y_col,
            title=f"{x_col} vs {y_col}"
        )

        st.plotly_chart(fig, width="stretch")


    # Visualization 5: Category Distribution

    if categorical_cols:
        st.subheader(" Category Distribution")

        cat_col = st.selectbox(
            "Select Categorical Column",
            categorical_cols,
            key="cat_col"
        )

        cat_counts = (
            clean_df[cat_col]
            .astype(str)
            .value_counts()
            .head(10)
            .reset_index()
        )

        cat_counts.columns = [cat_col, "Count"]

        fig = px.bar(
            cat_counts,
            x=cat_col,
            y="Count",
            title=f"Top Categories in {cat_col}"
        )

        st.plotly_chart(fig, width="stretch")

    # 4️: PROBLEM DEFINITION

    st.header(" Problem Definition")

    target_options = ["None (Clustering)"] + clean_df.columns.tolist()

    selected_target = st.selectbox(
        " Select Target Column",
        target_options
    )

    target_col = (
        None
        if selected_target == "None (Clustering)"
        else selected_target
    )

    problem_type = detect_problem_type(clean_df, target_col)

    st.info(f" Detected Problem Type: **{problem_type}**")


    # 5️: MODELING & EVALUATION + 6️: RESULTS

    st.header(" Modeling & Evaluation")

    if st.button(" Run Full Analysis", width="stretch"):
        from sklearn.model_selection import train_test_split
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        from sklearn.impute import SimpleImputer
        from sklearn.preprocessing import (
            OneHotEncoder,
            StandardScaler,
            LabelEncoder
        )

        from sklearn.metrics import (
            accuracy_score,
            r2_score,
            mean_squared_error,
            silhouette_score
        )

        from sklearn.ensemble import (
            RandomForestClassifier,
            RandomForestRegressor,
            GradientBoostingClassifier,
            GradientBoostingRegressor
        )

        from sklearn.linear_model import (
            LogisticRegression,
            LinearRegression
        )

        from sklearn.cluster import KMeans
        from sklearn.decomposition import PCA

        with st.spinner("Running end-to-end data science pipeline..."):

            
            # CLUSTERING
        
            if problem_type == "Clustering":

                numeric_df = clean_df.select_dtypes(include=np.number)

                if numeric_df.shape[1] < 2:
                    st.error("At least 2 numeric columns are required for clustering.")
                    st.stop()

                # Preprocessing
                preprocess = Pipeline([
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ])

                X_processed = preprocess.fit_transform(numeric_df)

                # Try different cluster counts and choose best silhouette score
                cluster_results = []
                best_score = -1
                best_model = None
                best_clusters = None
                best_k = None

                max_k = min(8, len(clean_df) - 1)

                for k in range(2, max_k + 1):
                    try:
                        model = KMeans(
                            n_clusters=k,
                            random_state=42,
                            n_init=10
                        )

                        clusters = model.fit_predict(X_processed)

                        score = silhouette_score(
                            X_processed,
                            clusters
                        )

                        cluster_results.append({
                            "Clusters": k,
                            "Silhouette Score": round(score, 4)
                        })

                        if score > best_score:
                            best_score = score
                            best_model = model
                            best_clusters = clusters
                            best_k = k

                    except Exception:
                        pass

                if best_model is None:
                    st.error("Unable to perform clustering.")
                    st.stop()

                # Show comparison
                st.subheader(" Cluster Comparison")
                cluster_df = pd.DataFrame(cluster_results)
                st.dataframe(cluster_df, width="stretch")

                st.success(
                    f" Best Number of Clusters: {best_k} "
                    f"(Silhouette Score: {best_score:.4f})"
                )

                # Final result
                result_df = clean_df.copy()
                result_df["Cluster"] = best_clusters

                # Cluster distribution
                st.subheader(" Cluster Distribution")

                cluster_counts = (
                    result_df["Cluster"]
                    .value_counts()
                    .sort_index()
                    .reset_index()
                )
                cluster_counts.columns = ["Cluster", "Count"]

                fig = px.bar(
                    cluster_counts,
                    x="Cluster",
                    y="Count",
                    text="Count",
                    title="Cluster Distribution"
                )
                st.plotly_chart(fig, width="stretch")

                # PCA Visualization
                st.subheader(" PCA Cluster Visualization")

                pca = PCA(n_components=2)
                pca_result = pca.fit_transform(X_processed)

                pca_df = pd.DataFrame({
                    "PC1": pca_result[:, 0],
                    "PC2": pca_result[:, 1],
                    "Cluster": best_clusters.astype(str)
                })

                fig = px.scatter(
                    pca_df,
                    x="PC1",
                    y="PC2",
                    color="Cluster",
                    title="PCA Visualization"
                )
                st.plotly_chart(fig, width="stretch")

            # CLASSIFICATION / REGRESSION
            
            else:
                X = clean_df.drop(columns=[target_col])
                y = clean_df[target_col]

                # Encode target if classification and categorical
                label_encoder = None

                if problem_type == "Classification":
                    if y.dtype == "object" or str(y.dtype) == "category":
                        label_encoder = LabelEncoder()
                        y_encoded = label_encoder.fit_transform(
                            y.astype(str)
                        )
                    else:
                        y_encoded = y
                else:
                    y_encoded = y

                # Build preprocessor
                preprocessor = build_preprocessor(X)

                # Train/test split
                X_train, X_test, y_train, y_test = safe_train_test_split(
                    X,
                    y_encoded
                )

                # Candidate models
                if problem_type == "Classification":
                    candidate_models = {
                        "Random Forest": RandomForestClassifier(
                            n_estimators=50,
                            random_state=42,
                            n_jobs=-1
                        ),
                        "Logistic Regression": LogisticRegression(
                            max_iter=2000
                        ),
                        "Gradient Boosting": GradientBoostingClassifier(
                            random_state=42
                        )
                    }
                    metric_name = "Accuracy"

                else:  # Regression
                    candidate_models = {
                        "Random Forest": RandomForestRegressor(
                            n_estimators=50,
                            random_state=42,
                            n_jobs=-1
                        ),
                        "Linear Regression": LinearRegression(),
                        "Gradient Boosting": GradientBoostingRegressor(
                            random_state=42
                        )
                    }
                    metric_name = "R² Score"

                # Compare models
                comparison_results = []

                best_score = -float("inf")
                best_model_name = None
                best_pipeline = None

                for model_name, model in candidate_models.items():

                    pipeline = Pipeline([
                        ("preprocessor", preprocessor),
                        ("model", model)
                    ])

                    try:
                        pipeline.fit(X_train, y_train)
                        y_pred = pipeline.predict(X_test)

                        if problem_type == "Classification":
                            score = accuracy_score(y_test, y_pred)
                        else:
                            score = r2_score(y_test, y_pred)

                        comparison_results.append({
                            "Model": model_name,
                            metric_name: round(score, 4)
                        })

                        if score > best_score:
                            best_score = score
                            best_model_name = model_name
                            best_pipeline = pipeline

                    except Exception as ex:
                        comparison_results.append({
                            "Model": model_name,
                            metric_name: f"Error: {str(ex)[:60]}"
                        })

                if best_pipeline is None:
                    st.error("Unable to train any model.")
                    st.stop()

                # Model comparison table
                st.subheader(" Model Comparison")
                comparison_df = pd.DataFrame(comparison_results)
                st.dataframe(comparison_df, width="stretch")

                # Best model
                st.success(
                    f" Best Model Selected: {best_model_name} "
                    f"({metric_name}: {best_score:.4f})"
                )

                # Additional metrics
                best_y_pred = best_pipeline.predict(X_test)

                if problem_type == "Classification":
                    st.metric("Accuracy", f"{best_score:.4f}")
                else:
                    rmse = np.sqrt(
                        mean_squared_error(y_test, best_y_pred)
                    )

                    c1, c2 = st.columns(2)
                    c1.metric("R² Score", f"{best_score:.4f}")
                    c2.metric("RMSE", f"{rmse:.4f}")

                # Feature Importance
                st.subheader(" Top 10 Important Features")

                try:
                    model = best_pipeline.named_steps["model"]

                    if hasattr(model, "feature_importances_"):
                        feature_names = (
                            best_pipeline
                            .named_steps["preprocessor"]
                            .get_feature_names_out()
                        )

                        importances = model.feature_importances_

                        fi_df = pd.DataFrame({
                            "Feature": feature_names,
                            "Importance": importances
                        })

                        fi_df = (
                            fi_df
                            .sort_values(
                                "Importance",
                                ascending=False
                            )
                            .head(10)
                        )

                        fig = px.bar(
                            fi_df,
                            x="Importance",
                            y="Feature",
                            orientation="h",
                            title="Top 10 Important Features"
                        )

                        st.plotly_chart(
                            fig,
                            width="stretch"
                        )
                    else:
                        st.info(
                            "Feature importance is not available "
                            "for the selected model."
                        )
                except Exception as e:
                    st.info(
                        f"Feature importance could not be generated: {e}"
                    )

                # Full predictions
                full_predictions = best_pipeline.predict(X)

                # Decode predictions if needed
                if (
                    problem_type == "Classification"
                    and label_encoder is not None
                ):
                    full_predictions = label_encoder.inverse_transform(
                        full_predictions.astype(int)
                    )

                # Final results
                result_df = clean_df.copy()
                result_df["Prediction"] = full_predictions

        
            # 6️: RESULTS
            
            st.header(" Results")

            st.subheader(" Result Preview")
            st.dataframe(
                result_df.head(20),
                width="stretch"
            )

            # Download button
            csv = result_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label=" Download Results",
                data=csv,
                file_name="automl_results.csv",
                mime="text/csv",
                width="stretch"
            )