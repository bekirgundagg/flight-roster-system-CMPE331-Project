import React from "react";

function FlightCrewDetailPage({ crew, onBack }) {
  if (!crew) return null;

  return (
    <div style={{ padding: 40 }}>
      <button onClick={onBack} style={{ marginBottom: 20 }}>← Back</button>
      <h1>{crew.name}</h1>

      <div style={{
        display: "flex",
        gap: 30,
        padding: 30,
        background: "#2f343f",
        borderRadius: 12,
        color: "white",
        maxWidth: 900
      }}>
        <img
          src={crew.image}
          alt={crew.name}
          style={{
            width: 180,
            height: 180,
            borderRadius: "50%",
            objectFit: "cover",
            border: "4px solid #007bff"
          }}
        />

        <div>
          <p><strong>Age:</strong> {crew.age}</p>
          <p><strong>Role:</strong> {crew.role}</p>

          <p style={{ marginTop: 12 }}><strong>Planes:</strong></p>
          <ul>
            {crew.planes.map((p, index) => <li key={index}>{p}</li>)}
          </ul>

          <p style={{ marginTop: 12 }}><strong>Flights:</strong></p>
          <ul>
            {crew.flights.map((f, index) => <li key={index}>{f}</li>)}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default FlightCrewDetailPage;
