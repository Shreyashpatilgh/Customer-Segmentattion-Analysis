import streamlit as st
import sqlite3
import random

def show_book_ticket():

    st.subheader(" Book Flight Ticket")

    passenger_name = st.text_input("Passenger Name")

    source = st.selectbox(
        "Source",
        ["Mumbai", "Pune", "Delhi", "Bangalore"]
    )

    destination = st.selectbox(
        "Destination",
        ["Dubai", "London", "Singapore", "New York"]
    )

    journey_date = st.date_input("Journey Date")

    if st.button("Book Ticket"):

        seat_no = "A" + str(random.randint(1, 100))

        conn = sqlite3.connect("customer_segmentation.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO bookings
        (
            user_email,
            passenger_name,
            source,
            destination,
            journey_date,
            seat_no,
            status,
            refund_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            st.session_state.email,
            passenger_name,
            source,
            destination,
            str(journey_date),
            seat_no,
            "Booked",
            "Not Requested"
        ))

        conn.commit()
        conn.close()

        st.success("✅ Ticket Booked Successfully")

        st.info(f"""
Passenger Name : {passenger_name}

Route : {source} ➜ {destination}

Journey Date : {journey_date}

Seat Number : {seat_no}

Status : Confirmed
""")