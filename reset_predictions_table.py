import sqlite3

conn = sqlite3.connect("iot_security.db")
cursor = conn.cursor()

# Delete the old predictions table
cursor.execute("DROP TABLE IF EXISTS predictions")

# Create the new predictions table
cursor.execute("""
CREATE TABLE predictions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction TEXT,
    confidence REAL,
    threat_level TEXT,
    rag_information TEXT,
    ai_analysis TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("✅ Predictions table recreated successfully!")