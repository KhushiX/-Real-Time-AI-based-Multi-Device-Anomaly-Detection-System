package com.example.mobilesensorclient

import android.bluetooth.BluetoothAdapter
import android.content.Intent
import android.content.IntentFilter
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.os.BatteryManager
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.provider.Settings
import android.util.Log
import android.view.MotionEvent
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import org.json.JSONObject
import java.io.BufferedWriter
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import kotlin.math.sqrt

class MainActivity : AppCompatActivity(), SensorEventListener {

    companion object {
        private const val SERVER_URL =
            "http://192.168.149.182:8000/api/unified-activity/"
    }

    /* ---------------- CORE OBJECTS ---------------- */

    private lateinit var behaviourAggregator: BehaviourAggregator
    private lateinit var screenReceiver: ScreenReceiver
    private lateinit var bluetoothReceiver: BluetoothReceiver

    private lateinit var sensorManager: SensorManager
    private var accel: Sensor? = null
    private var gyro: Sensor? = null

    /* ---------------- UI ---------------- */

    private lateinit var tvBattery: TextView
    private lateinit var tvAccel: TextView
    private lateinit var tvGyro: TextView
    private lateinit var tvStatus: TextView

    /* ---------------- STATE ---------------- */

    private var batteryLevel: Int = -1
    private val handler = Handler(Looper.getMainLooper())

    /* ---------------- ACTIVITY LIFECYCLE ---------------- */

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        behaviourAggregator = BehaviourAggregator()

        // Screen receiver
        screenReceiver = ScreenReceiver(behaviourAggregator)
        val screenFilter = IntentFilter().apply {
            addAction(Intent.ACTION_SCREEN_ON)
            addAction(Intent.ACTION_SCREEN_OFF)
        }
        registerReceiver(screenReceiver, screenFilter)

        // Bluetooth receiver
        bluetoothReceiver = BluetoothReceiver(behaviourAggregator)
        val bluetoothFilter = IntentFilter(BluetoothAdapter.ACTION_STATE_CHANGED)
        registerReceiver(bluetoothReceiver, bluetoothFilter)

        tvBattery = findViewById(R.id.tvBattery)
        tvAccel = findViewById(R.id.tvAccel)
        tvGyro = findViewById(R.id.tvGyro)
        tvStatus = findViewById(R.id.tvStatus)

        sensorManager = getSystemService(SENSOR_SERVICE) as SensorManager
        accel = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
        gyro = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE)

        accel?.let {
            sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_NORMAL)
        }

        gyro?.let {
            sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_NORMAL)
        }

        startAggregationTimer()
        tvStatus.text = "Behaviour monitoring started"
    }

    override fun onResume() {
        super.onResume()
        accel?.let {
            sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_NORMAL)
        }
        gyro?.let {
            sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_NORMAL)
        }
    }

    override fun onPause() {
        super.onPause()
        sensorManager.unregisterListener(this)
    }

    override fun onDestroy() {
        super.onDestroy()
        unregisterReceiver(screenReceiver)
        unregisterReceiver(bluetoothReceiver)
    }

    /* ---------------- SENSOR CALLBACK ---------------- */

    override fun onSensorChanged(event: SensorEvent?) {
        when (event?.sensor?.type) {

            Sensor.TYPE_ACCELEROMETER -> {
                val x = event.values[0]
                val y = event.values[1]
                val z = event.values[2]

                val magnitude = sqrt(x * x + y * y + z * z)
                behaviourAggregator.recordAccelerometer(magnitude)

                tvAccel.text = "Accel magnitude: %.2f".format(magnitude)
            }

            Sensor.TYPE_GYROSCOPE -> {
                val x = event.values[0]
                val y = event.values[1]
                val z = event.values[2]

                tvGyro.text = "Gyro: x=%.2f y=%.2f z=%.2f".format(x, y, z)
            }
        }
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {}

    /* ---------------- USER INPUT ---------------- */

    override fun dispatchTouchEvent(ev: MotionEvent): Boolean {
        behaviourAggregator.recordUserInput()
        return super.dispatchTouchEvent(ev)
    }

    /* ---------------- BATTERY ---------------- */

    private fun readBatteryLevel() {
        val intent = registerReceiver(null, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
        val level = intent?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: -1
        val scale = intent?.getIntExtra(BatteryManager.EXTRA_SCALE, -1) ?: -1

        if (level >= 0 && scale > 0) {
            batteryLevel = (level * 100) / scale
            tvBattery.text = "Battery Level: $batteryLevel%"
        }
    }

    /* ---------------- AGGREGATION TIMER ---------------- */

    private fun startAggregationTimer() {
        handler.postDelayed(object : Runnable {
            override fun run() {
                readBatteryLevel()

                val json = buildAggregatedJSON()
                Log.d("ANOMALY_JSON", json.toString())

                sendDataToServer(json)
                behaviourAggregator.reset()

                handler.postDelayed(this, 30_000)
            }
        }, 30_000)
    }

    /* ---------------- BUILD JSON ---------------- */

    private fun buildAggregatedJSON(): JSONObject {
        val json = JSONObject()
        val timestamp = SimpleDateFormat(
            "yyyy-MM-dd HH:mm:ss",
            Locale.getDefault()
        ).format(Date())

        json.put(
            "device_id",
            Settings.Secure.getString(
                contentResolver,
                Settings.Secure.ANDROID_ID
            )
        )
        json.put("device_type", "Mobile")

        // Mobile fields
        json.put("accel_level", behaviourAggregator.getDominantAccelLevel())
        json.put("bluetooth_state", behaviourAggregator.bluetoothState)
        json.put("screen_state", behaviourAggregator.screenState)
        json.put("input_activity", behaviourAggregator.inputActivity)
        json.put("activity_duration_sec", behaviourAggregator.activityDurationSec)
        json.put("event_frequency", behaviourAggregator.eventFrequency)
        json.put("battery_level", batteryLevel)

        // Laptop-only fields (explicit nulls)
        json.put("file_transfer", JSONObject.NULL)
        json.put("data_transfer_mb", JSONObject.NULL)

        // Watch-only fields (explicit null)
        json.put("heart_rate", JSONObject.NULL)

        json.put("timestamp", timestamp)
        return json
    }

    /* ---------------- SEND TO BACKEND ---------------- */

    private fun sendDataToServer(json: JSONObject) {
        Thread {
            try {
                val url = URL(SERVER_URL)
                val conn = url.openConnection() as HttpURLConnection
                conn.requestMethod = "POST"
                conn.setRequestProperty("Content-Type", "application/json")
                conn.connectTimeout = 5000
                conn.readTimeout = 5000
                conn.doOutput = true

                BufferedWriter(OutputStreamWriter(conn.outputStream)).use {
                    it.write(json.toString())
                }

                val responseCode = conn.responseCode
                Log.d("HTTP_RESPONSE", "Server responded with code: $responseCode")

                runOnUiThread {
                    tvStatus.text = "Server response: $responseCode"
                }

                conn.disconnect()

            } catch (e: Exception) {
                Log.e("HTTP_ERROR", e.message ?: "Unknown error")
                runOnUiThread {
                    tvStatus.text = "Send failed: ${e.message}"
                }
            }
        }.start()
    }
}
