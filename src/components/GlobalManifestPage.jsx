import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './FlightDashboard.css';

export default function GlobalManifestPage() {
  const navigate = useNavigate();
  const [people, setPeople] = useState([]);
  const [loading, setLoading] = useState(true);

  // FİLTRELEME STATE'LERİ
  const [filterType, setFilterType] = useState('All'); // All, Pilot, Cabin Crew, Passenger
  const [searchTerm, setSearchTerm] = useState(''); // İsimle arama
  const [roleFilter, setRoleFilter] = useState(''); // Senior, Business vb. arama

  // SAYFALAMA
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 15; // Listede 15 kişi göster

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    fetch('http://127.0.0.1:8000/api/flights/global-manifest/', {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(res => res.json())
    .then(data => {
        setPeople(data);
        setLoading(false);
    })
    .catch(err => {
        console.error(err);
        setLoading(false);
    });
  }, []);

  // --- GELİŞMİŞ FİLTRELEME MANTIĞI ---
  const filteredPeople = people.filter(person => {
    // 1. Tip Filtresi (Pilot mu Yolcu mu?)
    if (filterType !== 'All' && person.type !== filterType) return false;
    
    // 2. İsim Arama (Ahmet, Bekir...)
    if (searchTerm && !person.name.toLowerCase().includes(searchTerm.toLowerCase())) return false;

    // 3. Rol/Flight Arama (HB1001, Senior, Business...)
    if (roleFilter && !JSON.stringify(person).toLowerCase().includes(roleFilter.toLowerCase())) return false;

    return true;
  });

  // SAYFALAMA HESAPLARI
  const totalPages = Math.ceil(filteredPeople.length / itemsPerPage);
  const currentItems = filteredPeople.slice(
    (currentPage - 1) * itemsPerPage, 
    currentPage * itemsPerPage
  );

  if (loading) return <div className="page-container"><p>Loading Global Data...</p></div>;

  return (
    <div className="page-container">
      <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'20px'}}>
        <div>
           <h2 className="page-title">🌍 Global Roster Management</h2>
           <p className="page-subtitle">All Personnel & Passengers across All Flights</p>
        </div>
        <button className="action-btn" onClick={() => navigate('/dashboard')}>Back to Dashboard</button>
      </div>

      <div className="card">
        {/* --- KONTROL PANELİ (Filtreler) --- */}
        <div style={{
            display:'flex', gap:'15px', flexWrap:'wrap', 
            background:'#f8f9fa', padding:'15px', borderRadius:'10px', marginBottom:'20px'
        }}>
            
            {/* 1. TİP SEÇİMİ */}
            <div>
                <label style={{fontWeight:'bold', display:'block', marginBottom:'5px'}}>Filter by Type:</label>
                <div className="filter-buttons" style={{display:'flex', gap:'5px'}}>
                    {['All', 'Pilot', 'Cabin Crew', 'Passenger'].map(type => (
                        <button 
                            key={type}
                            onClick={() => { setFilterType(type); setCurrentPage(1); }}
                            style={{
                                padding: '6px 12px',
                                border: '1px solid #ddd',
                                borderRadius: '20px',
                                backgroundColor: filterType === type ? '#3498db' : 'white',
                                color: filterType === type ? 'white' : '#333',
                                cursor: 'pointer'
                            }}
                        >
                            {type}
                        </button>
                    ))}
                </div>
            </div>

            {/* 2. İSİM ARAMA */}
            <div style={{flex:1, minWidth:'200px'}}>
                <label style={{fontWeight:'bold', display:'block', marginBottom:'5px'}}>Search Name:</label>
                <input 
                    type="text" 
                    placeholder="e.g. Ahmet, John..." 
                    value={searchTerm}
                    onChange={e => setSearchTerm(e.target.value)}
                    style={{width:'100%', padding:'8px', borderRadius:'5px', border:'1px solid #ccc'}}
                />
            </div>

            {/* 3. DETAY ARAMA (Uçuş No veya Rol) */}
            <div style={{flex:1, minWidth:'200px'}}>
                <label style={{fontWeight:'bold', display:'block', marginBottom:'5px'}}>Search Flight / Role:</label>
                <input 
                    type="text" 
                    placeholder="e.g. HB1001, Senior, Business..." 
                    value={roleFilter}
                    onChange={e => setRoleFilter(e.target.value)}
                    style={{width:'100%', padding:'8px', borderRadius:'5px', border:'1px solid #ccc'}}
                />
            </div>
        </div>

        {/* --- TABLO --- */}
        <div style={{overflowX: 'auto'}}>
            <table className="styled-table" style={{width:'100%'}}>
                <thead>
                    <tr>
                        <th>Ava</th>
                        <th>Name</th>
                        <th>Type</th>
                        <th>Role / Seat</th>
                        <th>Flight No</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {currentItems.length > 0 ? (
                        currentItems.map((person) => (
                            <tr key={person.unique_id}>
                                <td style={{fontSize:'1.5em', textAlign:'center'}}>{person.avatar}</td>
                                <td style={{fontWeight:'bold'}}>{person.name}</td>
                                
                                {/* TİP BADGE */}
                                <td>
                                    <span className={`ticket-badge ${person.type === 'Passenger' ? 'economy' : 'business'}`}
                                          style={{
                                              backgroundColor: person.type === 'Pilot' ? '#2c3e50' : 
                                                              (person.type === 'Passenger' ? '#95a5a6' : '#e67e22')
                                          }}>
                                        {person.type}
                                    </span>
                                </td>

                                {/* ROL / KOLTUK */}
                                <td>
                                    {person.type === 'Passenger' ? (
                                        <span>
                                            {person.role} 
                                            {person.seat && <b style={{marginLeft:'5px', color:'#2980b9'}}>({person.seat})</b>}
                                        </span>
                                    ) : (
                                        <span style={{textTransform:'capitalize'}}>{person.role}</span>
                                    )}
                                </td>

                                {/* UÇUŞ BİLGİSİ (ÖNEMLİ!) */}
                                <td style={{color:'#8e44ad', fontWeight:'bold'}}>{person.flight}</td>
                                <td>{person.date}</td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="6" style={{textAlign:'center', padding:'30px', color:'#999'}}>
                                No records found matching your filters.
                            </td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>

        {/* --- SAYFALAMA --- */}
        {totalPages > 1 && (
            <div style={{display:'flex', justifyContent:'center', marginTop:'20px', gap:'10px'}}>
                <button 
                    disabled={currentPage === 1}
                    onClick={() => setCurrentPage(p => p - 1)}
                    className="action-btn"
                    style={{padding:'5px 15px', backgroundColor: currentPage===1?'#ccc':'#3498db'}}
                >
                    Previous
                </button>
                <span style={{lineHeight:'30px', fontWeight:'bold'}}> Page {currentPage} / {totalPages} </span>
                <button 
                    disabled={currentPage === totalPages}
                    onClick={() => setCurrentPage(p => p + 1)}
                    className="action-btn"
                    style={{padding:'5px 15px', backgroundColor: currentPage===totalPages?'#ccc':'#3498db'}}
                >
                    Next
                </button>
            </div>
        )}
      </div>
    </div>
  );
}