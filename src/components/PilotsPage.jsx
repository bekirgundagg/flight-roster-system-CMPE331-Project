import pilots from "../assets/data/pilot.json";

export default function PilotsPage() {
  return (
    <div className="page-container">
      <h2 className="page-title">Pilots</h2>
      <p className="page-subtitle">Pilot information is retrieved from the system database.</p>

      <div className="card">
        <table className="styled-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Rank</th>
              <th>Flight Hours</th>
              <th>License ID</th>
            </tr>
          </thead>
          <tbody>
            {pilots.map(p => (
              <tr key={p.id}>
                <td>{p.id}</td>
                <td>{p.name}</td>
                <td>{p.rank}</td>
                <td>{p.flightHours}</td>
                <td>{p.licenseId}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
