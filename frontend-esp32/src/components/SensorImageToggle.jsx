import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";
import sensorImages from "../sensorImages.json";

export default function SensorImageToggle({ sensor_type }) {
  const [isOpen, setIsOpen] = useState(false);
  const imageSrc = sensorImages[sensor_type] || sensorImages["default"];

  return (
    <div style={{position: "relative", zIndex: 10,}}className="p-4 border rounded-2xl shadow-md max-w-sm mx-auto bg-white">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 text-blue-600 hover:text-blue-800 transition"
      >
        {isOpen ? <ChevronDown /> : <ChevronRight />}
        <span className="font-medium">Показать датчик: {sensor_type}</span>
      </button>

      {isOpen && (
        <div className="mt-4 bg-white">
          <img
            src={imageSrc}
            alt={sensor_type}
            className="w-auto max-h-[300px] h-auto rounded-lg bg-white"
          />
        </div>
      )}
    </div>
  );
}
