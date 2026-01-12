import React from "react";

export default function StatusBar({ isStreaming, onToggle, onClear, deviceId, readingCount }) {
  return (
    <div className="status-bar">
      <div className="status-indicator">
        <div className="status-dot" id="statusDot" style={{ background: isStreaming ? "#22c55e" : "#ef4444" }}></div>
        <span className="status-text" id="statusText" style={{ color: isStreaming ? "#1ce666" : "#ef4444" }}>{isStreaming ? "STREAMING" : "PAUSED"}</span>
      </div>
      <div className="device-info">
        Device: <span id="deviceId">{deviceId}</span> | Readings: <span id="readingCount">{readingCount}</span>
      </div>
      <div className="controls">
        <button className={isStreaming ? "btn-stop" : "btn-start"} id="toggleBtn" onClick={onToggle}>{isStreaming ? "Stop" : "Start"}</button>
        <button className="btn-clear" onClick={onClear}>Clear Data</button>
      </div>
    </div>
  );
}
