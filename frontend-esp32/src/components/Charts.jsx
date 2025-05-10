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
import SensorImageToggle from "./SensorImageToggle";

const Chart = ({ sensor_data, sensor_type }) => {
  return (
    <div className="bg-white" style={{ width: "90%", height: 200, marginBottom: "100px" }}>
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
      <SensorImageToggle sensor_type={sensor_type}>

      </SensorImageToggle>
    </div>
  );
};

export default Chart;