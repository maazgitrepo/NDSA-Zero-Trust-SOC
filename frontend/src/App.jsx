import { useEffect, useState } from "react";

function App() {
  const [alerts, setAlerts] = useState([]);
  const [title, setTitle] = useState("");
  const [severity, setSeverity] = useState("low");

  const loadAlerts = async () => {
    const response = await fetch("http://127.0.0.1:8001/alerts");
    const data = await response.json();
    setAlerts(data);
  };

  const createAlert = async (e) => {
    e.preventDefault();

    await fetch(
      `http://127.0.0.1:8001/alerts?title=${encodeURIComponent(title)}&severity=${severity}`,
      {
        method: "POST",
      }
    );

    setTitle("");
    setSeverity("low");
    loadAlerts();
  };

  useEffect(() => {
    loadAlerts();
  }, []);

  return (
    <div>
      <h1>NDSA Zero Trust SOC</h1>

      <h2>Create Alert</h2>

      <form onSubmit={createAlert}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Alert title"
          required
        />

        <select
          value={severity}
          onChange={(e) => setSeverity(e.target.value)}
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="critical">Critical</option>
        </select>

        <button type="submit">Create Alert</button>
      </form>

      <h2>Security Alerts</h2>

      {alerts.map((alert) => (
        <div key={alert.id}>
          <strong>{alert.title}</strong> — {alert.severity}
        </div>
      ))}
    </div>
  );
}

export default App;
