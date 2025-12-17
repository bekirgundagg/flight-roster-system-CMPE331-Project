import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './FlightDashboard.css';

export default function FlightRosterPage() {
  const { flightNo } = useParams();
  const navigate = useNavigate();

  const [rosterData, setRosterData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // --- HATA BURADAYDI: Bu satırları buradan kaldırdık ---
  // Çünkü burada henüz 'flight' verisi yok!

  useEffect(() => {
    const apiUrl = `http://127.0.0.1:8000/api/flights/roster/${flightNo}/`;
    const token = localStorage.getItem('access_token');

    if (!token) {
        navigate('/');
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
        setRosterData(data);
        setLoading(false);
    })
    .catch(err => {
        setError(err.message);
        setLoading(false);
    });
  }, [flightNo, navigate]);

  // Otomatik Atama Fonksiyonu (Auto Assign)
  const handleAutoAssign = () => {
    const token = localStorage.getItem('access_token');
    // URL'in senin backend urls.py ile uyumlu olduğundan emin ol
    fetch(`http://127.0.0.1:8000/api/flights/roster/${flightNo}/auto-assign/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            alert("Ekip başarıyla atandı! Sayfa yenileniyor...");
            window.location.reload();
        } else {
            alert("Hata: " + (data.message || data.error));
        }
    })
    .catch(err => alert("Bağlantı hatası"));
  };

  if (loading) return <div className="page-container"><p>Veriler yükleniyor...</p></div>;
  if (error) return <div className="page-container"><p style={{color:'red'}}>Hata: {error}</p></div>;

  // BU SATIR KRİTİK: Eğer veri yoksa (null), aşağıya geçme ve boş dön.
  if (!rosterData) return null;

  // --- VERİLER GELDİKTEN SONRA ---
  // Değişkenleri burada tanımlıyoruz (Destructuring)
  const { flight, passengers, crew } = rosterData;

  // --- PLANE VIEW HESAPLAMALARINI BURAYA TAŞIDIK ---
  // Artık 'flight' verisi elimizde olduğu için güvenle hesap yapabiliriz.

  const columnsLeft = ['A', 'B', 'C'];
  const columnsRight = ['D', 'E', 'F'];

  // Dinamik Hesaplama:
  const seatCount = flight.vehicle_type?.seat_count || 180;
  const seatsPerRow = 6;
  const totalRows = Math.ceil(seatCount / seatsPerRow);

  const getPassengerBySeat = (seatNo) => {
    if (!passengers) return null;
    return passengers.find(p => p.seat_number === seatNo);
  };

  const renderSeat = (rowNum, colLetter) => {
    const seatId = `${rowNum}${colLetter}`;
    const passenger = getPassengerBySeat(seatId);
    const isOccupied = !!passenger;
    const seatClass = isOccupied ? `occupied ${passenger.seat_type?.toLowerCase()}` : 'empty';

    return (
      <div key={seatId} className={`seat ${seatClass}`}>
        {!isOccupied && seatId}
        <div className="tooltip">
            {isOccupied ? (
                <>
                    <strong>{passenger.full_name}</strong>
                    <br />
                    {passenger.nationality} / {passenger.age}y
                    <br />
                    <small>{passenger.seat_type}</small>
                </>
            ) : (
                <>
                    <strong>{seatId}</strong>
                    <br />
                    <span style={{color: '#aaa'}}>Boş (Empty)</span>
                </>
            )}
        </div>
      </div>
    );
  };

  return (
    <div className="page-container">
      {/* BAŞLIK */}
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px'}}>
        <div>
           <h2 className="page-title">Flight Roster – {flight.flight_number}</h2>
           <p className="page-subtitle">
             {flight.source_airport?.city} ➝ {flight.destination_airport?.city}
           </p>
           <p style={{color:'#666', fontSize:'14px'}}>
             {new Date(flight.departure_datetime).toLocaleString('tr-TR')} | {flight.vehicle_type?.model_name} ({seatCount} seats)
           </p>
        </div>
        <button className="action-btn" onClick={() => navigate(-1)}>Geri Dön</button>
      </div>

      <div className="roster-layout">

        {/* SOL SÜTUN */}
        <div className="roster-left">

            {/* 1. EKİP LİSTESİ */}
            <div className="card">
                <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'10px'}}>
                    <h3>Flight Crew & Pilots</h3>

                    {/* AUTO ASSIGN BUTONU */}
                    {crew.length === 0 && (
                        <button
                            onClick={handleAutoAssign}
                            style={{
                                backgroundColor: '#27ae60',
                                color: 'white',
                                border: 'none',
                                padding: '8px 15px',
                                borderRadius: '5px',
                                cursor: 'pointer',
                                fontWeight: 'bold'
                            }}
                        >
                            🤖 Otomatik Ata
                        </button>
                    )}
                </div>

                {crew.length > 0 ? (
                <table className="styled-table">
                    <thead>
                    <tr>
                        <th>Type</th>
                        <th>Name</th>
                        <th>Role</th>
                    </tr>
                    </thead>
                    <tbody>
                    {crew.map((member) => (
                        <tr key={`${member.type}-${member.id}`}>
                        <td>
                            <span style={{ fontSize: '1.2em', marginRight: '8px' }}>{member.avatar}</span>
                            <span style={{ fontWeight: 'bold' }}>{member.type}</span>
                        </td>
                        <td>{member.name}</td>
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
                <p style={{padding:'20px', color:'#999'}}>
                    Atama yapılmamış. Otomatik atama yapmak için butona tıklayın.
                </p>
                )}
            </div>

            {/* 2. YOLCU LİSTESİ */}
            <div className="card" style={{marginTop:'20px'}}>
                <h3>Passengers ({passengers.length})</h3>
                {passengers.length > 0 ? (
                    <table className="styled-table">
                    <thead>
                        <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Seat</th>
                        <th>Info</th>
                        </tr>
                    </thead>
                    <tbody>
                        {passengers.map(p => (
                        <tr key={p.id}>
                            <td>#{p.id}</td>
                            <td style={{fontWeight:'bold'}}>{p.full_name} {p.is_infant ? "👶" : ""}</td>
                            <td>
                                <span className={`ticket-badge ${p.seat_type?.toLowerCase()}`}>
                                    {p.seat_number || "-"}
                                </span>
                            </td>
                            <td>{p.nationality} / {p.gender} / {p.age}y</td>
                        </tr>
                        ))}
                    </tbody>
                    </table>
                ) : (
                    <p style={{padding:'20px'}}>Yolcu yok.</p>
                )}
            </div>
        </div>

        {/* SAĞ SÜTUN: UÇAK PLANI */}
        <div className="roster-right">
            <div className="card" style={{textAlign:'center', padding: '10px'}}>
                <h3>Seat Map</h3>
                <p style={{fontSize:'12px', color:'#666', marginBottom:'15px'}}>
                    <span style={{color:'#2c3e50'}}>■ Biz</span>
                    <span style={{color:'#3498db', marginLeft:'5px'}}>■ Eco</span>
                    <span style={{color:'#ccc', marginLeft:'5px'}}>■ Empty</span>
                </p>

                <div className="plane-fuselage">
                    <div style={{marginBottom:'20px', borderBottom:'2px dashed #ccc', color:'#999', fontSize:'10px'}}>
                    COCKPIT
                    </div>

                    {Array.from({ length: totalRows }, (_, i) => i + 1).map(row => (
                        <div key={row} className="seat-row">
                            <div className="seat-group">
                                {columnsLeft.map(col => renderSeat(row, col))}
                            </div>
                            <div className="aisle">{row}</div>
                            <div className="seat-group">
                                {columnsRight.map(col => renderSeat(row, col))}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>

      </div>
    </div>
  );
}