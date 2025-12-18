import React, { useState, useEffect } from 'react';

export default function PassengersPage() {
  const [passengers, setPassengers] = useState([]);
  const [loading, setLoading] = useState(true);

  // useEffect bloğunun içi:
  useEffect(() => {
    const apiUrl = "http://127.0.0.1:8000/api/passengers/";

    // 1. Token'ı cepten çıkar
    const token = localStorage.getItem('access_token');

    // Token yoksa login'e geri postala
    if (!token) {
        console.warn("Token yok, login sayfasına yönlendiriliyor...");
        // React Router kullanıyorsan: navigate('/login');
        // Kullanmıyorsan:
        window.location.href = '/';
        return;
    }

    fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        // 2. Token'ı göster (Bearer şeması standarttır)
        'Authorization': `Bearer ${token}`
      }
    })
    .then(response => {
        // Eğer Token süresi dolmuşsa (401), kullanıcıyı logine at
        if (response.status === 401) {
            localStorage.removeItem('access_token'); // Çürük token'ı sil
            window.location.href = '/';
            throw new Error("Oturum süresi doldu.");
        }
        return response.json();
    })
    .then(data => {
        setPassengers(data);
        setLoading(false);
    })
    // ... catch bloğu aynı
      .catch(error => {
        console.error("Hata:", error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="page-container"><p>Yükleniyor...</p></div>;
  }

  return (
    <div className="page-container">
      <h2 className="page-title">Yolcu Listesi</h2>
      <p className="page-subtitle">Anlık uçuş yolcu kayıtları ve durumları.</p>

      <div className="card">
        <table className="styled-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Yolcu Bilgisi</th>
              <th>Yaş / Cinsiyet</th>
              <th>Milliyet</th>
              <th>Koltuk Tipi</th>
              <th>Uçuş No</th>
            </tr>
          </thead>
          <tbody>
            {passengers.map(p => (
              <tr key={p.id}>
                <td>#{p.id}</td>

                {/* İsim ve Bebek Kontrolü */}
                <td>
                  <div style={{ display: 'flex', flexDirection: 'column' }}>
                    <span style={{ fontWeight: 'bold' }}>
                      {p.full_name} {p.is_infant && "👶"}
                    </span>
                    <span style={{ fontSize: '12px', color: '#666' }}>
                      {p.email || "E-posta yok"}
                    </span>
                  </div>
                </td>

                <td>{p.age} / {p.gender}</td>

                {/* Modelde 'passport' yoktu, 'nationality' ekledik */}
                <td>{p.nationality}</td>

                <td>
                  {/* Business/Economy renklendirmesi */}
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