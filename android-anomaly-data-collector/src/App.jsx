import React, { useState, useEffect } from "react";
import Header from "./components/Header";
import StatusBar from "./components/StatusBar";
import SensorsGrid from "./components/SensorsGrid";
import ChartsSection from "./components/ChartsSection";
import Footer from "./components/Footer";
import { useMockSensorStream } from "./hooks/useMockSensorStream";
import { SENSORS } from "./config/sensors";

export default function App() {
  // lower update frequency to avoid CPU/memory issues (500ms = 2Hz)
  const { data, readingCount } = useMockSensorStream(500);

  const [isStreaming, setIsStreaming] = useState(true);

  useEffect(() => {
    // watch for toggle events from hook via custom event (hook exposes readingCount)
    function onToggleEvent(ev) {
      setIsStreaming(ev.detail === undefined ? !isStreaming : ev.detail);
    }
    window.addEventListener("streaming-changed", onToggleEvent);
    return () => window.removeEventListener("streaming-changed", onToggleEvent);
  }, [isStreaming]);

  function handleToggle() {
    const ev = new CustomEvent("toggle-stream");
    window.dispatchEvent(ev);
    setIsStreaming(prev => !prev);
    // notify UI toggle
    window.dispatchEvent(new CustomEvent("streaming-changed", { detail: !isStreaming }));
  }

  function handleClear() {
    const ev = new CustomEvent("clear-data");
    window.dispatchEvent(ev);
  }

  return (
    <div className="container">
      <Header />
      <StatusBar
        isStreaming={isStreaming}
        onToggle={handleToggle}
        onClear={handleClear}
        deviceId="MOCK-DEVICE-001"
        readingCount={readingCount}
      />
      <SensorsGrid sensors={SENSORS} data={data} />
      <ChartsSection sensors={SENSORS} data={data} />
      <Footer />
    </div>
  );
}
