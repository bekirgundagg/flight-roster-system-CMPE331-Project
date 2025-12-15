import passengers from "../assets/data/passengers.json";

export default function PassengersPage() {
  return (
    <div className="page-container">
      <h2 className="page-title">Passengers</h2>
      <p className="page-subtitle">Passenger records are shown for monitoring purposes.</p>

      <div className="card">
        <table className="styled-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Passport</th>
              <th>Country</th>
              <th>Ticket</th>
              <th>Flight</th>
            </tr>
          </thead>
          <tbody>
            {passengers.map(p => (
              <tr key={p.id}>
                <td>{p.id}</td>
                <td>{p.name}</td>
                <td>{p.passport}</td>
                <td>{p.country}</td>
                <td>
                  <span className={`ticket-badge ${p.ticket.toLowerCase()}`}>
                    {p.ticket}
                  </span>
                </td>
                <td>{p.flight}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
