package com.example.mobilesensorclient

class BehaviourAggregator {

    /* ---------------- ACCELEROMETER LEVEL COUNTS ---------------- */

    private var lowAccelCount = 0
    private var medAccelCount = 0
    private var highAccelCount = 0

    /* ---------------- DEVICE STATES ---------------- */

    var bluetoothState: String = "OFF"
        private set

    var screenState: String = "OFF"
        private set

    var inputActivity: Boolean = false
        private set

    /* ---------------- BEHAVIOR METRICS ---------------- */

    var activityDurationSec: Long = 0
        private set

    var eventFrequency: Int = 0
        private set

    private var lastStateChangeTime: Long = System.currentTimeMillis()

    /* ---------------- ACCELEROMETER HANDLING ---------------- */

    fun recordAccelerometer(magnitude: Float) {
        when {
            magnitude < 1.5 -> lowAccelCount++
            magnitude < 4.0 -> medAccelCount++
            else -> highAccelCount++
        }
        eventFrequency++
    }

    fun getDominantAccelLevel(): String {
        val accelMap = mapOf(
            "LOW" to lowAccelCount,
            "MED" to medAccelCount,
            "HIGH" to highAccelCount
        )
        return accelMap.maxByOrNull { it.value }?.key ?: "LOW"
    }

    /* ---------------- SCREEN STATE ---------------- */

    fun updateScreenState(state: String) {
        updateDuration()
        screenState = state
        eventFrequency++
    }

    /* ---------------- BLUETOOTH STATE ---------------- */

    fun updateBluetoothState(state: String) {
        updateDuration()
        bluetoothState = state
        eventFrequency++
    }

    /* ---------------- USER INPUT ---------------- */

    fun recordUserInput() {
        inputActivity = true
        eventFrequency++
    }

    /* ---------------- DURATION TRACKING ---------------- */

    private fun updateDuration() {
        val now = System.currentTimeMillis()
        activityDurationSec += (now - lastStateChangeTime) / 1000
        lastStateChangeTime = now
    }

    /* ---------------- RESET AFTER 60s WINDOW ---------------- */

    fun reset() {
        lowAccelCount = 0
        medAccelCount = 0
        highAccelCount = 0

        inputActivity = false
        activityDurationSec = 0
        eventFrequency = 0

        lastStateChangeTime = System.currentTimeMillis()
    }
}
