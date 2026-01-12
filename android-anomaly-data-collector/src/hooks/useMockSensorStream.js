// src/hooks/useMockSensorStream.js   (replaced with real backend polling)

import { useEffect, useRef, useState } from "react";
import { SENSORS } from "../config/sensors";

/*
Polls backend endpoint and maps result into:
  data: { sensorId: { latest, history } }
  readingCount: total readings counter
*/
export function useMockSensorStream(intervalMs = 1000, opts = {}) {
  const { deviceId } = opts;

  const [data, setData] = useState(() =>
    SENSORS.reduce((acc, s) => {
      acc[s.id] = { latest: null, history: [] };
      return acc;
    }, {})
  );

  const readingCountRef = useRef(0);
  const timerRef = useRef(null);
  const [, tick] = useState(0);

  // Backend URL (edit .env or replace default)
  const BASE =
    process.env.REACT_APP_BACKEND_URL ||
    "https://your-backend.example";

  function getUrl() {
    let url = `${BASE}/api/readings/latest/?limit=50`;
    if (deviceId) url += `&device_id=${encodeURIComponent(deviceId)}`;
    return url;
  }

  async function fetchOnce() {
    try {
      const res = await fetch(getUrl(), {
        headers: { Accept: "application/json" }
      });

      if (!res.ok) throw new Error("Network error");

      const payload = await res.json();
      const readings = Array.isArray(payload.data) ? payload.data : [];

      setData(prev => {
        const next = { ...prev };

        readings.forEach(r => {
          const id = r.sensor_id || r.sensorId || r.id || "unknown";
          const prevHistory = next[id]?.history || [];

          next[id] = {
            latest: r,
            history: [...prevHistory.slice(-49), r]
          };

          readingCountRef.current++;
        });

        tick(n => n + 1);
        return next;
      });
    } catch (err) {
      console.warn("Fetch failed:", err.message);
    }
  }

  function start() {
    if (timerRef.current) return;
    fetchOnce();
    timerRef.current = setInterval(fetchOnce, intervalMs);
  }

  function stop() {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  }

  useEffect(() => {
    function onToggle() {
      if (timerRef.current) stop();
      else start();
    }

    function onClear() {
      setData(
        SENSORS.reduce((acc, s) => {
          acc[s.id] = { latest: null, history: [] };
          return acc;
        }, {})
      );
      readingCountRef.current = 0;
      tick(n => n + 1);
    }

    window.addEventListener("toggle-stream", onToggle);
    window.addEventListener("clear-data", onClear);

    start();

    return () => {
      stop();
      window.removeEventListener("toggle-stream", onToggle);
      window.removeEventListener("clear-data", onClear);
    };
  }, []);

  return { data, readingCount: readingCountRef.current };
}
