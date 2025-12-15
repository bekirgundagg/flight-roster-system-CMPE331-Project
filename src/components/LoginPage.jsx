import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {
    // ŞİMDİLİK FAKE LOGIN
    // Backend geldiğinde burası API call olacak
    if (username.trim() !== "" && password.trim() !== "") {
      navigate("/dashboard");
    } else {
      alert("Please enter username and password");
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1 className="login-title">SkyTeam System</h1>
        <p className="login-subtitle">Please login to continue</p>

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={handleLogin}>
          Login
        </button>
      </div>
    </div>
  );
}
