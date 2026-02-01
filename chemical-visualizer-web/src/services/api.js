import axios from "axios";

const API = axios.create({
  baseURL: process.env.REACT_APP_BASE_URL,
});

API.interceptors.request.use((config) => {
  const token = process.env.REACT_APP_API_TOKEN;
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export const uploadCSV = (formData) =>
  API.post("upload/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

export default API;

export const fetchHistory = () => API.get("history/");
export const fetchDatasetById = (id) => API.get(`history/${id}/`);
export const downloadReport = (id) =>
  API.get(`report/${id}/`, { responseType: "blob" });
