function History({ datasets, onSelect }) {
  return (
    <div>
      <h2>Previous Uploads (Last 5)</h2>
      <p style={{ fontSize: "14px", color: "#666" }}>
        Click a dataset to reload its analysis
      </p>

      <div className="history-list">
        {datasets.map(ds => (
            <div
            key={ds.id}
            className="history-card"
            onClick={() => onSelect(ds.id)}
            >
            <div className="history-id">Dataset #{ds.id}</div>
            <div className="history-meta">
                {ds.summary.total_count} items
            </div>
            </div>
        ))}
        </div>
    </div>
  );
}

export default History;