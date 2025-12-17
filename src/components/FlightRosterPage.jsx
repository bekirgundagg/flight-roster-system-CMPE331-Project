import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

export default function FlightRosterPage() {
  const { flightNo } = useParams(); // URL'den uçuş numarasını (örn: HB0001) alır
  const navigate = useNavigate();

  const [rosterData, setRosterData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Backend'de yazdığımız yeni endpoint
    const apiUrl = `http://127.0.0.1:8000/api/flights/roster/${flightNo}/`;
    const token = localStorage.getItem('access_token');

    if (!token) {
        navigate('/'); // Token yoksa login'e at
        return;
    }

    fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    })
    .then(res => {
        if (!res.ok) throw new Error("Uçuş bilgileri çekilemedi");
        return res.json();
    })
    .then(data => {
        console.log("Roster Verisi:", data);
        setRosterData(data);
        setLoading(false);
    })
    .catch(err => {
        console.error(err);
        setError(err.message);
        setLoading(false);
    });
  }, [flightNo, navigate]);

  if (loading) return <div className="page-container"><p>Veriler yükleniyor...</p></div>;
  if (error) return <div className="page-container"><p style={{color:'red'}}>Hata: {error}</p></div>;
  if (!rosterData) return null;

  const { flight, passengers, crew } = rosterData;

  return (
    <div className="page-container">
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <div>
           <h2 className="page-title">Flight Roster – {flight.flight_number}</h2>
           <p className="page-subtitle">
             {flight.source_airport?.city} ({flight.source_airport?.code}) ➝ {flight.destination_airport?.city} ({flight.destination_airport?.code})
           </p>
           <p style={{color:'#666', fontSize:'14px'}}>
             Tarih: {new Date(flight.departure_datetime).toLocaleString('tr-TR')} |
             Uçak: {flight.vehicle_type?.model_name || "Belirtilmemiş"}
           </p>
        </div>
        <button className="action-btn" onClick={() => navigate(-1)}>Geri Dön</button>
      </div>

      {/* 1. KISIM: EKİP LİSTESİ (Tabular View) */}
      <div className="card" style={{marginTop:'20px'}}>
        <h3>Tabular View (Flight Crew & Pilots)</h3>
        {crew.length > 0 ? (
          <table className="styled-table">
            <thead>
              <tr>
                <th>Type</th>
                <th>Name</th>
                <th>Role</th>
              </tr>
            </thead>
            {/* GÜNCELLENEN KISIM BURASI */}
            <tbody>
              {crew.map((member) => (
                <tr key={`${member.type}-${member.id}`}> {/* Benzersiz key oluşturduk */}

                  {/* Tip ve İkon */}
                  <td>
                    <span style={{ fontSize: '1.2em', marginRight: '8px' }}>
                        {member.avatar}
                    </span>
                    <span style={{ fontWeight: 'bold' }}>
                        {member.type}
                    </span>
                  </td>

                  {/* İsim */}
                  <td>{member.name}</td>

                  {/* Rol (Badge rengini tipe göre değiştirdik) */}
                  <td>
                    <span className={`ticket-badge ${member.type === 'Pilot' ? 'business' : 'economy'}`}>
                      {member.role}
                    </span>
                  </td>

                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p style={{padding:'20px', color:'#999', fontStyle:'italic'}}>
            Bu uçuşa henüz pilot veya kabin ekibi atanmamış. (Backend ilişkisi bekleniyor)
          </p>
        )}
      </div>

      {/* 2. KISIM: YOLCU LİSTESİ (Gerçek Veri) */}
      <div className="card" style={{marginTop:'20px'}}>
        <h3>Passengers ({passengers.length})</h3>
        {passengers.length > 0 ? (
            <table className="styled-table">
            <thead>
                <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Seat / Type</th>
                <th>Info</th>
                </tr>
            </thead>
            <tbody>
                {passengers.map(p => (
                <tr key={p.id}>
                    <td>#{p.id}</td>
                    <td style={{fontWeight:'bold'}}>{p.full_name} {p.is_infant ? "👶" : ""}</td>
                    <td>{p.email || "-"}</td>
                    <td>
                        <span className={`ticket-badge ${p.seat_type?.toLowerCase()}`}>
                            {p.seat_type}
                        </span>
                        {p.seat_number && <span style={{marginLeft:'5px'}}>({p.seat_number})</span>}
                    </td>
                    <td>{p.nationality} / {p.gender} / {p.age}y</td>
                </tr>
                ))}
            </tbody>
            </table>
        ) : (
            <p style={{padding:'20px'}}>Bu uçuşta kayıtlı yolcu yok.</p>
        )}
      </div>
    </div>
  );
}