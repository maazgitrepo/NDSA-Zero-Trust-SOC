import { useEffect, useState } from "react";
import keycloak from "./keycloak";

function App() {
  const [alerts, setAlerts] = useState([]);
  const [incidents, setIncidents] = useState([]);

  const [title, setTitle] = useState("");
  const [severity, setSeverity] = useState("low");
  const [filter, setFilter] = useState("all");

  const [incidentTitle, setIncidentTitle] = useState("");
  const [incidentSeverity, setIncidentSeverity] = useState("High");
  const [incidentOwner, setIncidentOwner] = useState("");

  const loadAlerts = async () => {
    try {
      await keycloak.updateToken(30);

      const response = await fetch(
        "http://192.168.2.211:8001/alerts",
        {
          headers: {
            Authorization: `Bearer ${keycloak.token}`,
          },
        }
      );

      if (!response.ok) {
        console.error("Alerts API:", response.status);
        return;
      }

      const data = await response.json();
      setAlerts(data);
    } catch (error) {
      console.error("Load alerts failed:", error);
    }
  };

  const loadIncidents = async () => {
    try {
      await keycloak.updateToken(30);

      const response = await fetch(
        "http://192.168.2.211:8001/incidents",
        {
          headers: {
            Authorization: `Bearer ${keycloak.token}`,
          },
        }
      );

      if (!response.ok) {
        console.error("Incidents API:", response.status);
        return;
      }

      const data = await response.json();
      setIncidents(data);
    } catch (error) {
      console.error("Load incidents failed:", error);
    }
  };

  const createAlert = async (e) => {
    e.preventDefault();

    try {
      await keycloak.updateToken(30);

      const response = await fetch(
        `http://192.168.2.211:8001/alerts?title=${encodeURIComponent(
          title
        )}&severity=${severity}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${keycloak.token}`,
          },
        }
      );

      if (!response.ok) {
        console.error("Create alert:", response.status);
        return;
      }

      setTitle("");
      setSeverity("low");
      loadAlerts();
    } catch (error) {
      console.error("Create alert failed:", error);
    }
  };

  const createIncident = async (e) => {
    e.preventDefault();

    try {
      await keycloak.updateToken(30);

      const response = await fetch(
        `http://192.168.2.211:8001/incidents?title=${encodeURIComponent(
          incidentTitle
        )}&severity=${incidentSeverity}&owner=${encodeURIComponent(
          incidentOwner
        )}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${keycloak.token}`,
          },
        }
      );

      if (!response.ok) {
        console.error("Create incident:", response.status);
        return;
      }

      setIncidentTitle("");
      setIncidentSeverity("High");
      setIncidentOwner("");
      loadIncidents();
    } catch (error) {
      console.error("Create incident failed:", error);
    }
  };

  useEffect(() => {
    loadAlerts();
    loadIncidents();
  }, []);

  const filteredAlerts =
    filter === "all"
      ? alerts
      : alerts.filter((alert) => alert.severity === filter);

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

      <select value={filter} onChange={(e) => setFilter(e.target.value)}>
        <option value="all">All Alerts</option>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
        <option value="critical">Critical</option>
      </select>

      {filteredAlerts.map((alert) => (
        <div key={alert.id}>
          <strong>{alert.title}</strong> — {alert.severity}
        </div>
      ))}

      <h2>Create Incident</h2>

      <form onSubmit={createIncident}>
        <input
          value={incidentTitle}
          onChange={(e) => setIncidentTitle(e.target.value)}
          placeholder="Incident title"
          required
        />

        <select
          value={incidentSeverity}
          onChange={(e) => setIncidentSeverity(e.target.value)}
        >
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
          <option value="Critical">Critical</option>
        </select>

        <input
          value={incidentOwner}
          onChange={(e) => setIncidentOwner(e.target.value)}
          placeholder="Owner"
        />

        <button type="submit">Create Incident</button>
      </form>

      <h2>Incidents</h2>

      {incidents.map((incident) => (
        <div key={incident.id}>
          <strong>{incident.title}</strong> — {incident.severity} —{" "}
          {incident.status}
        </div>
      ))}
    </div>
  );
}

export default App;
