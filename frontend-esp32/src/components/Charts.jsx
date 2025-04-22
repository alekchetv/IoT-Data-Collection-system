import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";


const Chart = ({ sensor_data, sensor_type }) => {
  return (
    <div style={{ width: "100%", height: 250 }}>
      <h3 className="text-lg font-semibold mb-1 text-center">
        {sensor_type}
      </h3>
      <ResponsiveContainer>
        <LineChart data={sensor_data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="value"
            stroke="#8884d8"
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default Chart;