import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './FlightDashboard.css';

export default function GlobalManifestPage() {
  const navigate = useNavigate();
  const [people, setPeople] = useState([]);
  const [loading, setLoading] = useState(true);

  // --- FİLTRE STATE'İ ---
  const [selectedFilters, setSelectedFilters] = useState([]);

  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 15;

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    // URL'ini kendi projene göre ayarla (api/main_system veya api/flights)
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

  // --- ÇOKLU SEÇİM FONKSİYONU ---
  const toggleFilter = (type) => {
    setCurrentPage(1);

    if (type === 'All') {
        setSelectedFilters([]);
        return;
    }

    if (selectedFilters.includes(type)) {
        setSelectedFilters(prev => prev.filter(item => item !== type));
    }
    else {
        setSelectedFilters(prev => [...prev, type]);
    }
  };

  // --- FİLTRELEME MANTIĞI ---
  const filteredPeople = people.filter(person => {

    // a) Tip Filtresi
    if (selectedFilters.length > 0 && !selectedFilters.includes(person.type)) {
        return false;
    }

    // b) İsim Arama
    if (searchTerm && !person.name.toLowerCase().includes(searchTerm.toLowerCase())) return false;

    // c) Rol/Flight Arama
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

  const filterOptions = ['Pilot', 'Cabin Crew', 'Passenger'];

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
        {/* --- KONTROL PANELİ --- */}
        <div style={{
            display:'flex', gap:'15px', flexWrap:'wrap',
            background:'#f8f9fa', padding:'15px', borderRadius:'10px', marginBottom:'20px'
        }}>

            {/* ÇOKLU SEÇİM BUTONLARI */}
            <div>
                <label style={{fontWeight:'bold', display:'block', marginBottom:'5px'}}>Filter by Type (Multi-select):</label>
                <div className="filter-buttons" style={{display:'flex', gap:'5px'}}>

                    {/* ALL BUTONU */}
                    <button
                        onClick={() => toggleFilter('All')}
                        style={{
                            padding: '6px 12px',
                            border: '1px solid #ddd',
                            borderRadius: '20px',
                            backgroundColor: selectedFilters.length === 0 ? '#2c3e50' : 'white',
                            color: selectedFilters.length === 0 ? 'white' : '#333',
                            cursor: 'pointer',
                            fontWeight: 'bold'
                        }}
                    >
                        All
                    </button>

                    {/* DİĞER TİPLER */}
                    {filterOptions.map(type => {
                        const isActive = selectedFilters.includes(type);
                        return (
                            <button
                                key={type}
                                onClick={() => toggleFilter(type)}
                                style={{
                                    padding: '6px 12px',
                                    border: '1px solid #ddd',
                                    borderRadius: '20px',
                                    backgroundColor: isActive ? '#3498db' : 'white',
                                    color: isActive ? 'white' : '#333',
                                    cursor: 'pointer',
                                    transition: 'all 0.2s'
                                }}
                            >
                                {type} {isActive && '✓'}
                            </button>
                        );
                    })}
                </div>
            </div>

            {/* İSİM ARAMA */}
            <div style={{flex:1, minWidth:'200px'}}>
                <label style={{fontWeight:'bold', display:'block', marginBottom:'5px'}}>Search Name:</label>
                <input
                    type="text"
                    placeholder="e.g. Ahmet, John..."
                    value={searchTerm}
                    onChange={e => { setSearchTerm(e.target.value); setCurrentPage(1); }}
                    style={{width:'100%', padding:'8px', borderRadius:'5px', border:'1px solid #ccc'}}
                />
            </div>

            {/* DETAY ARAMA */}
            <div style={{flex:1, minWidth:'200px'}}>
                <label style={{fontWeight:'bold', display:'block', marginBottom:'5px'}}>Search Flight / Role:</label>
                <input
                    type="text"
                    placeholder="e.g. HB1001, Senior..."
                    value={roleFilter}
                    onChange={e => { setRoleFilter(e.target.value); setCurrentPage(1); }}
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

                                {/* --- GÜNCELLENEN KISIM: İSİM, EBEVEYN VE ŞEF MENÜSÜ --- */}
                                <td>
                                    <div style={{display:'flex', flexDirection:'column'}}>
                                        <span style={{fontWeight:'bold'}}>{person.name}</span>

                                        {/* 1. Eğer bebekse ve ebeveyn ismi backend'den geldiyse göster */}
                                        {person.is_infant && person.parent_name && (
                                             <span style={{fontSize: '0.75em', color: '#e67e22', fontStyle:'italic'}}>
                                                Parent: {person.parent_name}
                                             </span>
                                        )}

                                        {/* 2. Eğer Şef ise ve Menü geldiyse göster */}
                                        {person.role === 'chef' && person.chef_menu && (
                                            <span style={{fontSize: '0.75em', color: '#e67e22', fontStyle:'italic', marginTop:'2px', display: 'block',maxWidth: '100px',whiteSpace: 'normal',lineHeight: '1.2'}}>
                                                {person.chef_menu}
                                            </span>
                                        )}
                                    </div>
                                </td>

                                <td>
                                    <span className={`ticket-badge ${person.type === 'Passenger' ? 'economy' : 'business'}`}
                                          style={{
                                              backgroundColor: person.type === 'Pilot' ? '#2c3e50' :
                                                              (person.type === 'Passenger' ? '#95a5a6' : '#e67e22')
                                          }}>
                                        {person.type}
                                    </span>
                                </td>

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