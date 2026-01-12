package com.example.mobilesensorclient

import android.bluetooth.BluetoothAdapter
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent

class BluetoothReceiver(
    private val behaviourAggregator: BehaviourAggregator
) : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {
        when (intent.action) {

            BluetoothAdapter.ACTION_STATE_CHANGED -> {
                val state = intent.getIntExtra(
                    BluetoothAdapter.EXTRA_STATE,
                    BluetoothAdapter.ERROR
                )

                when (state) {
                    BluetoothAdapter.STATE_ON ->
                        behaviourAggregator.updateBluetoothState("ON")

                    BluetoothAdapter.STATE_OFF ->
                        behaviourAggregator.updateBluetoothState("OFF")
                }
            }
        }
    }
}
