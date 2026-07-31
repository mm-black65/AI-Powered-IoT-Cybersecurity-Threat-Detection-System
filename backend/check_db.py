import sqlite3
import os

db_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "iot_security.db"
)

db_path = os.path.abspath(db_path)

print("Using:", db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(predictions)")

print("\nPredictions table columns:\n")
for col in cursor.fetchall():
    print(col)

conn.close()