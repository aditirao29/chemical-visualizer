import React, { useState } from "react";
import { uploadCSV } from "../services/api";

function UploadCSV({ setResponse }) {
  const [file, setFile] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Select a CSV file");

    const formData = new FormData();
    formData.append("file", file);

    const res = await uploadCSV(formData);
    setResponse(res.data);
  };

  return (
    <div className="upload-box">
      <form onSubmit={handleSubmit}>
        <label className="file-label">Choose CSV File
          <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} hidden/>
        </label>
        <span className="file-name">
          {file ? file.name : "No file selected"}
        </span>
        <button type="submit" className="upload-btn">Upload</button>
      </form>
    </div>
  );
}

export default UploadCSV;