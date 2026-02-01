function DataTable({ rows }) {
  if (!rows || rows.length === 0) return null;

  // Get column names dynamically from first row
  const columns = Object.keys(rows[0]);

  return (
    <div style={{ marginTop: "30px" }}>
      <h2>Equipment Data Preview</h2>

      <table border="1" cellPadding="8" style={{ borderCollapse: "collapse", width: "100%" }}>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col}>{col}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {rows.map((row, idx) => (
            <tr key={idx}>
              {columns.map((col) => (
                <td key={col}>{row[col]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DataTable;