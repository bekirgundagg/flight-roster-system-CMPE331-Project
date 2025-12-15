import { useParams } from "react-router-dom";

import pilots from "../assets/data/pilot.json";
import crew from "../assets/data/crew.json";
import passengers from "../assets/data/passengers.json";

export default function FlightRosterPage() {
  const { flightNo } = useParams();

  /* ===============================
     DATA PREPARATION
  =============================== */

  // Gerçek passenger'lar (flight'a göre)
  const flightPassengers = passengers.filter(
    (p) => p.flight === flightNo
  );

  // Mock seat data (passenger yoksa)
  const mockSeats = [
    { id: 1, name: "Emily Carter", ticket: "Economy" },
    { id: 2, name: "Hiroshi Tanaka", ticket: "Business" },
    { id: 3, name: "Sarah Thompson", ticket: "Economy" },
    { id: 4, name: "Kenji Nakamura", ticket: "Business" },
  ];

  // Plane view'de gösterilecek koltuklar
  const seatsToShow =
    flightPassengers.length > 0 ? flightPassengers : mockSeats;

  /* ===============================
     EXPORT ROSTER (JSON)
  =============================== */
  const exportRosterJSON = () => {
    const rosterData = {
      flightNo: flightNo,
      pilots: pilots,
      cabinCrew: crew,
      passengers: flightPassengers,
      generatedAt: new Date().toISOString(),
    };

    const jsonString = JSON.stringify(rosterData, null, 2);
    const blob = new Blob([jsonString], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = `roster_${flightNo}.json`;
    link.click();

    URL.revokeObjectURL(url);
  };

  /* ===============================
     RENDER
  =============================== */
  return (
    <div className="page-container">
      <h2 className="page-title">Flight Roster – {flightNo}</h2>
      <p className="page-subtitle">
        Combined roster information for the selected flight.
      </p>

      <button
        onClick={exportRosterJSON}
        style={{
          marginBottom: "24px",
          padding: "10px 18px",
          borderRadius: "12px",
          border: "none",
          background: "#0d6efd",
          color: "white",
          fontWeight: "700",
          cursor: "pointer",
        }}
      >
        Export Roster (JSON)
      </button>

      {/* ===============================
         TABULAR VIEW (SUMMARY)
      =============================== */}
      <div className="card" style={{ marginBottom: "30px" }}>
        <h3>Tabular View (Summary)</h3>
        <table className="styled-table">
          <thead>
            <tr>
              <th>Type</th>
              <th>ID</th>
              <th>Name</th>
              <th>Role / Seat</th>
            </tr>
          </thead>
          <tbody>
            {pilots.map((p) => (
              <tr key={`pilot-${p.id}`}>
                <td>Pilot</td>
                <td>{p.id}</td>
                <td>{p.name}</td>
                <td>{p.rank}</td>
              </tr>
            ))}

            {crew.map((c) => (
              <tr key={`crew-${c.id}`}>
                <td>Cabin Crew</td>
                <td>{c.id}</td>
                <td>{c.name}</td>
                <td>{c.role}</td>
              </tr>
            ))}

            {flightPassengers.map((p) => (
              <tr key={`passenger-${p.id}`}>
                <td>Passenger</td>
                <td>{p.id}</td>
                <td>{p.name}</td>
                <td>{p.ticket}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* ===============================
         EXTENDED VIEW – PASSENGERS
      =============================== */}
      <div className="card" style={{ marginBottom: "30px" }}>
        <h3>Passengers</h3>
        <table className="styled-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Passport</th>
              <th>Ticket</th>
            </tr>
          </thead>
          <tbody>
            {flightPassengers.map((p) => (
              <tr key={p.id}>
                <td>{p.id}</td>
                <td>{p.name}</td>
                <td>{p.passport}</td>
                <td>{p.ticket}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* ===============================
         PLANE VIEW (MOCK SEAT PLAN)
      =============================== */}
      <div className="card">
        <h3>Plane View (Seat Plan)</h3>

        {flightPassengers.length === 0 && (
          <p className="page-subtitle">
            Sample seat data is shown for demonstration purposes.
          </p>
        )}

        <div className="seat-grid">
          {seatsToShow.map((p, index) => (
            <div key={p.id} className="seat">
              <span className="seat-label">{index + 1}A</span>
              <div className="seat-tooltip">
                <strong>{p.name}</strong>
                <br />
                {p.ticket} Class
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
