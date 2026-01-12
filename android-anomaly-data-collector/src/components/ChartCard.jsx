import React, { useEffect, useRef } from "react";

export default function ChartCard({ sensor, history }) {
  const canvasRef = useRef(null);
  const rafRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    // Use DPR but cap backing store dimensions to avoid huge memory usage
    const DPR = Math.max(1, Math.floor(window.devicePixelRatio || 1));
    const MAX_BACKING_PIXELS = 2000; // cap width/height in pixels (adjust if desired)

    function scheduleDraw() {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
      rafRef.current = requestAnimationFrame(() => {
        draw();
        rafRef.current = null;
      });
    }

    function resize() {
      const rect = canvas.getBoundingClientRect();
      const widthCss = Math.max(1, rect.width);
      const heightCss = Math.max(1, rect.height);

      // reset transforms before changing size
      ctx.setTransform(1, 0, 0, 1, 0, 0);

      // compute backing-store size but cap to MAX_BACKING_PIXELS
      const bw = Math.min(Math.round(widthCss * DPR), MAX_BACKING_PIXELS);
      const bh = Math.min(Math.round(heightCss * DPR), MAX_BACKING_PIXELS);

      canvas.width = bw;
      canvas.height = bh;

      // ensure CSS size explicitly (helps some browsers)
      canvas.style.width = `${widthCss}px`;
      canvas.style.height = `${heightCss}px`;

      // scale drawing operations to CSS pixels
      ctx.scale(bw / widthCss, bh / heightCss); // equivalent to ctx.scale(DPR,DPR) but safe with cap
      scheduleDraw();
    }

    function draw() {
      try {
        const data = history || [];

        // Use CSS sizes for layout math
        const rect = canvas.getBoundingClientRect();
        const widthCss = Math.max(1, rect.width);
        const heightCss = Math.max(1, rect.height);

        const padding = { top: 20, right: 20, bottom: 30, left: 50 };
        const chartWidth = widthCss - padding.left - padding.right;
        const chartHeight = heightCss - padding.top - padding.bottom;

        // clear entire backing store using canvas width/height (pixel coords)
        ctx.save();
        ctx.setTransform(1, 0, 0, 1, 0, 0); // reset
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // restore the scale that we use for drawing
        const scaleX = canvas.width / widthCss;
        const scaleY = canvas.height / heightCss;
        ctx.scale(scaleX, scaleY);

        if (data.length < 2) {
          ctx.fillStyle = '#64748b';
          ctx.font = '12px sans-serif';
          ctx.textAlign = 'center';
          ctx.fillText('Waiting for data...', widthCss / 2, heightCss / 2);
          ctx.restore();
          return;
        }

        // Build values
        let allValues = [];
        if (sensor.hasAxes) data.forEach(d => allValues.push(d.x, d.y, d.z));
        else data.forEach(d => allValues.push(d.value));

        const minVal = Math.min(...allValues);
        const maxVal = Math.max(...allValues);
        const range = maxVal - minVal || 1;
        const yMin = minVal - range * 0.1;
        const yMax = maxVal + range * 0.1;

        // draw grid (in CSS coords)
        ctx.strokeStyle = 'rgba(255,255,255,0.1)';
        ctx.lineWidth = 1;
        for (let i = 0; i <= 4; i++) {
          const y = padding.top + (chartHeight / 4) * i;
          ctx.beginPath();
          ctx.moveTo(padding.left, y);
          ctx.lineTo(widthCss - padding.right, y);
          ctx.stroke();

          const value = yMax - ((yMax - yMin) / 4) * i;
          ctx.fillStyle = '#64748b';
          ctx.font = '10px monospace';
          ctx.textAlign = 'right';
          ctx.fillText(value.toFixed(1), padding.left - 5, y + 3);
        }

        function drawLine(values, color) {
          ctx.strokeStyle = color;
          ctx.lineWidth = 2;
          ctx.beginPath();
          values.forEach((val, i) => {
            const x = padding.left + (i / (values.length - 1)) * chartWidth;
            const y = padding.top + ((yMax - val) / (yMax - yMin)) * chartHeight;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
          });
          ctx.stroke();
        }

        if (sensor.hasAxes) {
          drawLine(data.map(d => d.x), sensor.colors.x);
          drawLine(data.map(d => d.y), sensor.colors.y);
          drawLine(data.map(d => d.z), sensor.colors.z);
        } else {
          drawLine(data.map(d => d.value), sensor.colors.value);
        }

        ctx.restore();
      } catch (err) {
        console.error("Chart draw error:", sensor.id, err);
      }
    }

    // initial resize/draw
    resize();

    // redraw on window resize
    window.addEventListener("resize", resize);

    // when history updates, schedule a draw (rAF)
    scheduleDraw();

    return () => {
      window.removeEventListener("resize", resize);
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, [history, sensor]);

  return (
    <div className="chart-card">
      <div className="chart-header">
        <h4>{sensor.icon} {sensor.label} History</h4>
        <span id={`chart-count-${sensor.id}`}>{(history || []).length} readings</span>
      </div>
      <div className="chart-container">
        <canvas ref={canvasRef} id={`chart-${sensor.id}`}></canvas>
      </div>
      {sensor.hasAxes && (
        <div className="chart-legend">
          <div className="legend-item"><div className="legend-color" style={{ background: sensor.colors.x }}></div><span>X</span></div>
          <div className="legend-item"><div className="legend-color" style={{ background: sensor.colors.y }}></div><span>Y</span></div>
          <div className="legend-item"><div className="legend-color" style={{ background: sensor.colors.z }}></div><span>Z</span></div>
        </div>
      )}
    </div>
  );
}
