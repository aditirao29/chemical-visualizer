function Summary({ data }) {
  const s = data.summary;

  return (
    <>
      <h2>Summary</h2>
      <div className="summary-grid">
        <div className="summary-card">
          <h3>Total Equipment</h3>
          <p>{s.total_count}</p>
        </div>
        <div className="summary-card">
          <h3>Avg Flowrate</h3>
          <p>{s.avg_flowrate}</p>
        </div>
        <div className="summary-card">
          <h3>Avg Pressure</h3>
          <p>{s.avg_pressure}</p>
        </div>
        <div className="summary-card">
          <h3>Avg Temperature</h3>
          <p>{s.avg_temperature}</p>
        </div>
      </div>
    </>
  );
}

export default Summary;