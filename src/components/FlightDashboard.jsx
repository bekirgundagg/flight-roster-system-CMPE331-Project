import React from "react";
import { useNavigate } from "react-router-dom";

function FlightDashboard() {
  const navigate = useNavigate();

  return (
    <div style={{ padding: "20px" }}>
      <h1 style={{ fontSize: "40px", display: "flex", alignItems: "center" }}>
        SkyTeam Dashboard ✈️
      </h1>

      <div className="nav-buttons">
        <button onClick={() => navigate("/pilots")}>Pilots</button>
        <button onClick={() => navigate("/crew")}>Flight Crew</button>
        <button onClick={() => navigate("/passengers")}>Passengers</button>
        <button onClick={() => navigate("/flights")}>Flights</button>
      </div>
    </div>
  );
}

export default FlightDashboard;
