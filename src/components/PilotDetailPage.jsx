// src/components/PilotDetailPage.jsx
import React from 'react';
import './PilotDetailPage.css'; // Stil dosyası

function PilotDetailPage({ pilot, onBack }) {
  if (!pilot) {
    return <div className="pilot-detail-container">Pilot seçilmedi.</div>;
  }

  // Bu verileri mockRosterTK1923'ten veya mockFlights'tan çekebiliriz
  // Şimdilik varsayılan ilk uçuştan veri alalım
  const planeCode = "A320"; // pilot.vehicle_restriction
  const crewMembers = ["Ava Miller", "Lou Green"]; // mockRosterTK1923'ten
  const routes = ["Istanbul-New York", "Paris-Rome", "Saville-Tokyo", "Vilnius-Berlin"]; // Sabit örnek

  return (
    <div className="pilot-detail-container">
      <button className="back-button" onClick={onBack}>← Back</button>
      <h1>Pilots</h1>
      <div className="detail-card-wrapper">
        <div className="pilot-card-detail">
          <img src={pilot.image} alt={pilot.name} className="pilot-image-detail" />
          <h2>{pilot.name}</h2>
          <p>Age {pilot.age}</p>
        </div>
        <div className="pilot-info-panel">
          <p><strong>Plane Code:</strong> {planeCode}</p>
          <p><strong>Crew:</strong> {crewMembers.join(', ')}</p>
          <p><strong>Routes:</strong></p>
          <ul>
            {routes.map((route, index) => (
              <li key={index}>{route}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default PilotDetailPage;