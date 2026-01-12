package com.example.mobilesensorclient

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent

class ScreenReceiver(
    private val behaviourAggregator: BehaviourAggregator
) : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {
        when (intent.action) {
            Intent.ACTION_SCREEN_ON -> {
                behaviourAggregator.updateScreenState("ON")
            }

            Intent.ACTION_SCREEN_OFF -> {
                behaviourAggregator.updateScreenState("OFF")
            }
        }
    }
}
