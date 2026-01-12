# Android Anomaly Data Client

## Overview
This Android application is a mobile data collection module developed as part of a multi-device anomaly detection system. It captures real-time behavioral and sensor data from the user's mobile device and sends aggregated information to a backend server for analysis and machine learning-based anomaly detection.

## Features
- Collects accelerometer data to estimate activity level
- Tracks gyroscope readings
- Monitors screen ON/OFF state
- Detects Bluetooth state changes
- Records user touch interactions
- Captures battery percentage
- Aggregates data in fixed time windows
- Sends structured JSON data to backend API

## Technologies Used
- Kotlin (Android Development)
- Android Sensors API
- Broadcast Receivers
- REST API (HTTP POST)
- JSON Data Formatting
- Android Studio

## Data Collected
- Device ID
- Device type (Mobile)
- Activity level (LOW / MED / HIGH)
- Bluetooth state
- Screen state
- Input activity
- Activity duration
- Event frequency
- Battery level
- Timestamp

## Project Structure
- MainActivity.kt – Sensor collection, data aggregation, API calls
- BehaviourAggregator.kt – Feature aggregation logic
- ScreenReceiver.kt – Screen state tracking
- BluetoothReceiver.kt – Bluetooth state tracking
- activity_main.xml – UI layout

## How It Works
1. The app listens to mobile sensors and system events.
2. Data is aggregated over a fixed time window.
3. Aggregated features are formatted as JSON.
4. JSON payload is sent to backend API.
5. Backend forwards data to ML model for anomaly detection.

## Purpose
This module serves as the Android client in a larger anomaly detection system that includes:
- Backend services
- Machine learning model
- Laptop monitoring module
- Smartwatch integration

## Author
Anushree Jaiswal  
B.Tech CSE (Data Science)
