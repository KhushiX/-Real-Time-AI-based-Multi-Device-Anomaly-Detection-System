import requests
import sqlite3
import time

API_URL = "http://192.168.149.182:8000/api/unified-activity-data/"

conn = sqlite3.connect("database/sensor_data.db", check_same_thread=False)
cursor = conn.cursor()

print("🔗 Fetching REAL unified backend data...")

def bool_to_int(value):
    if value is True:
        return 1
    else:
        return 0

while True:
    try:
        response = requests.get(API_URL, timeout=5)
        data_list = response.json()  # API returns a list

        for data in data_list:  # iterate over each device
            cursor.execute("""
            INSERT INTO device_activity_logs VALUES
            (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get("device_id"),
                data.get("device_type"),

                data.get("accel_level"),
                data.get("bluetooth_state"),
                data.get("screen_state"),
                bool_to_int(data.get("input_activity")),
                data.get("activity_duration_sec"),
                data.get("event_frequency"),

                bool_to_int(data.get("file_transfer")),
                data.get("data_transfer_mb"),

                data.get("heart_rate"),
                data.get("battery_level"),

                data.get("timestamp")
            ))

            conn.commit()
            print(f"✅ Inserted {data.get('device_type')} data")

    except Exception as e:
        print("⚠️ Error fetching data:", e)

    time.sleep(2)
