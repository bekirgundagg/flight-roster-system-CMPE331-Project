import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import "./App.css";

import LoginPage from "./components/LoginPage";
import PilotsPage from "./components/PilotsPage";
import FlightCrewPage from "./components/FlightCrewPage";
import PassengersPage from "./components/PassengersPage";
import FlightsPage from "./components/FlightsPage";
import FlightRosterPage from "./components/FlightRosterPage";

function Dashboard() {
  const navigate = useNavigate();

  return (
    // BURASI DEĞİŞTİ: Sınıf ismini 'dashboard-container' yaptık.
    // CSS dosyasında .dashboard-container sınıfına ortalama kodlarını yazacaksın.
    <div className="dashboard-container">
      <h1 className="title">SkyTeam Dashboard ✈️</h1>

      <div className="nav-buttons">
        <button onClick={() => navigate("/dashboard/pilots")}>Pilots</button>
        <button onClick={() => navigate("/dashboard/crew")}>Flight Crew</button>
        <button onClick={() => navigate("/dashboard/passengers")}>Passengers</button>
        <button onClick={() => navigate("/dashboard/flights")}>Flights</button>
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