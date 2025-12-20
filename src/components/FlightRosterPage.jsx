import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './FlightDashboard.css';

export default function FlightRosterPage() {
  const { flightNo } = useParams();
  const navigate = useNavigate();

  const [rosterData, setRosterData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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
    fetch(`http://127.0.0.1:8000/api/flights/roster/${flightNo}/auto-assign/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            alert("The team has been successfully assigned! Page is refreshing....");
            window.location.reload();
        } else {
            alert("Hata: " + (data.message || data.error));
        }
    })
    .catch(err => alert("Connection Error"));
  };

  // --- YENİ: JSON Export Fonksiyonu ---
  const handleExportJson = () => {
    if (!rosterData) return;

    const fileName = `Roster-${rosterData.flight.flight_number}.json`;

    // 2. Veriyi JSON string'e çevir
    const jsonString = JSON.stringify(rosterData, null, 2);

    // 3. Blob oluştur
    const blob = new Blob([jsonString], { type: "application/json" });

    // 4. İndirme bağlantısı oluştur ve tıkla
    const href = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = href;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();

    // 5. Temizlik
    document.body.removeChild(link);
    URL.revokeObjectURL(href);
  };

  if (loading) return <div className="page-container"><p>Veriler yükleniyor...</p></div>;
  if (error) return <div className="page-container"><p style={{color:'red'}}>Hata: {error}</p></div>;
  if (!rosterData) return null;

  // --- VERİLER GELDİKTEN SONRA ---
  const { flight, passengers, crew, menu } = rosterData;

  // --- EXTENDED VIEW: EKİBİ AYRIŞTIRMA ---
  const pilots = crew.filter(c => c.type === 'Pilot');
  const cabinCrew = crew.filter(c => c.type === 'Cabin Crew');

  // --- PLANE VIEW HESAPLAMALARINI ---
  const columnsLeft = ['A', 'B', 'C'];
  const columnsRight = ['D', 'E', 'F'];

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

  // İlk 5 sıra Business kabul edilsin
  const isBusinessRow = rowNum <= 5;

  // Class belirleme mantığı:
  // 1. Doluysa: Yolcunun tipine göre (business/economy) renk alıyor (Eski mantık).
  // 2. Boşsa ve Business sırasındaysa: 'empty-business' (Sarı) oluyor.
  // 3. Boşsa ve Economy sırasındaysa: 'empty' (Standart) oluyor.
  let seatClass;
  if (isOccupied) {
      seatClass = `occupied ${passenger.seat_type?.toLowerCase()}`;
  } else {
      seatClass = isBusinessRow ? 'empty-business' : 'empty';
  }

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
                  {/* Yolcu varsa veritabanındaki tipi yazar */}
                  <small>{passenger.seat_type}</small>
              </>
          ) : (
              <>
                  <strong>{seatId}</strong>
                  <br />
                  <span style={{color: '#aaa'}}>
                      {/* Boşsa sıraya göre tipini yazar */}
                      {isBusinessRow ? 'Business (Empty)' : 'Economy (Empty)'}
                  </span>
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
        <button className="action-btn" onClick={() => navigate(-1)}>Go Back</button>
      </div>

      <div className="roster-layout">

        {/* SOL SÜTUN */}
        <div className="roster-left">

            {/* BUTONLAR VE BAŞLIK ALANI */}
            <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'15px'}}>
               <h3 style={{margin:0}}>Flight Roster Details</h3>
               <div style={{display:'flex', gap:'10px'}}>
                   {/* OTO ATA BUTONU (Sadece liste boşsa) */}
                   {crew.length === 0 && (
                        <button
                            onClick={handleAutoAssign}
                            className="action-btn"
                            style={{backgroundColor: '#27ae60'}} // Yeşil
                        >
                            Auto Assign
                        </button>
                   )}

                   {/* EXPORT JSON BUTONU (Her zaman görünür) */}
                   <button
                        onClick={handleExportJson}
                        className="action-btn"
                        style={{backgroundColor: '#e67e22'}} // Turuncu
                   >
                        Export JSON
                   </button>
               </div>
            </div>

            {/* 1. TABLO: PİLOTLAR */}
            <div className="card" style={{marginBottom:'20px'}}>
                <h4>Pilots</h4>
                {pilots.length > 0 ? (
                <table className="styled-table">
                    <thead>
                    <tr>
                        <th>Icon</th>
                        <th>Name</th>
                        <th>Seniority</th>
                    </tr>
                    </thead>
                    <tbody>
                    {pilots.map((member) => (
                        <tr key={`pilot-${member.id}`}>
                        <td style={{fontSize: '1.5em'}}>{member.avatar}</td>
                        <td style={{fontWeight:'bold'}}>{member.name}</td>
                        <td>
                            <span className="ticket-badge business">
                                {member.role}
                            </span>
                        </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
                ) : (
                    <p style={{color:'#999', padding:'10px'}}>No pilot has been assigned yet.</p>
                )}
            </div>

            {/* 2. TABLO: KABİN EKİBİ */}
            <div className="card" style={{marginBottom:'20px'}}>
                <h4>Cabin Crew</h4>
                {cabinCrew.length > 0 ? (
                <table className="styled-table">
                    <thead>
                    <tr>
                        <th>Icon</th>
                        <th>Name</th>
                        <th>Role</th>
                    </tr>
                    </thead>
                    <tbody>
                    {cabinCrew.map((member) => (
                        <tr key={`crew-${member.id}`}>
                        <td style={{fontSize: '1.5em'}}>{member.avatar}</td>
                        <td>{member.name}</td>
                        <td>
                            <span className={`ticket-badge ${member.role === 'chef' ? 'business' : 'economy'}`}>
                                {member.role}
                            </span>
                        </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
                ) : (
                    <p style={{color:'#999', padding:'10px'}}>No Crew has been assigned yet.</p>
                )}
            </div>

            {/* 3. MENÜ KARTI */}
            <div className="card" style={{marginBottom:'20px'}}>
                <h3>In-Flight Menu 🍽️</h3>
                {menu && menu.length > 0 ? (
                    <ul style={{listStyle:'none', padding:0, marginTop:'10px'}}>
                        {menu.map((item, index) => (
                            <li key={index} style={{
                                padding: '10px',
                                borderBottom: '1px solid #eee',
                                display: 'flex',
                                alignItems: 'center'
                            }}>
                                <span style={{fontSize:'1.5em', marginRight:'10px'}}>
                                    {item.type === "Chef's Special" ? "👨‍🍳" : "🍱"}
                                </span>
                                <div>
                                    <div style={{fontWeight:'bold', color: '#2c3e50'}}>
                                        {item.name}
                                    </div>
                                    {item.chef && (
                                        <div style={{fontSize:'12px', color:'#e67e22', fontStyle:'italic'}}>
                                            ★ Chef's Special by {item.chef}
                                        </div>
                                    )}
                                </div>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p style={{padding:'10px', color:'#999'}}>No Recipe has been assigned yet.</p>
                )}
            </div>

            {/* 4. YOLCU LİSTESİ */}
            <div className="card">
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
                    {p.is_infant && p.parent_name && (
                        <span style={{ fontSize: '0.8em', color: '#e67e22', marginTop: '3px', fontWeight: 'bold', marginLeft: '100px'}}>
                            Parent: {p.parent_name}
                        </span>
                    )}
                            </td>
                            <td>{p.nationality} / {p.gender} / {p.age}y</td>
                        </tr>
                        ))}
                    </tbody>
                    </table>
                ) : (
                    <p style={{padding:'20px'}}>No passengers.</p>
                )}
            </div>
        </div>

        {/* SAĞ SÜTUN: UÇAK PLANI */}
        <div className="roster-right">
            <div className="card" style={{textAlign:'center', padding: '10px'}}>
                <h3>Seat Map</h3>
                <p style={{fontSize:'12px', color:'#666', marginBottom:'15px'}}>
                    <span style={{color:'#2c3e50'}}>■ Business</span>
                    <span style={{color:'#3498db', marginLeft:'5px'}}>■ Eco</span>
                    <span style={{color:'#f1c40f', marginLeft:'5px'}}>■ Empty Business</span>
                    <span style={{color:'#ccc', marginLeft:'5px'}}>■ Empty Eco</span>

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