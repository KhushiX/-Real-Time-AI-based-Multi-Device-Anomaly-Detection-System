import React from "react";

function SensorCardSmall({ sensor, latest }) {
  return (
    <div className={`sensor-card ${sensor.id}`} id={`card-${sensor.id}`}>
      <div className="card-header">
        <div className="card-title-section">
          <div className="card-icon">{sensor.icon}</div>
          <div className="card-title">
            <h3>{sensor.label}</h3>
            <span>{sensor.unit}</span>
          </div>
        </div>
        <div className="live-badge">LIVE</div>
      </div>

      <div className="sensor-values">
        {sensor.hasAxes ? (
          <div className="axes-grid">
            <div className="axis-value">
              <div className="axis-label">X</div>
              <div className="axis-number" id={`${sensor.id}-x`}>{latest ? Number(latest.x).toFixed(2) : "—"}</div>
            </div>
            <div className="axis-value">
              <div className="axis-label">Y</div>
              <div className="axis-number" id={`${sensor.id}-y`}>{latest ? Number(latest.y).toFixed(2) : "—"}</div>
            </div>
            <div className="axis-value">
              <div className="axis-label">Z</div>
              <div className="axis-number" id={`${sensor.id}-z`}>{latest ? Number(latest.z).toFixed(2) : "—"}</div>
            </div>
          </div>
        ) : (
          <div className="single-value">
            <div className="value" id={`${sensor.id}-value`}>{latest ? Number(latest.value).toFixed(2) : "—"}</div>
          </div>
        )}
      </div>

      <div className="card-footer">
        <span>Last update</span>
        <span className="timestamp" id={`${sensor.id}-timestamp`}>{latest ? new Date(latest.timestamp).toLocaleTimeString() : "—"}</span>
      </div>
    </div>
  );
}

export default function SensorsGrid({ sensors, data }) {
  return (
    <div className="sensors-grid" id="sensorsGrid">
      {sensors.map(s => <SensorCardSmall key={s.id} sensor={s} latest={data[s.id]?.latest} />)}
    </div>
  );
}
