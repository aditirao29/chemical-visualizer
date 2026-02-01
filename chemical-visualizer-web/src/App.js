import React, { useState } from "react";
import UploadCSV from "./components/UploadCSV";
import Summary from "./components/Summary";
import DataTable from "./components/DataTable";
import Charts from "./components/Charts";
import "./App.css";
import { useEffect } from "react";
import History from "./components/History";
import { fetchHistory, fetchDatasetById, downloadReport } from "./services/api";

function App() {
  const [response, setResponse] = useState(null);
  const [history, setHistory] = useState([]);
  useEffect(() => {
    fetchHistory().then(res => setHistory(res.data));
  }, []);
  const loadDataset = (id) => {
    fetchDatasetById(id).then(res => setResponse(res.data));
  };

  return (
    <div className="container">
      <h1>Chemical Equipment Visualizer</h1>

      <UploadCSV setResponse={setResponse} />

      {/* HISTORY SECTION */}
      {history.length > 0 && (
        <div className="section" style={{ background: "#fafafa" }}>
          <History datasets={history} onSelect={loadDataset} />
        </div>
      )}

      {response && (
        <>
          <div className="section">
            <Summary data={response} />
            <button className="pdf-btn"
              onClick={async () => {
                const res = await downloadReport(response.id);

                const url = window.URL.createObjectURL(
                  new Blob([res.data], { type: "application/pdf" })
                );

                const link = document.createElement("a");
                link.href = url;
                link.setAttribute("download", "report.pdf");
                document.body.appendChild(link);
                link.click();
                link.remove();
              }}
            >
            Download PDF Report
          </button>

        </div>

          <div className="section">
            <Charts distribution={response.summary.type_distribution} />
          </div>

          <div className="section">
            <DataTable rows={response.preview} />
          </div>
        </>
      )}
    </div>
  );
}

export default App;