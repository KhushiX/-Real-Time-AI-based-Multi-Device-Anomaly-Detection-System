# Real-Time AI-Based Multi-Device Anomaly Detection System

## 📌 Project Overview
This project is a **real-time AI-powered anomaly detection system** designed to monitor and analyze behavioral and sensor activity across **multiple devices**, including **laptops, mobile phones, and smartwatches**.

The system uses a **unified backend data ingestion pipeline** where real-time data from different devices is streamed to a central server, stored in a database, and analyzed using **machine learning models** to detect abnormal patterns such as unusual activity frequency, abnormal sensor readings, or suspicious usage behavior.

---

## 🧠 System Architecture (High Level)
- **Data Collection Layer**  
  Laptop, Mobile, and Smartwatch continuously collect device-specific metrics.
- **Backend Layer (Django + REST API)**  
  Acts as a centralized data receiver and validator.
- **AI/ML Layer**  
  Applies unsupervised anomaly detection on aggregated data.
- **Visualization Layer**  
  Displays live metrics, anomalies, and alerts through a dashboard.

---

## 🛠️ Technology Stack
- **Backend:** Python, Django, Django REST Framework  
- **Database:** SQLite (development)  
- **Machine Learning:** Isolation Forest (unsupervised)  
- **Frontend / Dashboard:** Streamlit  
- **Communication:** REST APIs (JSON over HTTP)  
- **Version Control:** Git, GitHub  

---

## ⚙️ Key Features
- Unified real-time data ingestion from multiple devices  
- Centralized backend API for all device types  
- Secure backend configuration using environment variables  
- AI-based anomaly detection on live data  
- Device-level filtering and monitoring  
- Real-time dashboard with alerts and data export  

---

## 📂 Project Structure
Real-Time-AI-based-Multi-Device-Anomaly-Detection-System/
│
├── backend/ # Django project configuration
├── sensorapi/ # Core backend APIs and data models
├── mobile_app/ # Android mobile data collection
├── laptop_agent/ # Laptop activity & system monitoring
├── smartwatch_agent/ # Smartwatch BLE data ingestion
├── ml_model/ # AI/ML anomaly detection logic
├── manage.py
├── README.md
└── .gitignore

---

## 👩‍💻 

### 🔹 **(Backend & System Integration)**
- Designed and implemented the **Django backend** using Django REST Framework  
- Built a **unified REST API** capable of receiving data from all devices  
- Replaced dummy data generators with **real-time streaming data**  
- Designed a **single unified database schema** for multi-device ingestion  
- Implemented backend validation using serializers  
- Integrated backend with **Android, Laptop, and Smartwatch data pipelines**  
- Stored real-time data in SQLite for AI/ML processing  
- Secured backend configuration using environment variables  
- Connected backend with AI model and real-time dashboard  

---

### 🔹 **(Android Development – Mobile Data Collection)**
- Developed an **Android application** to collect real-time behavioral and sensor data  
- Captured:
  - Accelerometer-based activity levels  
  - Gyroscope readings  
  - Screen state  
  - Bluetooth state  
  - User interaction activity  
  - Battery level  
- Aggregated sensor data over fixed time windows  
- Structured data according to a **unified backend schema**  
- Implemented REST-based communication using JSON payloads  
- Verified real-time transmission using Logcat and resolved backend validation issues  

---

### 🔹 **(Laptop Data Collection)**
- Implemented a laptop-based monitoring system  
- Collected:
  - User activity status  
  - Screen state  
  - Network usage  
  - Bluetooth and USB device connections  
  - File transfer activity  
  - Battery percentage  
- Aggregated data periodically with timestamps  
- Sent structured data to backend at fixed intervals for analysis  

---

### 🔹 **(Smartwatch Data Collection)**
- Implemented smartwatch data extraction using **Bluetooth Low Energy (BLE)**  
- Scanned and connected to nearby smartwatches using MAC address  
- Subscribed to heart rate characteristics for real-time notifications  
- Periodically read battery level  
- Decoded raw BLE data into meaningful values  
- Packaged processed data into structured JSON format  
- Transmitted smartwatch data to backend REST API  

---

### 🔹 **(AI / Machine Learning)**
- Designed and implemented the **AI anomaly detection model**  
- Used **Isolation Forest (unsupervised learning)**  
- Detected anomalies such as:
  - Heavy data transfer  
  - High-frequency activity events  
  - Abnormal wearable metrics  
- Integrated ML predictions with backend data pipeline  

---

## 📊 Dashboard & Monitoring
- Developed a **Streamlit-based live dashboard**  
- Features:
  - Real-time monitoring of all connected devices  
  - Anomaly alerts  
  - Device-based filtering  
  - Data export for analysis  

---

## 🏁 Final Summary
This project demonstrates an end-to-end **real-time multi-device anomaly detection system** built using industry-standard backend, machine learning, and data ingestion practices. The modular and scalable design enables seamless integration of heterogeneous devices and prepares the system for real-world monitoring and security use cases.

---

## 👥 Team
- **Khushi Sharma** – Backend & System Integration  
- **Anushree** – Android Development  
- **Shubhangi** – Laptop Data Collection  
- **Pranav** – Smartwatch Data Collection  
- **Aarya** – AI / ML Model Development  

