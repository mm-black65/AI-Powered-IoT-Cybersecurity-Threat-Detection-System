import json
import sqlite3
import requests
import paho.mqtt.client as mqtt

from backend.feature_mapper import telemetry_to_ml_features

# ==========================================================
# Configuration
# ==========================================================

BROKER = "localhost"
PORT = 1883

TELEMETRY_TOPIC = "iot/device01/telemetry"
ALERT_TOPIC = "iot/device01/alert"

FASTAPI_URL = "http://127.0.0.1:8000/predict-threat"
DB_PATH = "iot_security.db"

# ==========================================================
# Database Setup
# ==========================================================

def init_db():
    """Create tables if they don't already exist. Safe to call every run."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS device_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            cpu_usage REAL,
            wifi_signal REAL,
            packet_rate REAL,
            failed_login INTEGER,
            heap REAL,
            uptime INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
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
    print(f"Database ready: {DB_PATH}")


def save_telemetry(telemetry: dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO device_data
        (temperature, humidity, cpu_usage, wifi_signal, packet_rate, failed_login, heap, uptime)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        telemetry.get("temperature"),
        telemetry.get("humidity"),
        telemetry.get("cpu_usage"),
        telemetry.get("wifi_signal"),
        telemetry.get("packet_rate"),
        telemetry.get("failed_login"),
        telemetry.get("heap"),
        telemetry.get("uptime"),
    ))
    conn.commit()
    conn.close()


def save_prediction(prediction: str, confidence: float, threat_level: str, rag_information: str = "", ai_analysis: str = ""):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO predictions (prediction, confidence, threat_level, rag_information, ai_analysis)
        VALUES (?, ?, ?, ?, ?)
    """, (prediction, confidence, threat_level, rag_information, ai_analysis))
    conn.commit()
    conn.close()


# ==========================================================
# MQTT Callbacks
# ==========================================================

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("\n==========================================")
        print("Connected to Mosquitto Broker")
        print("==========================================")

        client.subscribe(TELEMETRY_TOPIC)
        print(f"Subscribed : {TELEMETRY_TOPIC}")
        print("Waiting for ESP32 Telemetry...\n")
    else:
        print("MQTT Connection Failed:", reason_code)


def on_message(client, userdata, msg):
    try:
        telemetry = json.loads(msg.payload.decode())

        print("\n==========================================")
        print("ESP32 TELEMETRY RECEIVED")
        print("==========================================")
        print(json.dumps(telemetry, indent=4))

        # --------------------------------------------------
        # Save raw telemetry to DB (so dashboard has live data
        # even before a prediction is generated)
        # --------------------------------------------------
        save_telemetry(telemetry)

        # --------------------------------------------------
        # Convert ESP32 telemetry to ML Features
        # --------------------------------------------------
        model_features = telemetry_to_ml_features(telemetry)
        print("\nFeatures mapped successfully.")

        # --------------------------------------------------
        # Call FastAPI Prediction API
        # --------------------------------------------------
        response = requests.post(FASTAPI_URL, json=model_features, timeout=20)

        if response.status_code != 200:
            print("\nPrediction API Failed")
            print(response.text)
            return

        result = response.json()

        print("\n==========================================")
        print("AI PREDICTION")
        print("==========================================")
        print("Prediction   :", result["prediction"])
        print("Confidence   :", result["confidence"], "%")
        print("Threat Level :", result["threat_level"])

        # --------------------------------------------------
        # Save prediction to DB
        # --------------------------------------------------
        save_prediction(
            result["prediction"],
            result["confidence"],
            result["threat_level"],
            result.get("rag_information", ""),
            result.get("ai_analysis", ""),
        )
        if "rag_information" in result:
            print("\nRAG INFORMATION")
            print("------------------------------------------")
            print(result["rag_information"])

        if "ai_analysis" in result:
            print("\nAI SECURITY ANALYSIS")
            print("------------------------------------------")
            print(result["ai_analysis"])

        # --------------------------------------------------
        # Publish Alert back to ESP32
        # --------------------------------------------------
        alert = "ATTACK" if result["threat_level"] in ["HIGH", "MEDIUM"] else "SAFE"
        client.publish(ALERT_TOPIC, alert)
        print("\nPublished Alert :", alert)
        print("==========================================\n")

    except requests.exceptions.RequestException as e:
        print("\nCould not reach FastAPI backend. Is it running on port 8000?")
        print(e)

    except Exception as e:
        print("\nMQTT Processing Error")
        print(e)


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    print("\nDisconnected from MQTT Broker. Will retry automatically...")


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":
    init_db()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    print("Connecting to Mosquitto...")
    client.connect(BROKER, PORT)

    client.loop_forever()