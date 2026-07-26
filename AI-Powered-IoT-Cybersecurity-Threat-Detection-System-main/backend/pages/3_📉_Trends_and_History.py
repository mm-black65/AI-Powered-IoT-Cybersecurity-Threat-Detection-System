import streamlit as st

from dashboard_data import load_data, render_status_bar

st.set_page_config(page_title="Trends & History", page_icon="📉", layout="wide")

st.title("📉 Threat Trends & History")
render_status_bar()

device_df, prediction_df = load_data()

# -----------------------------
# Threat Trends
# -----------------------------

st.header("Threat Trends")

if not prediction_df.empty:
    trend_col1, trend_col2 = st.columns(2)

    with trend_col1:
        st.subheader("Threat Level Distribution")
        st.bar_chart(prediction_df["threat_level"].value_counts())

    with trend_col2:
        st.subheader("Confidence Over Time")
        # reverse so it plots oldest -> newest, left to right
        st.line_chart(prediction_df["confidence"][::-1])

    st.subheader("🕑 Last 20 Predictions")
    st.dataframe(
        prediction_df[["id", "prediction", "confidence", "threat_level"]].head(20),
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No predictions yet — trigger an attack or generate a report to populate this section.")

st.divider()

# -----------------------------
# Full History
# -----------------------------

st.header("📄 Full History")

tab1, tab2 = st.tabs(["Device Telemetry", "Threat Predictions"])

with tab1:
    if device_df.empty:
        st.info("No device telemetry recorded yet.")
    else:
        st.dataframe(device_df, use_container_width=True, hide_index=True)

with tab2:
    if prediction_df.empty:
        st.info("No predictions recorded yet.")
    else:
        st.dataframe(prediction_df, use_container_width=True, hide_index=True)