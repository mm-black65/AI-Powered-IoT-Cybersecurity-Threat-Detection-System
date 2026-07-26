import streamlit as st
from streamlit_autorefresh import st_autorefresh

from dashboard_data import load_data, require_device_data, render_status_bar

st.set_page_config(page_title="Live Telemetry", page_icon="📡", layout="wide")
st_autorefresh(interval=5000, key="telemetry_refresh")

st.title("📡 Live Device Telemetry")
render_status_bar()

device_df, _ = load_data()
require_device_data(device_df)

# Charts are stored newest-first (id DESC); reverse so time runs left -> right
chart_df = device_df.iloc[::-1]

st.header("📈 Live Device Statistics")

left, right = st.columns(2)

with left:
    st.subheader("🌡 Temperature")
    st.line_chart(chart_df["temperature"])

    st.subheader("📶 WiFi Signal")
    st.line_chart(chart_df["wifi_signal"])

with right:
    st.subheader("💻 CPU Usage")
    st.line_chart(chart_df["cpu_usage"])

    st.subheader("📦 Packet Rate")
    st.line_chart(chart_df["packet_rate"])

if "humidity" in device_df.columns and device_df["humidity"].notna().any():
    st.subheader("💧 Humidity")
    st.line_chart(chart_df["humidity"])

st.divider()

st.header("📄 Device Telemetry History")
st.dataframe(device_df, use_container_width=True, hide_index=True)