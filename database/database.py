import sqlite3


DB_NAME = "customer_segmentation.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    # ==========================================
    # LOGIN ACTIVITY TABLE
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login_activity (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT NOT NULL,

        login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ==========================================
    # USERS TABLE
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        role TEXT DEFAULT 'customer',

        otp TEXT,

        is_verified INTEGER DEFAULT 0,

        phone TEXT,

        dob TEXT,

        address TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_email TEXT,

        passenger_name TEXT,

        source TEXT,

        destination TEXT,

        journey_date TEXT,

        seat_no TEXT,

        status TEXT,

        refund_status TEXT,
        payment_status TEXT DEFAULT 'Successful',

        booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ==========================================
    # PREDICTIONS TABLE
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        customer_email TEXT,

        prediction_result TEXT,

        confidence REAL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ==========================================
    # CUSTOMER SEGMENTS TABLE
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer_segments (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        customer_email TEXT,

        segment_name TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ==========================================
    # CUSTOMER FEEDBACK REPORTS TABLE
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback_reports (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        customer_email TEXT,

        feedback TEXT NOT NULL,

        rating INTEGER NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    conn.close()
