import requests
import streamlit as st

from dashboard_data import render_status_bar

st.set_page_config(page_title="AI Threat Detection", page_icon="🤖", layout="wide")

st.title("🤖 AI Threat Detection")
render_status_bar()

st.caption(
    "Simulates a network flow, sends it to the FastAPI + ML backend, and "
    "shows the model's prediction alongside RAG-retrieved context and an "
    "LLM-written analysis."
)

default_sample = {
    "flow_duration": 0,
    "Header_Length": 54,
    "Protocol Type": 6,
    "Duration": 64,
    "Rate": 250,
    "Srate": 250,
    "fin_flag_number": 0,
    "syn_flag_number": 1,
    "rst_flag_number": 0,
    "psh_flag_number": 0,
    "ack_flag_number": 1,
    "ack_count": 1,
    "syn_count": 1,
    "fin_count": 0,
    "urg_count": 0,
    "rst_count": 0,
    "HTTP": 0,
    "HTTPS": 0,
    "DNS": 0,
    "TCP": 1,
    "UDP": 0,
    "ARP": 0,
    "ICMP": 0,
    "IPv": 1,
    "LLC": 1,
    "Tot sum": 120,
    "Min": 60,
    "Max": 60,
    "AVG": 60,
    "Std": 0,
    "Tot size": 120,
    "IAT": 0,
    "Number": 2,
    "Magnitue": 60,
    "Radius": 0,
    "Covariance": 0,
    "Variance": 0,
    "Weight": 141.55,
}

st.subheader("⚙️ Simulated Flow Parameters")
st.caption("Tweak a few key fields to simulate different traffic patterns, or leave the defaults.")

sample = dict(default_sample)

col1, col2, col3 = st.columns(3)
with col1:
    sample["Rate"] = st.number_input("Rate", value=default_sample["Rate"])
    sample["Srate"] = st.number_input("Srate (send rate)", value=default_sample["Srate"])
    sample["syn_flag_number"] = st.selectbox(
        "SYN Flag", [0, 1], index=default_sample["syn_flag_number"]
    )
with col2:
    sample["ack_flag_number"] = st.selectbox(
        "ACK Flag", [0, 1], index=default_sample["ack_flag_number"]
    )
    sample["TCP"] = st.selectbox("TCP", [0, 1], index=default_sample["TCP"])
    sample["UDP"] = st.selectbox("UDP", [0, 1], index=default_sample["UDP"])
with col3:
    sample["Tot size"] = st.number_input("Total Size", value=default_sample["Tot size"])
    sample["Weight"] = st.number_input("Weight", value=float(default_sample["Weight"]))
    sample["Number"] = st.number_input("Number", value=default_sample["Number"])

with st.expander("🔧 Show all raw flow fields sent to the model"):
    st.json(sample)

st.divider()

if st.button("🚀 Generate AI Security Report", type="primary"):
    with st.spinner("Running AI Security Analysis..."):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/predict-threat",
                json=sample,
                timeout=20,
            )

            if response.status_code == 200:
                result = response.json()
                st.success("Analysis Completed Successfully")

                left, right = st.columns(2)

                with left:
                    st.subheader("🎯 Prediction")
                    st.info(result["prediction"])

                    st.subheader("📊 Confidence")
                    st.progress(result["confidence"] / 100)
                    st.write(f"**{result['confidence']} %**")

                    st.subheader("⚠ Threat Level")
                    if result["threat_level"] == "HIGH":
                        st.error(result["threat_level"])
                    elif result["threat_level"] == "MEDIUM":
                        st.warning(result["threat_level"])
                    else:
                        st.success(result["threat_level"])

                with right:
                    st.subheader("📚 RAG Knowledge Base")
                    st.info(result["rag_information"])

                st.divider()
                st.subheader("🤖 AI Security Analysis")
                st.markdown(result["ai_analysis"])

            else:
                st.error("Backend returned an error.")
                st.code(response.text)

        except Exception as e:
            st.error("Unable to connect to FastAPI backend.")
            st.exception(e)