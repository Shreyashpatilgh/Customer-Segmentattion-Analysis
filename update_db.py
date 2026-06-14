import sqlite3

conn = sqlite3.connect("customer_segmentation.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT")
except:
    print("phone already exists")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN dob TEXT")
except:
    print("dob already exists")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN address TEXT")
except:
    print("address already exists")

conn.commit()
conn.close()

print("Database updated successfully")