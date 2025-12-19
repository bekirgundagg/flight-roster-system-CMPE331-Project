import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function FlightsPage() {
  const [flights, setFlights] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const apiUrl = "http://127.0.0.1:8000/api/flights/flights/";
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
    .then(res => {
        if (!res.ok) throw new Error("Data Error");
        return res.json();
    })
    .then(data => {
        console.log("Flight datas:", data);
        setFlights(data);
        setLoading(false);
    })
    .catch(err => {
        console.error(err);
        setLoading(false);
    });
  }, []);

  const formatDate = (dateString) => {
    if (!dateString) return "-";
    const date = new Date(dateString);
    return date.toLocaleString('tr-TR', {
      day: '2-digit', month: '2-digit', year: 'numeric',
      hour: '2-digit', minute: '2-digit'
    });
  };

  if (loading) return <div className="page-container"><p>Flights are loading...</p></div>;

  return (
    <div className="page-container">
      <h2 className="page-title">Flight List</h2>
      <div className="card">
        <table className="styled-table">
          <thead>
            <tr>
              <th>Flight Number</th>
              <th>Soruce</th>
              <th>Destination</th>
              <th>Date</th>
              <th>Vehicle Type</th>
              <th>Duration</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            {flights.map(flight => (
              <tr key={flight.flight_number}>
                <td style={{fontWeight: 'bold'}}>{flight.flight_number}</td>

                {/* Serializer'da 'source_airport' bir obje olduğu için içindeki alanlara iniyoruz */}
                <td>
                    {flight.source_airport?.city} <br/>
                    <small style={{color: '#666'}}>({flight.source_airport?.code})</small>
                </td>

                <td>
                    {flight.destination_airport?.city} <br/>
                    <small style={{color: '#666'}}>({flight.destination_airport?.code})</small>
                </td>

                <td>{formatDate(flight.departure_datetime)}</td>

                {/* VehicleTypeSerializer'dan gelen model bilgisi (Not: modelde 'model_name' olduğunu varsaydım create metoduna bakarak) */}
                <td>{flight.vehicle_type?.model_name || flight.vehicle_type?.name || "-"}</td>

                <td>{flight.duration_minutes} min</td>

                <td>
                    <button
                        className="action-btn"
                        onClick={() => navigate(`/roster/${flight.flight_number}`)}
                    >
                        Show Details
                    </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}