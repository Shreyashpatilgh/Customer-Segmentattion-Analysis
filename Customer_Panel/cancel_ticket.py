import streamlit as st
import sqlite3
import pandas as pd

def show_cancel_ticket():

    st.subheader(" Cancel Ticket")

    conn = sqlite3.connect("customer_segmentation.db")

    query = """
    SELECT
        id,
        passenger_name,
        source,
        destination
    FROM bookings
    WHERE user_email=?
    AND status='Booked'
    """

    df = pd.read_sql(
        query,
        conn,
        params=[st.session_state.email]
    )

    conn.close()

    if df.empty:
        st.warning("No Active Tickets")
        return

    ticket_id = st.selectbox(
        "Select Ticket ID",
        df["id"]
    )

    if st.button("Cancel Ticket"):

        conn = sqlite3.connect("customer_segmentation.db")
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE bookings
        SET status='Cancelled'
        WHERE id=?
        """, (ticket_id,))

        conn.commit()
        conn.close()

        st.success(" Ticket Cancelled")