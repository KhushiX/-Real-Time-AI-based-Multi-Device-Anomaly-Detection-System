import sqlite3
import random
import time
from datetime import datetime

conn = sqlite3.connect("database/sensor_data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS device_activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT,
    device_type TEXT,

    accel_level TEXT,
    bluetooth_state TEXT,
    screen_state TEXT,
    input_activity INTEGER,
    activity_duration_sec INTEGER,
    event_frequency INTEGER,

    file_transfer INTEGER,
    data_transfer_mb REAL,

    heart_rate INTEGER,
    battery_level INTEGER,

    timestamp DATETIME
)
""")
conn.commit()

def insert_laptop():
    cursor.execute("""
    INSERT INTO device_activity_logs VALUES
    (NULL, ?, 'Laptop',
     NULL, ?, ?, ?, ?, ?,
     ?, ?, NULL, NULL, ?)
    """, (
        "laptop_01",
        random.choice(["ON","OFF"]),
        random.choice(["ON","OFF"]),
        random.choice([0,1]),
        random.randint(60,600),
        random.randint(1,6),
        random.choice([0,1]),
        round(random.uniform(10,1200),2),
        datetime.now()
    ))

def insert_mobile():
    cursor.execute("""
    INSERT INTO device_activity_logs VALUES
    (NULL, ?, 'Mobile',
     ?, ?, ?, ?, ?, ?,
     NULL, NULL, NULL, NULL, ?)
    """, (
        "mobile_01",
        random.choice(["LOW","MED","HIGH"]),
        random.choice(["ON","OFF"]),
        random.choice(["ON","OFF"]),
        random.choice([0,1]),
        random.randint(30,300),
        random.randint(5,25),
        datetime.now()
    ))

def insert_watch():
    cursor.execute("""
    INSERT INTO device_activity_logs VALUES
    (NULL, ?, 'Watch',
     NULL, NULL, NULL, NULL, NULL, NULL,
     NULL, NULL, ?, ?, ?)
    """, (
        "watch_01",
        random.randint(60,160),
        random.randint(20,100),
        datetime.now()
    ))

print("🔴 Unified real-time data generation started...")

while True:
    random.choice([insert_laptop, insert_mobile, insert_watch])()
    conn.commit()
    time.sleep(2)
