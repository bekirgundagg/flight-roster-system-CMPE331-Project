import crew from "../assets/data/crew.json";

export default function FlightCrewPage() {
  return (
    <div className="page-container">
      <h2 className="page-title">Flight Crew</h2>
      <p className="page-subtitle">Crew data is displayed in read-only mode.</p>

      <div className="card">
        <table className="styled-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Role</th>
              <th>Experience</th>
              <th>Contact</th>
            </tr>
          </thead>
          <tbody>
            {crew.map(c => (
              <tr key={c.id}>
                <td>{c.id}</td>
                <td>{c.name}</td>
                <td>{c.role}</td>
                <td>{c.experience}</td>
                <td>{c.contact}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
