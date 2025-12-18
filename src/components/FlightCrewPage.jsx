import React, { useState, useEffect } from 'react';

export default function FlightCrewPage() {
  const [crewMembers, setCrewMembers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // URL NOTU: Eğer veriler gelmezse, tarayıcıda bu adrese git.
    // Pilot ve Flight sayfalarındaki gibi bir alt klasör (api/crew/crews/) olabilir.
    // Şimdilik senin verdiğin adresi kullanıyorum.
    const apiUrl = "http://127.0.0.1:8000/api/crew/";
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
        if (response.status === 401) {
            localStorage.removeItem('access_token');
            window.location.href = '/';
            throw new Error("Oturum süresi doldu.");
        }
        if (!response.ok) throw new Error("Veri hatası");
        return response.json();
    })
    .then(data => {
        // Eğer API paginated (sayfalı) dönerse veri data.results içinde olabilir.
        // Array mi yoksa Obje mi geldiğini kontrol edip set ediyoruz.
        const crewData = Array.isArray(data) ? data : (data.results || []);
        console.log("Kabin Ekibi Verisi:", crewData);
        setCrewMembers(crewData);
        setLoading(false);
    })
    .catch(error => {
        console.error("Fetch Hatası:", error);
        setLoading(false);
    });
  }, []);

  if (loading) return <div className="page-container"><p>Kabin ekibi yükleniyor...</p></div>;

  return (
    <div className="page-container">
      <h2 className="page-title">Uçuş Ekibi (Cabin Crew)</h2>
      <div className="card">
        <table className="styled-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>İsim</th>
              <th>Rol / Kıdem</th>
              <th>Yaş / Uyruk</th>
              <th>Bildiği Diller</th>
              <th>Kısıtlamalar / Tarifler</th>
            </tr>
          </thead>
          <tbody>
            {crewMembers.map(member => (
              <tr key={member.attendant_id}>
                <td style={{fontWeight:'bold'}}>#{member.attendant_id}</td>

                <td>
                    {member.name} <br/>
                    <small style={{color:'#666'}}>{member.gender}</small>
                </td>

                {/* Rol ve Kıdem */}
                <td>
                    <span className={`ticket-badge ${member.attendant_type}`}>
                        {member.attendant_type.toUpperCase()}
                    </span>
                    <div style={{fontSize:'12px', marginTop:'5px', color:'#555'}}>
                        {member.seniority_level}
                    </div>
                </td>

                <td>{member.age} / {member.nationality}</td>

                {/* Diller (Array Mapping) */}
                <td>
                    {member.known_languages && member.known_languages.length > 0
                        ? member.known_languages.map(l => l.lan_name).join(', ')
                        : <span style={{color:'#ccc'}}>-</span>
                    }
                </td>

                {/* Araç Kısıtlamaları veya Chef Tarifleri */}
                <td>
                   {/* Araç Kısıtlamaları */}
                   {member.vehicle_restrictions && member.vehicle_restrictions.length > 0 && (
                       <div style={{marginBottom:'5px'}}>
                           <strong>Araç: </strong>
                           {member.vehicle_restrictions.map(v => v.type_veh).join(', ')}
                       </div>
                   )}

                   {/* Eğer Chef ise Tariflerini göster */}
                   {member.attendant_type === 'chef' && member.recipes && member.recipes.length > 0 && (
                       <div style={{color: '#d35400'}}>
                           <strong>Recipes: </strong>
                           {member.recipes.map(r => r.recipe_name).join(', ')}
                       </div>
                   )}

                   {/* İkisi de yoksa tire koy */}
                   {(!member.vehicle_restrictions?.length && !member.recipes?.length) && "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}