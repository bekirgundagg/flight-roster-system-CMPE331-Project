import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // Geri butonu için ekledim (Opsiyonel)

export default function PassengersPage() {
  const [passengers, setPassengers] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate(); // Geri butonu için

  useEffect(() => {
    const apiUrl = "http://127.0.0.1:8000/api/passengers/";
    const token = localStorage.getItem('access_token');

    if (!token) {
        console.warn("Missing Token, redirecting to login page...");
        window.location.href = '/';
        return;
    }

    fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    })
    .then(response => {
        if (response.status === 401) {
            localStorage.removeItem('access_token');
            window.location.href = '/';
            throw new Error("The session has expired.");
        }
        return response.json();
    })
    .then(data => {
        setPassengers(data);
        setLoading(false);
    })
    .catch(error => {
        console.error("Error:", error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="page-container"><p>Loading...</p></div>;
  }

  return (
    <div className="page-container">
      {/* Başlık ve Geri Butonu */}
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px'}}>
        <div>
            <h2 className="page-title">Passenger List</h2>
            <p className="page-subtitle">Real-time flight passenger records and statuses.</p>
        </div>
        <button className="action-btn" onClick={() => navigate('/dashboard')}>Back to Dashboard</button>
      </div>

      <div className="card">
        <table className="styled-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Passenger Info</th>
              <th>Age / Gender</th>
              <th>Nationality</th>
              <th>Seat Type</th>
              <th>Flight Number</th>
            </tr>
          </thead>
          <tbody>
            {passengers.map(p => (
              <tr key={p.id}>
                <td>#{p.id}</td>

                {/* --- İSİM VE EBEVEYN BİLGİSİ --- */}
                <td>
                  <div style={{ display: 'flex', flexDirection: 'column' }}>
                    <span style={{ fontWeight: 'bold' }}>
                      {p.full_name} {p.is_infant && "👶"}
                    </span>

                    <span style={{ fontSize: '12px', color: '#666' }}>
                      {p.email || "no E-mail"}
                    </span>

                    {/* YENİ EKLENEN KISIM: Ebeveyn Gösterimi */}
                    {p.is_infant && p.parent_name && (
                        <span style={{ fontSize: '0.8em', color: '#e67e22', marginTop: '3px', fontWeight: 'bold' }}>
                            Parent: {p.parent_name}
                        </span>
                    )}
                  </div>
                </td>

                <td>{p.age} / {p.gender}</td>
                <td>{p.nationality}</td>

                <td>
                  <span className={`ticket-badge ${p.seat_type ? p.seat_type.toLowerCase() : ''}`}>
                    {p.seat_type === 'business' ? 'Business' : 'Economy'}
                  </span>
                  {p.seat_number && <span style={{marginLeft:'5px', fontSize:'12px'}}>({p.seat_number})</span>}
                </td>

                <td>{p.flight_id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}