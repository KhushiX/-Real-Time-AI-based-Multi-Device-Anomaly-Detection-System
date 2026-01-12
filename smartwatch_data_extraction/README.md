# Smartwatch Module (BLE Data Extraction)

This folder contains all the code related to **smartwatch data extraction using Bluetooth Low Energy (BLE)** and **real-time data transmission to a remote backend via REST API**.  
The module is designed to be independent, modular, and easily integrable with larger multi-device or AI-based systems.

---

## 📁 Files Overview

### 1. `scan.py`
This file is responsible for **discovering nearby BLE devices**.

**Key responsibilities:**
- Scans for nearby BLE-enabled devices
- Displays device name and MAC address
- Enables dynamic device selection instead of hardcoded addresses

This ensures flexibility when working with multiple smartwatches or BLE devices.

---

### 2. `ble_services.py`
This file defines and manages **BLE service and characteristic details** used by the smartwatch.

**Key responsibilities:**
- Stores standard BLE UUIDs such as:
  - Heart Rate Measurement (0x2A37)
  - Battery Level (0x2A19)
- Acts as a central reference for BLE services
- Improves readability and maintainability of the BLE code

Separating BLE services into this file avoids duplication and simplifies updates.

---

### 3. `stream.py`
This is the **core logic file** of the smartwatch module.

**Key responsibilities:**
- Connects to the selected smartwatch using its MAC address
- Subscribes to heart rate notifications (real-time data)
- Periodically reads battery percentage
- Decodes raw BLE data into meaningful values
- Sends processed data to a remote backend using a REST API

Each data payload includes:
- Device ID (MAC address)
- Device type (default: `watch`)
- Heart rate value
- Battery percentage
- Timestamp

This enables real-time, network-based data sharing with a backend system.

---

## 🔁 Data Flow Summary

1. BLE devices are scanned using `scan.py`
2. User selects the target smartwatch
3. BLE services and UUIDs are referenced from `ble_services.py`
4. Real-time heart rate and battery data are extracted in `stream.py`
5. Data is transmitted to a backend REST API for storage and analysis

---

## 🧠 Design Highlights

- Modular file structure for clarity and scalability
- No hardcoded device dependencies
- Low-power BLE communication
- Backend-agnostic REST API integration
- Suitable for real-time health monitoring and anomaly detection systems

---

## 🚀 Use Case

This module is designed for:
- Smartwatch-based health monitoring
- IoT data collection systems
- Real-time sensor data pipelines
- Integration with AI/ML-based anomaly detection backends

---


