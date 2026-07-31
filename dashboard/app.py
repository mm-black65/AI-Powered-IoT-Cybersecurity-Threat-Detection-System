import sqlite3
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from dashboard_data import (
    DB_PATH,
    load_data,
    require_device_data,
    render_status_bar,
    threat_counts,
)

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI IoT Cybersecurity",
    page_icon="🛡️",
    layout="wide",
)

st_autorefresh(interval=5000, key="home_refresh")

# -----------------------------
# Title
# -----------------------------

st.title("🛡️ AI-Based IoT Cybersecurity Threat Detection System")
render_status_bar("Machine Learning + RAG + LLM Powered IoT Security Dashboard")

col1, _ = st.columns([1, 6])
with col1:
    if st.button("🔄 Refresh"):
        st.rerun()

# -----------------------------
# Load Data
# -----------------------------

device_df, prediction_df = load_data()
require_device_data(device_df)

latest = device_df.iloc[0]

# -----------------------------
# Threat Statistics
# -----------------------------

st.header("📊 Threat Statistics")

total_predictions, high_count, medium_count, low_count = threat_counts(prediction_df)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Predictions", total_predictions)
c2.metric("🔴 HIGH Threats", high_count)
c3.metric("🟡 MEDIUM Threats", medium_count)
c4.metric("🟢 LOW Threats", low_count)

st.divider()

# -----------------------------
# Latest Device Telemetry
# -----------------------------

st.header("📡 Latest Device Telemetry")

a, b, c = st.columns(3)

a.metric("🌡 Temperature", f"{latest['temperature']} °C")
b.metric("💻 CPU Usage", f"{latest['cpu_usage']} %")
c.metric("📶 WiFi Signal", f"{latest['wifi_signal']} dBm")

d, e, f = st.columns(3)

d.metric("📦 Packet Rate", int(latest["packet_rate"]))
e.metric("🔐 Failed Login", int(latest["failed_login"]))

if "humidity" in latest.index and pd.notna(latest["humidity"]):
    f.metric("💧 Humidity", f"{latest['humidity']} %")

st.divider()

# -----------------------------
# AI Security Report
# -----------------------------

st.header("🛡️ AI Security Report")

prediction = None
confidence = None
threat_level = None
rag_information = ""
ai_analysis = ""

try:
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            """
            SELECT
                prediction,
                confidence,
                threat_level,
                rag_information,
                ai_analysis
            FROM predictions
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()

    if row:
        (
            prediction,
            confidence,
            threat_level,
            rag_information,
            ai_analysis,
        ) = row

        with st.expander("📚 Knowledge Base Context (RAG)", expanded=True):
            if rag_information:
                st.text(rag_information)
            else:
                st.info("No RAG information available.")

        with st.expander("🤖 Gemini Security Analysis", expanded=True):
            if ai_analysis:
                st.markdown(ai_analysis)
            else:
                st.info("No AI analysis available.")

    else:
        st.info("No AI security report available.")

except sqlite3.OperationalError as e:
    st.error(f"Database Error: {e}")
except Exception as e:
    st.error(f"Unexpected Error: {e}")

st.divider()

# -----------------------------
# Latest Threat Detection
# -----------------------------

st.header("🚨 Latest Threat Detection")

if not prediction_df.empty:

    latest_prediction = prediction_df.iloc[0]

    p1, p2, p3 = st.columns(3)

    p1.metric("Prediction", latest_prediction["prediction"])
    p2.metric("Confidence", f"{latest_prediction['confidence']} %")

    level = str(latest_prediction["threat_level"]).upper()

    if level == "HIGH":
        p3.error("🔴 HIGH")
    elif level == "MEDIUM":
        p3.warning("🟡 MEDIUM")
    else:
        p3.success("🟢 LOW")

else:
    st.info(
        "No predictions yet.\n\nGo to **AI Threat Detection** from the sidebar to generate one."
    )

st.divider()

# -----------------------------
# Recent Predictions
# -----------------------------

st.header("📋 Recent Predictions")

if not prediction_df.empty:

    display_columns = [
        col
        for col in [
            "timestamp",
            "prediction",
            "confidence",
            "threat_level",
        ]
        if col in prediction_df.columns
    ]

    st.dataframe(
        prediction_df[display_columns],
        use_container_width=True,
        hide_index=True,
    )

else:
    st.info("No prediction history available.")
