import sqlite3
import os

DATABASE_NAME = "iot_security.db"

def get_connection():
    print("Using database:", os.path.abspath(DATABASE_NAME))
    return sqlite3.connect(DATABASE_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS device_data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        temperature REAL,
        humidity REAL,
        cpu_usage REAL,
        packet_rate INTEGER,
        failed_login INTEGER,
        wifi_signal INTEGER,
        heap REAL,
        uptime REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def create_prediction_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions(
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

def insert_device_data(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO device_data
    (
        device_id,
        temperature,
        humidity,
        cpu_usage,
        packet_rate,
        failed_login,
        wifi_signal,
        heap,
        uptime
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        getattr(data, 'device_id', None),
        getattr(data, 'temperature', None),
        getattr(data, 'humidity', None),
        getattr(data, 'cpu_usage', None),
        getattr(data, 'packet_rate', None),
        getattr(data, 'failed_login', None),
        getattr(data, 'wifi_signal', None),
        getattr(data, 'heap', None),
        getattr(data, 'uptime', None)
    ))

    conn.commit()
    conn.close()


def insert_prediction(
    prediction,
    confidence,
    threat_level,
    rag_information="",
    ai_analysis=""
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions
    (
        prediction,
        confidence,
        threat_level,
        rag_information,
        ai_analysis
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        prediction,
        confidence,
        threat_level,
        rag_information,
        ai_analysis
    ))

    conn.commit()
    conn.close()


def get_latest_device_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        device_id,
        temperature,
        humidity,
        cpu_usage,
        packet_rate,
        failed_login,
        wifi_signal,
        heap,
        uptime
    FROM device_data
    ORDER BY id DESC
    LIMIT 1
    """)

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "device_id": row[0],
        "temperature": row[1],
        "humidity": row[2],
        "cpu_usage": row[3],
        "packet_rate": row[4],
        "failed_login": row[5],
        "wifi_signal": row[6],
        "heap": row[7],
        "uptime": row[8]
    }