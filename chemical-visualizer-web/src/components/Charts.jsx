import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
);

function Charts({ distribution }) {
  if (!distribution) return null;

  const labels = Object.keys(distribution);
  const values = Object.values(distribution);

  const data = {
    labels,
    datasets: [
        {
        label: "Equipment Count",
        data: values,
        backgroundColor: "#f58742",
        borderColor: "#f58742",
        borderWidth: 1,
        },
    ],
};


  return (
    <div style={{ marginTop: "40px", width: "600px" }}>
      <h2>Equipment Type Distribution</h2>
      <Bar
        data={data}
        options={{
            plugins: {
            legend: { display: false },
            },
        }}
        />
    </div>
    
  );
}

export default Charts;