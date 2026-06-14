
from database.database import get_connection
import pandas as pd
import streamlit as st
from fpdf import FPDF
import os

from src.theme import apply_dark_theme


# =====================================================
# MY TICKETS PAGE
# =====================================================

def show_my_tickets():
    apply_dark_theme()

    # =====================================================
    # TITLE
    # =====================================================

    st.title("Airlines Ticket Dashboard")

    st.write(
        "Manage bookings, ticket history, cancellations and refunds."
    )

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "booking_success" not in st.session_state:
        st.session_state.booking_success = False

    if "booking_price" not in st.session_state:
        st.session_state.booking_price = 0

    if st.session_state.booking_success:

        st.success(
            f"""
            Ticket Booked Successfully

            Ticket Price:
            ₹ {st.session_state.booking_price}
            """
        )

        st.session_state.booking_success = False

    # =====================================================
    # DATABASE
    # =====================================================

    conn = get_connection()

    email = st.session_state.username

    query = """
    SELECT *
    FROM bookings
    ORDER BY id DESC
    """

    bookings = pd.read_sql(
        query,
        conn
    )

    # =====================================================
    # PRICE LOGIC
    # =====================================================

    route_prices = {

        ("Mumbai", "Dubai"): 18000,
        ("Mumbai", "London"): 45000,
        ("Mumbai", "Singapore"): 22000,
        ("Mumbai", "Paris"): 50000,
        ("Mumbai", "New York"): 75000,

        ("Delhi", "Dubai"): 17000,
        ("Delhi", "London"): 42000,
        ("Delhi", "Singapore"): 21000,
        ("Delhi", "Paris"): 48000,
        ("Delhi", "New York"): 72000,

        ("Pune", "Dubai"): 20000,
        ("Pune", "London"): 47000,
        ("Pune", "Singapore"): 24000,
        ("Pune", "Paris"): 52000,
        ("Pune", "New York"): 78000,
    }

    # =====================================================
    # TABS
    # =====================================================

    tab1, tab2, tab3, tab4, tab5,tab6 = st.tabs([

        "Ticket Booking",
        "Ticket History",
        "Payment Status",
        "Cancel Ticket",
        "Refund Request",
        "Feedback"
    ])

    # =====================================================
    # BOOK TICKET
    # =====================================================

    with tab1:

        st.subheader("Book New Ticket")

        col1, col2 = st.columns(2)

        with col1:

            passenger_name = st.text_input(
                "Passenger Name"
            )

            source = st.selectbox(
                "Source",
                [
                    "Mumbai",
                    "Delhi",
                    "Pune"
                ],
                key="source_select"
            )

            seat_no = st.selectbox(
                "Seat Number",
                [f"A{i}" for i in range(1, 101)],
                key="seat_select"
            )

        with col2:

            destination = st.selectbox(
                "Destination",
                [
                    "Dubai",
                    "London",
                    "Singapore",
                    "Paris",
                    "New York"
                ],
                key="destination_select"
            )

            journey_date = st.date_input(
                "Journey Date"
            )

            price = route_prices.get(
                (source, destination),
                15000
            )

            st.text_input(
                "Ticket Price",
                value=f"₹ {price}",
                disabled=True
            )
            

        if st.button(
            "Book Ticket",
            key="book_ticket_btn",
            use_container_width=True
        ):

            cursor = conn.cursor()

            insert_query = """
            INSERT INTO bookings
            (
                user_email,
                passenger_name,
                source,
                destination,
                journey_date,
                seat_no,
                status,
                refund_status,
                payment_status
            )
            VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            cursor.execute(

                insert_query,

                (
                    email,
                    passenger_name,
                    source,
                    destination,
                    str(journey_date),
                    seat_no,
                    "Booked",
                    "Not Requested",
                    "Successful"
                )
            )

            conn.commit()

            cursor.close()

            st.session_state.booking_success = True

            st.session_state.booking_price = price

            st.rerun()

    # =====================================================
    # TICKET HISTORY
    # =====================================================

    with tab2:

        st.subheader("Ticket History")

        if bookings.empty:

            st.warning("No tickets found.")

        else:

            for index, row in bookings.iterrows():

                passenger = str(row.get("passenger_name", "N/A"))
                source_city = str(row.get("source", "N/A"))
                destination_city = str(row.get("destination", "N/A"))
                seat = str(row.get("seat_no", "N/A"))
                journey = str(row.get("journey_date", "N/A"))
                status = str(row.get("status", "Booked"))
                refund = str(row.get("refund_status", "Not Requested"))

                st.markdown("---")

                st.markdown(
                    f"""
                    ### Flight Ticket

                    **Passenger:** {passenger}

                    **Source:** {source_city}

                    **Destination:** {destination_city}

                    **Seat Number:** {seat}

                    **Journey Date:** {journey}

                    **Status:** {status}

                    **Refund Status:** {refund}
                    """
                )

                pdf = FPDF()
                pdf.add_page()
                pdf.set_margins(15, 15, 15)

                # ==================== HEADER ====================
                pdf.set_fill_color(0, 102, 204)
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Arial", "B", 26)
                pdf.cell(0, 16, txt="AIRLINE TICKET", ln=1, align="C", fill=True)
                
                # ==================== TICKET NUMBER ====================
                pdf.set_text_color(100, 100, 100)
                pdf.set_font("Arial", "I", 9)
                pdf.cell(0, 6, txt=f"Booking Reference: TKT-{index:05d}-{seat}", ln=1, align="C")
                pdf.ln(3)

                # ==================== TABLE START ====================
                pdf.set_draw_color(0, 102, 204)
                pdf.set_line_width(1)
                
                # Set column widths
                col1_width = 95
                col2_width = 95
                row_height = 10

                # ==================== ROW 1: PASSENGER & SEAT ====================
                pdf.set_font("Arial", "B", 11)
                pdf.set_text_color(0, 102, 204)
                pdf.set_fill_color(240, 248, 255)
                pdf.cell(col1_width, row_height, txt="PASSENGER NAME", border=1, align="C", fill=True)
                pdf.cell(col2_width, row_height, txt="SEAT NUMBER", border=1, align="C", fill=True, ln=1)

                pdf.set_font("Arial", "B", 11)
                pdf.set_text_color(0, 0, 0)
                pdf.set_fill_color(255, 255, 255)
                pdf.cell(col1_width, row_height, txt=passenger[:25], border=1, align="C")
                pdf.cell(col2_width, row_height, txt=seat, border=1, align="C", ln=1)
                
                pdf.ln(1)

                # ==================== ROW 2: FROM & TO ====================
                pdf.set_font("Arial", "B", 11)
                pdf.set_text_color(0, 102, 204)
                pdf.set_fill_color(240, 248, 255)
                pdf.cell(col1_width, row_height, txt="FROM", border=1, align="C", fill=True)
                pdf.cell(col2_width, row_height, txt="TO", border=1, align="C", fill=True, ln=1)

                pdf.set_font("Arial", "B", 11)
                pdf.set_text_color(0, 0, 0)
                pdf.set_fill_color(255, 255, 255)
                pdf.cell(col1_width, row_height, txt=source_city, border=1, align="C")
                pdf.cell(col2_width, row_height, txt=destination_city, border=1, align="C", ln=1)
                
                pdf.ln(1)

                # ==================== ROW 3: DATE & STATUS ====================
                pdf.set_font("Arial", "B", 11)
                pdf.set_text_color(0, 102, 204)
                pdf.set_fill_color(240, 248, 255)
                pdf.cell(col1_width, row_height, txt="JOURNEY DATE", border=1, align="C", fill=True)
                pdf.cell(col2_width, row_height, txt="BOOKING STATUS", border=1, align="C", fill=True, ln=1)

                pdf.set_font("Arial", "B", 11)
                status_color = (0, 153, 0) if status == "Booked" else (204, 102, 0)
                pdf.set_fill_color(255, 255, 255)
                pdf.set_text_color(0, 0, 0)
                pdf.cell(col1_width, row_height, txt=journey, border=1, align="C")
                pdf.set_text_color(*status_color)
                pdf.cell(col2_width, row_height, txt=status, border=1, align="C", ln=1)
                
                pdf.ln(1)

                # ==================== ROW 4: REFUND STATUS ====================
                pdf.set_font("Arial", "B", 11)
                pdf.set_text_color(0, 102, 204)
                pdf.set_fill_color(240, 248, 255)
                pdf.cell(0, row_height, txt="REFUND STATUS", border=1, align="C", fill=True, ln=1)

                pdf.set_font("Arial", "B", 11)
                pdf.set_text_color(0, 0, 0)
                pdf.set_fill_color(255, 255, 255)
                pdf.cell(0, row_height, txt=refund, border=1, align="C", ln=1)

                pdf.ln(4)

                # ==================== FOOTER ====================
                pdf.set_font("Arial", "I", 8)
                pdf.set_text_color(100, 100, 100)
                pdf.cell(0, 5, txt="Thank you for your booking! Safe travels and a pleasant journey.", ln=1, align="C")
                pdf.cell(0, 4, txt=f"Issued: {pd.Timestamp.now().strftime('%d-%b-%Y | %H:%M:%S')}", ln=1, align="C")
                pdf.ln(2)
                pdf.set_font("Arial", "B", 8)
                pdf.set_text_color(0, 102, 204)
                pdf.cell(0, 5, txt="Keep this ticket safe for check-in", ln=1, align="C")

                pdf_file = f"ticket_{index}.pdf"

                pdf.output(pdf_file)

                with open(pdf_file, "rb") as file:

                    st.download_button(

                        label="Download Ticket PDF",

                        data=file,

                        file_name=pdf_file,

                        mime="application/pdf",

                        key=f"download_pdf_{index}"
                    )

                if os.path.exists(pdf_file):

                    os.remove(pdf_file)

    with tab3:

        st.subheader("Payment Status")

        conn = get_connection()

        payment_df = pd.read_sql(
            """
            SELECT
                id,
                passenger_name,
                source,
                destination,
                payment_status
            FROM bookings
            WHERE user_email=?
            """,
            conn,
            params=(email,)
        )

        conn.close()

        st.dataframe(
            payment_df,
            use_container_width=True
        )

    # =====================================================
    # CANCEL TICKET
    # =====================================================

    with tab4:

        st.subheader("Cancel Ticket")

        if bookings.empty:

            st.warning("No bookings available.")

        else:

            booking_id = st.selectbox(
                "Select Booking ID",
                bookings["id"],
                key="cancel_booking_id"
            )

            cancel_reason = st.text_area(
                "Reason For Cancellation"
            )

            if st.button(
                "Cancel Selected Ticket",
                use_container_width=True
            ):

                cursor = conn.cursor()

                cursor.execute(
                    """
                    UPDATE bookings
                    SET status='Cancelled'
                    WHERE id=?
                    """,
                    (booking_id,)
                )

                conn.commit()

                cursor.close()

                st.success(
                    f"""
                    Ticket Cancelled Successfully

                    Reason:
                    {cancel_reason}
                    """
                )

                st.rerun()

    # =====================================================
    # REFUND REQUEST
    # =====================================================

    with tab5:

        st.subheader("Refund Request")

        if bookings.empty:

            st.warning("No bookings available.")

        else:

            refund_id = st.selectbox(
                "Select Booking ID",
                bookings["id"],
                key="refund_booking_id"
            )

            refund_reason = st.text_area(
                "Refund Reason"
            )

            if st.button(
                "Submit Refund Request",
                use_container_width=True
            ):

                cursor = conn.cursor()

                cursor.execute(
                    """
                    UPDATE bookings
                    SET refund_status='Requested'
                    WHERE id=?
                    """,
                    (refund_id,)
                )

                conn.commit()

                cursor.close()

                st.success(
                    f"""
                    Refund Request Submitted

                    Reason:
                    {refund_reason}
                    """
                )

                st.rerun()

    # =====================================================
    # FEEDBACK
    # =====================================================

    with tab6:

        st.subheader("Customer Feedback")

        feedback = st.text_area(
            "Write Your Feedback"
        )

        rating = st.slider(
            "Rating",
            1,
            5,
            5
        )

        if st.button(
            "Submit Feedback",
            use_container_width=True
        ):

            if not feedback.strip():

                st.error(
                    "Please write your feedback before submitting."
                )

                return

            feedback_conn = get_connection()

            cursor = feedback_conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS feedback_reports (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    customer_email TEXT,

                    feedback TEXT NOT NULL,

                    rating INTEGER NOT NULL,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            cursor.execute(
                """
                INSERT INTO feedback_reports
                (
                    customer_email,
                    feedback,
                    rating
                )
                VALUES (?, ?, ?)
                """,
                (
                    email,
                    feedback.strip(),
                    rating
                )
            )

            feedback_conn.commit()

            feedback_conn.close()

            st.success(
                "Thank You For Your Feedback!"
            )

    conn.close()
