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
function Dashboard() {
  const navigate = useNavigate();
    const handleLogout = () => {
    // 1. Token'ı sil
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token'); // Varsa bunu da sil

    // 2. Kullanıcıya bilgi ver (Opsiyonel)
    // alert("Başarıyla çıkış yapıldı.");

    // 3. Giriş sayfasına yönlendir
    navigate('/');
    };
  return (

    <div className="dashboard-container">
        <button onClick={handleLogout} className="logout-btn">
              LOGOUT
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