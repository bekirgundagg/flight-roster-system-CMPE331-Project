import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import "./App.css";
import GlobalManifestPage from "./components/GlobalManifestPage";
import LoginPage from "./components/LoginPage";
import PilotsPage from "./components/PilotsPage";
import FlightCrewPage from "./components/FlightCrewPage";
import PassengersPage from "./components/PassengersPage";
import FlightsPage from "./components/FlightsPage";
import FlightRosterPage from "./components/FlightRosterPage";
import logoImg from './assets/logo.png';
import React, { useState } from 'react';
function Dashboard() {
  const navigate = useNavigate();
  const [isFlying, setIsFlying] = useState(false);

    const handleLogout = () => {
    setIsFlying(true);
    setTimeout(() => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        navigate('/');
    }, 800);
    };
  return (

    <div className="dashboard-container">
        <button onClick={handleLogout} className={`logout-btn ${isFlying ? 'flying' : ''}`} disabled={isFlying}>
              <span className="btn-text">Logout</span>
            {/* App.jsx içindeki <svg> kısmını bununla değiştir */}
<svg
    className="plane-icon"
    viewBox="0 0 24 24" /* Standart boyut */
    fill="currentColor"
    xmlns="http://www.w3.org/2000/svg"
>
    <path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/>
</svg>
          </button>
        <img src={logoImg} alt="HvB Logo" className="dashboard-logo" />
      <h1 className="dashboard-title">HvB Team Dashboard</h1>

      <div className="nav-buttons">
        <button onClick={() => navigate("/dashboard/pilots")}>Pilots</button>
        <button onClick={() => navigate("/dashboard/crew")}>Flight Crew</button>
        <button onClick={() => navigate("/dashboard/passengers")}>Passengers</button>
        <button onClick={() => navigate("/dashboard/flights")}>Flights</button>
          <button onClick={() => navigate("/dashboard/global-manifest")}>Roster Management</button>
      </div>

    </div>
  );
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/dashboard/global-manifest" element={<GlobalManifestPage />} />
        <Route path="/dashboard/pilots" element={<PilotsPage />} />
        <Route path="/dashboard/crew" element={<FlightCrewPage />} />
        <Route path="/dashboard/passengers" element={<PassengersPage />} />
        <Route path="/dashboard/flights" element={<FlightsPage />} />

        {/* Roster sayfası dinamik parametre alıyor */}
        <Route path="/roster/:flightNo" element={<FlightRosterPage />} />

      </Routes>
    </Router>
  );
}