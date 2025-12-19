import React, { useState, useEffect } from 'react';

export default function PilotsPage() {
  const [pilots, setPilots] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiUrl = "http://127.0.0.1:8000/api/pilot/pilots/";
    const token = localStorage.getItem('access_token');

    if (!token) {
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
        if (!response.ok) throw new Error("Data error");
        return response.json();
    })
    .then(data => {
        setPilots(data);
        setLoading(false);
    })
    .catch(error => {
        console.error("Error:", error);
        setLoading(false);
    });
  }, []);

  if (loading) return <div className="page-container"><p>Pilot datas are loading...</p></div>;

  return (
    <div className="page-container">
      <h2 className="page-title">Pilotlar</h2>
      <div className="card">
        <table className="styled-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Pilot Name</th>
              <th>Seniority Level</th>
              <th>Age</th>
              <th>Known Languages</th>
              <th>Vehicle Restriction</th>
            </tr>
          </thead>
          <tbody>
            {pilots.map(pilot => (
              <tr key={pilot.id}>
                <td>#{pilot.id}</td>

                {/* Serializer'da direkt 'name' alanı var */}
                <td style={{fontWeight: 'bold'}}>{pilot.name}</td>

                {/* Seniority Level */}
                <td>
                    <span className={`ticket-badge ${pilot.seniority_level?.toLowerCase()}`}>
                        {pilot.seniority_level}
                    </span>
                </td>

                <td>{pilot.age} / {pilot.nationality}</td>

                {/* Languages bir array obje olarak geliyor, içinden isimleri alıp birleştiriyoruz */}
                <td>
                    {pilot.languages && pilot.languages.length > 0
                        ? pilot.languages.map(l => l.language_name).join(', ')
                        : <span style={{color:'#999'}}>-</span>
                    }
                </td>

                {/* Vehicle Restriction */}
                <td>{pilot.vehicle_restriction || "Yok"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}