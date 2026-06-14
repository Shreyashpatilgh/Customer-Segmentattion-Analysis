import streamlit as st
import sqlite3

def show_refund_request():

    st.subheader(" Refund Request")

    ticket_id = st.text_input("Enter Ticket ID")

    reason = st.text_area("Reason")

    if st.button("Submit Request"):

        conn = sqlite3.connect("customer_segmentation.db")
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE bookings
        SET refund_status='Requested'
        WHERE id=?
        """, (ticket_id,))

        conn.commit()
        conn.close()

        st.success("✅ Refund Request Submitted")