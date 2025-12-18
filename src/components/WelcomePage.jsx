import { useNavigate } from "react-router-dom";
import "./WelcomePage.css";

export default function WelcomePage() {
  const navigate = useNavigate();

  const handleEnter = () => {
    navigate("/login");
  };

  return (
    <div className="welcome-container">
      <div className="welcome-box">
        <h1>Welcome to SkyTeam Flight System</h1>
        <button className="enter-button" onClick={handleEnter}>
          Enter
        </button>
      </div>
    </div>
  );
}

