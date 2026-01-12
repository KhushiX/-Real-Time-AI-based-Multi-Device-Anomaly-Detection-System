import streamlit as st
import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest
import time

# =========================
# STREAMLIT CONFIG
# =========================
st.set_page_config(
    page_title="AI Activity Anomaly Detection",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Unified AI Activity Anomaly Detection Dashboard")
st.markdown("""
This dashboard shows **real-time activity and anomaly detection** for Laptop, Mobile, and Smartwatch devices.
Data is fetched from a **live backend API** and processed by an AI model.
""")

# =========================
# LOAD DATA FROM DB
# =========================
@st.cache_data(ttl=5)
def load_data():
    conn = sqlite3.connect("database/sensor_data.db")
    df = pd.read_sql("SELECT * FROM device_activity_logs ORDER BY timestamp DESC", conn)
    conn.close()
    return df

df = load_data()

if df.empty:
    st.warning("⏳ Waiting for data... Please make sure `fetch_live_backend_data.py` is running.")
    st.stop()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")
device_filter = st.sidebar.multiselect(
    "Select Device Type",
    options=df["device_type"].unique(),
    default=df["device_type"].unique()
)

# Filter dataframe
df_filtered = df[df["device_type"].isin(device_filter)]

# =========================
# FEATURE ENGINEERING
# =========================
def prepare_features(df):
    df = df.copy()
    df["bluetooth_on"] = df["bluetooth_state"].map({"ON":1,"OFF":0}).fillna(0)
    df["screen_on"] = df["screen_state"].map({"ON":1,"OFF":0}).fillna(0)
    df["accel_val"] = df["accel_level"].map({"LOW":1,"MED":2,"HIGH":3}).fillna(0)
    df["input_activity"] = df["input_activity"].fillna(0)
    df["activity_duration_sec"] = df["activity_duration_sec"].fillna(0)
    df["event_frequency"] = df["event_frequency"].fillna(0)
    df["file_transfer"] = df["file_transfer"].fillna(0)
    df["data_transfer_mb"] = df["data_transfer_mb"].fillna(0)
    df["heart_rate"] = df["heart_rate"].fillna(0)
    df["battery_level"] = df["battery_level"].fillna(0)

    features = [
        "bluetooth_on",
        "screen_on",
        "accel_val",
        "input_activity",
        "activity_duration_sec",
        "event_frequency",
        "file_transfer",
        "data_transfer_mb",
        "heart_rate",
        "battery_level"
    ]
    return df[features]

# =========================
# TRAIN MODEL ON LIVE DATA
# =========================
X_train = prepare_features(df_filtered)
model = IsolationForest(n_estimators=100, contamination=0.08, random_state=42)
model.fit(X_train)

# =========================
# LIVE MONITORING DISPLAY
# =========================
st.subheader("🔴 Live Activity Monitoring")

placeholder = st.empty()

for i in range(len(df_filtered)):
    current_df = df_filtered.iloc[:i+1]
    X_live = prepare_features(current_df)
    pred = model.predict(X_live.iloc[-1:])[0]

    row = current_df.iloc[-1]
    status = "🟢 NORMAL" if pred == 1 else "🔴 ANOMALY"

    with placeholder.container():
        # ------------------
        # Metrics Row
        # ------------------
        col1, col2, col3, col4 = st.columns([2,2,2,2])
        col1.metric("Device Type", row["device_type"])
        col2.metric("Device ID", row["device_id"])
        col3.metric("Status", status)
        col4.metric("Battery Level", row["battery_level"])

        # ------------------
        # Details Table
        # ------------------
        st.markdown("### 🔹 Recent Activity Logs")
        st.dataframe(current_df.tail(5), use_container_width=True)

        # ------------------
        # Highlight Anomalies
        # ------------------
        if pred == -1:
            st.warning(f"⚠️ Anomaly detected on {row['device_type']} ({row['device_id']})!")
        else:
            st.success(f"✅ {row['device_type']} is normal.")

    time.sleep(1)

# =========================
# OPTIONAL: DOWNLOAD DATA
# =========================
st.sidebar.header("Download Data")
if st.sidebar.button("Download CSV of Filtered Data"):
    csv = df_filtered.to_csv(index=False)
    st.sidebar.download_button("Download CSV", data=csv, file_name="filtered_activity_data.csv", mime="text/csv")
