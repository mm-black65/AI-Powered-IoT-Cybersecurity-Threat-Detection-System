import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from dashboard_data import (
    load_data,
    require_device_data,
    render_status_bar,
    threat_counts,
)

st.set_page_config(
    page_title="AI IoT Cybersecurity",
    page_icon="🛡️",
    layout="wide"
)

st_autorefresh(interval=5000, key="home_refresh")

# -----------------------------
# Title / status
# -----------------------------

st.title("🛡️ AI-Based IoT Cybersecurity Threat Detection System")
render_status_bar("Machine Learning + RAG + LLM Powered IoT Security Dashboard")

col1, _ = st.columns([1, 6])
with col1:
    if st.button("🔄 Refresh"):
        st.rerun()

# -----------------------------
# Data
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
c2.metric("🔴 HIGH", high_count)
c3.metric("🟡 MEDIUM", medium_count)
c4.metric("🟢 LOW", low_count)

st.divider()

# -----------------------------
# Latest Telemetry Snapshot
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
# Latest Prediction
# -----------------------------

if not prediction_df.empty:
    latest_prediction = prediction_df.iloc[0]

    st.header("🚨 Latest Threat Detection")

    p1, p2, p3 = st.columns(3)
    p1.metric("Prediction", latest_prediction["prediction"])
    p2.metric("Confidence", f"{latest_prediction['confidence']} %")

    if latest_prediction["threat_level"] == "HIGH":
        p3.error("🔴 HIGH")
    elif latest_prediction["threat_level"] == "MEDIUM":
        p3.warning("🟡 MEDIUM")
    else:
        p3.success("🟢 LOW")
else:
    st.info("No predictions yet — open **AI Threat Detection** in the sidebar to generate one.")

st.divider()

# -----------------------------
# Navigation
# -----------------------------

st.subheader("🧭 Explore the dashboard")
n1, n2, n3 = st.columns(3)
with n1:
    st.page_link("pages/1_📡_Live_Telemetry.py", label="Live Telemetry", icon="📡")
with n2:
    st.page_link("pages/2_🤖_AI_Threat_Detection.py", label="AI Threat Detection", icon="🤖")
with n3:
    st.page_link("pages/3_📉_Trends_and_History.py", label="Trends & History", icon="📉")