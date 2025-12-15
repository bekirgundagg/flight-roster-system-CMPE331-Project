import flights from "../assets/data/flights.json";
import { useNavigate } from "react-router-dom";

export default function FlightsPage() {
  const navigate = useNavigate();

  const calculateDuration = (departure, arrival) => {
    const diff = new Date(arrival) - new Date(departure);
    const h = Math.floor(diff / (1000 * 60 * 60));
    const m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    return `${h}h ${m}m`;
  };

  return (
    <div className="page-container">
      <h2 className="page-title">Flights Management</h2>
      <p className="page-subtitle">
        Select a flight to view its roster information.
      </p>

      <div className="card">
        <table className="styled-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Flight No</th>
              <th>Route</th>
              <th>Departure</th>
              <th>Arrival</th>
              <th>Duration</th>
              <th>Status</th>
              <th>Roster</th>
            </tr>
          </thead>

          <tbody>
            {flights.map((f) => (
              <tr key={f.id}>
                <td>{f.id}</td>
                <td>{f.flightNo}</td>
                <td>{f.origin} → {f.destination}</td>
                <td>{new Date(f.departure).toLocaleString()}</td>
                <td>{new Date(f.arrival).toLocaleString()}</td>
                <td>{calculateDuration(f.departure, f.arrival)}</td>
                <td>
                  <span
                    className={`status-badge ${f.status
                      .replace(" ", "")
                      .toLowerCase()}`}
                  >
                    {f.status}
                  </span>
                </td>
                <td>
                  <button
                    onClick={() => navigate(`/roster/${f.flightNo}`)}
                    style={{
                      padding: "6px 14px",
                      borderRadius: "10px",
                      border: "none",
                      background: "#0d6efd",
                      color: "white",
                      fontWeight: "600",
                      cursor: "pointer",
                    }}
                  >
                    View Roster
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
