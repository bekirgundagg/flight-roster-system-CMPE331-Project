import React, { useState } from 'react';
// Eğer routing için react-router-dom kullanıyorsanız navigate eklemeliyiz
// Kullanmıyorsanız bu satırı silip aşağıda window.location kullanabiliriz
import { useNavigate } from 'react-router-dom';
import './LoginPage.css'; // CSS dosyanın yolu

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  // Yönlendirme kancası (React Router kullanıyorsanız)
  // Kullanmıyorsanız aşağıdaki yorum satırlarını okuyun
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      // 1. Backend'e Kullanıcı Adı ve Şifreyi gönderiyoruz
      // URL'İ KONTROL ET: Senin projenin login url'i neyse onu yaz
      const response = await fetch('http://127.0.0.1:8000/api/token/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // 2. BAŞARILI! Gelen Token'ı Local Storage'a kaydediyoruz
        // Backend'den genellikle 'access' veya 'token' adıyla gelir.
        // Django SimpleJWT kullanıyorsanız 'access' olarak gelir.
        console.log("Giriş Başarılı, Token:", data.access);

        localStorage.setItem('access_token', data.access);

        // Varsa Refresh token'ı da alalım (uzun oturumlar için)
        if (data.refresh) {
            localStorage.setItem('refresh_token', data.refresh);
        }

        // 3. Kullanıcıyı Dashboard'a veya Yolcu listesine yönlendir
        navigate('/dashboard');
        // react-router yoksa: window.location.href = '/passengers';
      } else {
        // Hata varsa ekrana yaz
        setError('Giriş başarısız! Kullanıcı adı veya şifre yanlış.');
      }
    } catch (err) {
      console.error("Login Hatası:", err);
      setError('Sunucuya bağlanılamadı.');
    }
  };

  return (
    <div className="login-container"> {/* CSS class ismini senin dosyanla eşleştir */}
      <div className="login-card">
        <h2>SkyTeam System</h2>
        <p>Please login to continue</p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && <p style={{ color: 'red', fontSize: '14px' }}>{error}</p>}

          <button type="submit" className="login-button">Login</button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;