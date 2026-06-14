# pages/Customer_Prediction.py

import streamlit as st
import pandas as pd
import traceback

from src.prediction import predict_customer
from src.utils import page_header
from src.theme import apply_dark_theme
from database.database import get_connection
from loader import show_loader

# =====================================================
# LOAD CUSTOMER IDS
# =====================================================
def load_customer_ids():
    customer_ids = []
    file_path = r"F:\Workspace\Airlines_Customer_Segmentation\Customer_Segmentation_App\data\processed_data.csv"

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            next(file)

            for i, line in enumerate(file):
                if i > 5000:
                    break

                try:
                    customer_id = line.split(",")[0].strip()

                    if customer_id:
                        customer_ids.append(customer_id)

                except Exception:
                    pass

    except Exception:
        customer_ids = ["1000001", "1000002", "1000003"]

    return sorted(list(set(customer_ids)))


customer_ids = load_customer_ids()


# =====================================================
# MAIN PAGE
# =====================================================
def show_customer_prediction():
    placeholder = st.empty()

    with placeholder.container():
        apply_dark_theme()

        page_header(
                "Customer Segmentation Prediction",
                "Predict customer segment using ML model."
            )

        # =====================================================
        # SESSION STATE
        # =====================================================
        if "prediction_result" not in st.session_state:
            st.session_state.prediction_result = None

        if "prediction_segment" not in st.session_state:
            st.session_state.prediction_segment = None

        SEGMENT_NAMES = {
            0: "Premium Customers",
            1: "Frequent Travelers",
            2: "Satisfied Customers",
            3: "At-Risk Customers",
            4: "New Customers"
        }

        # =====================================================
        # INPUT FORM
        # =====================================================
        st.markdown('<div class="prediction-card">', unsafe_allow_html=True)

        with st.form("customer_prediction_form"):

            st.subheader("Customer Information")

            col1, col2 = st.columns(2)

            with col1:
                customer_id = st.number_input(
                    "Customer ID",
                    min_value=1000000,
                    value=1000001
                )

                gender = st.number_input(
                    "Gender (0 = Female, 1 = Male)",
                    min_value=0,
                    max_value=1,
                    value=1
                )

                age = st.slider(
                    "Age",
                    min_value=18,
                    max_value=80,
                    value=30
                )

                annual_income = st.number_input(
                    "Annual Income",
                    min_value=0,
                    value=50000
                )

                travel_type = st.number_input(
                    "Travel Type (0 = Personal, 1 = Business)",
                    min_value=0,
                    max_value=1,
                    value=1
                )

            with col2:
                travel_class = st.number_input(
                    "Travel Class (0 = Eco, 1 = Eco Plus, 2 = Business)",
                    min_value=0,
                    max_value=2,
                    value=2
                )

                flight_distance = st.number_input(
                    "Flight Distance",
                    min_value=0,
                    value=1500
                )

                flights_per_year = st.number_input(
                    "Flights Per Year",
                    min_value=0,
                    value=5
                )

                customer_satisfaction = st.slider(
                    "Customer Satisfaction",
                    min_value=1,
                    max_value=5,
                    value=3
                )

                inflight_wifi = st.slider(
                    "Inflight WiFi Service",
                    min_value=0,
                    max_value=5,
                    value=3
                )

            col3, col4 = st.columns(2)

            with col3:
                online_boarding = st.slider(
                    "Online Boarding",
                    min_value=0,
                    max_value=5,
                    value=3
                )

            with col4:
                cleanliness = st.slider(
                    "Cleanliness",
                    min_value=0,
                    max_value=5,
                    value=3
                )

            submit = st.form_submit_button(
                "Predict Customer Segment",
                key="book_ticket",
                use_container_width=True
            )

        # =====================================================
        # BUTTON CLICK EVENT
        # =====================================================
        if submit:

            st.success(" Button clicked successfully!")

            try:

                st.info("Preparing input data...")

                input_data = {
                    "Customer_ID": float(customer_id),
                    "Gender": float(gender),
                    "Age": float(age),
                    "Type_Of_Travel": float(travel_type),
                    "Travel_Class": float(travel_class),
                    "Flight_Distance": float(flight_distance),
                    "Flights_Per_Year": float(flights_per_year),
                    "Annual_Income": float(annual_income),
                    "Customer_Satisfaction": float(customer_satisfaction),
                    "Inflight_Wifi_Service": float(inflight_wifi),
                    "Online_Boarding": float(online_boarding),
                    "Cleanliness": float(cleanliness)
                }

                input_df = pd.DataFrame([input_data])

                st.subheader("Input Data")
                st.dataframe(input_df, width="stretch")

                st.info("Calling prediction model...")

                result = predict_customer(input_df)
                st.session_state.prediction_result = result

                # Save result in session
                st.session_state.prediction_result = result

                st.success("Prediction function executed!")

                st.subheader("Raw Prediction Result")
                st.dataframe(result, width="stretch")

                if result is None:
                    st.error("predict_customer() returned None")
                    return

                if len(result) == 0:
                    st.error("Prediction result is empty")
                    return

                if "Predicted_Cluster" not in result.columns:
                    st.error(
                        f"Column 'Predicted_Cluster' not found.\nAvailable columns: {list(result.columns)}"
                    )
                    return

                cluster = int(result.iloc[0]["Predicted_Cluster"])
                conn = get_connection()
                cursor = conn.cursor()

                segment_name = SEGMENT_NAMES.get(
                    cluster,
                    f"Cluster {cluster}"
                )

                customer_email = st.session_state.get(
                    "email",
                    "unknown"
                )

                cursor.execute(
                    """
                    INSERT INTO predictions
                    (
                        customer_email,
                        prediction_result,
                        confidence
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        customer_email,
                        segment_name,
                        0.0
                    )
                )

                cursor.execute(
                    """
                    INSERT INTO customer_segments
                    (
                        customer_email,
                        segment_name
                    )
                    VALUES (?, ?)
                    """,
                    (
                        customer_email,
                        segment_name
                    )
                )

                conn.commit()
                conn.close()
                st.session_state.prediction_segment = cluster

                

                segment_name = SEGMENT_NAMES.get(
                    cluster,
                    f"Cluster {cluster}"
                )

                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(135deg,#1e3c72,#2a5298);
                        padding:30px;
                        border-radius:20px;
                        text-align:center;
                        color:white;
                        margin-top:20px;
                    ">
                        <h1>{segment_name}</h1>
                        <h3>Cluster {cluster}</h3>
                        <p>Customer successfully classified.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.success("Prediction completed successfully!")

            except Exception as e:

                st.error("Prediction Failed!")

                st.error(str(e))

                st.code(
                    traceback.format_exc(),
                    language="python"
                )

            # =====================================================
            # DISPLAY SAVED RESULT
            # =====================================================
        if st.session_state.prediction_result is not None:

                st.markdown("---")
                st.subheader("Saved Prediction Result")

                st.dataframe(
                    st.session_state.prediction_result,
                    width="stretch"
                )

                cluster = st.session_state.prediction_segment

                if cluster is not None:

                    segment_name = SEGMENT_NAMES.get(
                        cluster,
                        f"Cluster {cluster}"
                    )

                    st.success(
                        f"Predicted Segment: {segment_name}"
                    )

                if st.button(
                    "Predict New",
                    key="predict_new",
                    use_container_width=True
                ):
                    st.session_state.prediction_result = None
                    st.session_state.prediction_segment = None
                    st.rerun()
