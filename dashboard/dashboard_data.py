import sqlite3
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

DB_PATH = "iot_security.db"
BACKEND_URL = "http://127.0.0.1:8000"


@st.cache_data(ttl=4)
def load_data():
    """Load device telemetry + prediction tables.

    Cached for a few seconds so multiple widgets/pages don't hit the
    database repeatedly on every rerun. TTL is shorter than the
    autorefresh interval, so data still stays effectively live.
    """
    conn = sqlite3.connect(DB_PATH)

    try:
        device_df = pd.read_sql_query(
            "SELECT * FROM device_data ORDER BY id DESC", conn
        )
    except Exception:
        device_df = pd.DataFrame()

    try:
        prediction_df = pd.read_sql_query(
            "SELECT * FROM predictions ORDER BY id DESC", conn
        )
    except Exception:
        prediction_df = pd.DataFrame()

    conn.close()
    return device_df, prediction_df


def check_backend():
    """Return (is_up: bool, message: str) for the FastAPI backend."""
    try:
        response = requests.get(BACKEND_URL + "/", timeout=2)
        if response.status_code == 200:
            return True, "🟢 Backend Connected"
        return False, "🔴 Backend Error"
    except Exception:
        return False, "🔴 Backend Offline"


def require_device_data(device_df):
    """Show the standard 'no telemetry yet' warning and halt the page.

    Single source of truth for this check so it isn't re-implemented
    (and drifts) on every page.
    """
    if device_df.empty:
        st.warning(
            "No telemetry tables found yet. Make sure the MQTT backend "
            "(mqtt.py) has run at least once to create 'iot_security.db'."
        )
        st.stop()


def render_status_bar(caption=None):
    """Backend connection badge + last-updated timestamp, shared by every page."""
    is_up, message = check_backend()
    if is_up:
        st.success(message)
    else:
        st.error(message)
    st.caption(f"Last Updated : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    if caption:
        st.caption(caption)


def threat_counts(prediction_df):
    """Return (total, high, medium, low) counts, safe on an empty df."""
    if prediction_df.empty:
        return 0, 0, 0, 0
    total = len(prediction_df)
    high = len(prediction_df[prediction_df["threat_level"] == "HIGH"])
    medium = len(prediction_df[prediction_df["threat_level"] == "MEDIUM"])
    low = len(prediction_df[prediction_df["threat_level"] == "LOW"])
    return total, high, medium, low