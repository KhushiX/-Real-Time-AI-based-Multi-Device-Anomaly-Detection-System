import React from "react";
import ChartCard from "./ChartCard";

export default function ChartsSection({ sensors, data }) {
  return (
    <section className="charts-section">
      <h2 className="section-title">📊 Data Visualization</h2>
      <div className="charts-grid" id="chartsGrid">
        {sensors.map(s => <ChartCard key={s.id} sensor={s} history={data[s.id]?.history || []} />)}
      </div>
    </section>
  );
}
