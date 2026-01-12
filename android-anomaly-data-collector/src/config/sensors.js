export const SENSORS = [
  { id: 'accelerometer', label: 'Accelerometer', unit: 'm/s²', icon: '📈', hasAxes: true, colors: { x: '#00d4ff', y: '#00b4d8', z: '#0096c7' } },
  { id: 'gyroscope', label: 'Gyroscope', unit: 'rad/s', icon: '🔄', hasAxes: true, colors: { x: '#a855f7', y: '#9333ea', z: '#7c3aed' } },
  { id: 'magnetometer', label: 'Magnetometer', unit: 'μT', icon: '🧭', hasAxes: true, colors: { x: '#22c55e', y: '#16a34a', z: '#15803d' } },
  { id: 'light', label: 'Light Sensor', unit: 'lux', icon: '☀️', hasAxes: false, colors: { value: '#facc15' } },
  { id: 'proximity', label: 'Proximity', unit: 'cm', icon: '📡', hasAxes: false, colors: { value: '#ec4899' } },
  { id: 'pressure', label: 'Pressure', unit: 'hPa', icon: '🌡️', hasAxes: false, colors: { value: '#38bdf8' } },
  // optional added sensors you used before:
  { id: 'temperature', label: 'Temperature', unit: '°C', icon: '🌡️', hasAxes: false, colors: { value: '#ff6347' } },
  { id: 'humidity', label: 'Humidity', unit: '%', icon: '💧', hasAxes: false, colors: { value: '#1e90ff' } },
  { id: 'ambienttemp', label: 'Ambient Temp', unit: '°C', icon: '🔥', hasAxes: false, colors: { value: '#ffa500' } }
];
