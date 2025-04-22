import { useEffect, useState } from "react";
import axios from "axios";
import Chart from "./Charts";
import { useNavigate } from 'react-router-dom'

export default function DevicesTable() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [newDevice, setNewDevice] = useState({
    title: "",
    mac_address: "",
    is_active: false,
    sensors: []
  });
  const [sensorTypes, setSensorTypes] = useState([]);
  const [sensorLoading, setSensorLoading] = useState(true);
  const [postResponse, setPostResponse] = useState(null); 
  const [showChart, setShowChart] = useState(false);
  const navigate = useNavigate()

  useEffect(() => {
    axios.get("http://192.168.39.9:8000/devices/get")
      .then(response => {
        setDevices(response.data);
        setLoading(false);
      })
      .catch(error => {
        setError(error.message);
        setLoading(false);
      });

    axios.get("http://192.168.39.9:8000/sensors/get_types")
      .then(response => {
        setSensorTypes(response.data);
        setSensorLoading(false);
      })
      .catch(error => {
        setError(error.message);
        setSensorLoading(false);
      });
  }, []);

  const handleDelete = (mac_address) => {
    axios
      .delete("http://192.168.39.9:8000/devices/delete", {
        data: { mac_address },
      })
      .then((response) => {
        console.log("Устройство удалено:", response.data);

        setDevices(devices.filter((device) => device.mac_address !== mac_address));
      })
      .catch((error) => {
        console.error("Ошибка при удалении устройства:", error);
        setError("Ошибка при удалении устройства: " + error.message);
      });
  };

  const handleOpen = (mac_address) => {
    navigate('/graph',{
      state: { mac_address: mac_address }
    })
  };

  const handleEdit = (mac_address) => {
    console.log("Редактирование устройства с MAC-адресом: " + mac_address);
  };

  const handleAddDevice = () => {
    const formattedDevice = {
      title: newDevice.title,
      mac_address: newDevice.mac_address,
      ip_address: newDevice.ip_address,
      sensors: newDevice.sensors.map(sensor => ({
        name: sensor.name,
        sensor_type: sensor.type,
        error_value: parseFloat(sensor.error) || 0,
        measurement_unit: sensor.unit,
        pin: sensor.pin
      }))
    };

    axios.post("http://192.168.39.9:8000/devices/add", formattedDevice)
      .then(response => {
        setPostResponse(response.data.detail);
        setDevices([...devices, response.data]);
        setShowForm(false);
      })
      .catch(error => {
        console.error("Ошибка при добавлении устройства:", error);
        setError("Ошибка при добавлении устройства: " + error.message);
      });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewDevice({
      ...newDevice,
      [name]: name === "is_active" ? value === "true" : value
    });
  };

  const handleAddSensor = () => {
    setNewDevice({
      ...newDevice,
      sensors: [...newDevice.sensors, { name: "", type: "", pin: "", error: "", unit: "" }]
    });
  };

  const handleRemoveSensor = (index) => {
    const updatedSensors = newDevice.sensors.filter((_, i) => i !== index);
    setNewDevice({
      ...newDevice,
      sensors: updatedSensors
    });
  };

  const handleSensorChange = (index, e) => {
    const { name, value } = e.target;
    const updatedSensors = newDevice.sensors.map((sensor, i) =>
      i === index ? { ...sensor, [name]: value } : sensor
    );
    setNewDevice({
      ...newDevice,
      sensors: updatedSensors
    });
  };

  if (loading || sensorLoading) return <p>Загрузка...</p>;
  if (error) return <p>Ошибка: {error}</p>;

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Список устройств</h2>
      
      {/* Кнопка для отображения формы */}
      <button
        onClick={() => setShowForm(!showForm)}
        className="mb-4 px-6 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 transition duration-200"
      >
        Добавить устройство
      </button>

      {/* Форма добавления устройства */}
      {showForm && (
        <div className="bg-white p-4 shadow-md rounded-md mb-6">
          <h3 className="text-lg font-semibold mb-4">Добавить новое устройство</h3>
          <form>
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Название устройства</label>
              <input
                type="text"
                name="title"
                value={newDevice.title}
                onChange={handleChange}
                className="w-full p-2 border border-gray-300 rounded-md"
                required
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">MAC-адрес</label>
              <input
                type="text"
                name="mac_address"
                value={newDevice.mac_address}
                onChange={handleChange}
                className="w-full p-2 border border-gray-300 rounded-md"
                required
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">IP-Address</label>
              <input
                type="text"
                name="ip_address"
                value={newDevice.ip_address}
                onChange={handleChange}
                className="w-full p-2 border border-gray-300 rounded-md"
                required
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Активность</label>
              <select
                name="is_active"
                value={newDevice.is_active}
                onChange={handleChange}
                className="w-full p-2 border border-gray-300 rounded-md"
              >
                <option value="true">Активно</option>
                <option value="false">Неактивно</option>
              </select>
            </div>

            {/* Формы для датчиков */}
            <div className="mb-4">
              <h4 className="text-md font-semibold">Датчики</h4>
              {newDevice.sensors.map((sensor, index) => (
                <div key={index} className="flex space-x-4 mb-2">
                  <div className="flex-1">
                    <label className="block text-sm font-medium mb-2">Имя датчика</label>
                    <input
                      type="text"
                      name="name"
                      value={sensor.name}
                      onChange={(e) => handleSensorChange(index, e)}
                      className="w-full p-2 border border-gray-300 rounded-md"
                      required
                    />
                  </div>
                  <div className="flex-1">
                    <label className="block text-sm font-medium mb-2">Тип датчика</label>
                    <select
                      name="type"
                      value={sensor.type}
                      onChange={(e) => handleSensorChange(index, e)}
                      className="w-full p-2 border border-gray-300 rounded-md"
                      required
                    >
                      <option value="">Выберите тип датчика</option>
                      {sensorTypes.map((type) => (
                        <option key={type.id} value={type.id}>{type.sensor_name}</option>
                      ))}
                    </select>
                  </div>
                  <div className="flex-1">
                    <label className="block text-sm font-medium mb-2">Используемый пин</label>
                    <input
                      type="number"
                      name="pin"
                      value={sensor.pin}
                      onChange={(e) => handleSensorChange(index, e)}
                      className="w-full p-2 border border-gray-300 rounded-md"
                      placeholder="Введите номер пина"
                    />
                  </div>
                  <div className="flex-1">
                    <label className="block text-sm font-medium mb-2">Погрешность</label>
                    <input
                      type="number"
                      name="error"
                      value={sensor.error}
                      onChange={(e) => handleSensorChange(index, e)}
                      className="w-full p-2 border border-gray-300 rounded-md"
                      placeholder="Введите погрешность"
                    />
                  </div>
                  <div className="flex-1">
                    <label className="block text-sm font-medium mb-2">Единица измерений</label>
                    <input
                      type="text"
                      name="unit"
                      value={sensor.unit}
                      onChange={(e) => handleSensorChange(index, e)}
                      className="w-full p-2 border border-gray-300 rounded-md"
                      placeholder="Введите единицу измерений"
                    />
                  </div>
                  <button
                    type="button"
                    onClick={() => handleRemoveSensor(index)}
                    className="text-red-500 hover:text-red-700 mt-6"
                  >
                    Удалить датчик
                  </button>
                </div>
              ))}
              <button
                type="button"
                onClick={handleAddSensor}
                className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition duration-200"
              >
                Добавить датчик
              </button>
            </div>

            <button
              type="button"
              onClick={handleAddDevice}
              className="px-6 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition duration-200"
            >
              Добавить
            </button>
          </form>
        </div>
      )}

      {/* Ответ от сервера после добавления устройства */}
      {postResponse && (
        <div className="bg-green-100 p-4 mt-4 rounded-md">
          <h3 className="font-semibold">Устройство успешно добавлено:</h3>
          <pre className="text-sm">{JSON.stringify(postResponse, null, 2)}</pre>
        </div>
      )}

      {/* Таблица с устройствами */}
      <table className="min-w-full border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-100">
            <th className="border border-gray-300 px-4 py-2">Название</th>
            <th className="border border-gray-300 px-4 py-2">MAC-адрес</th>
            <th className="border border-gray-300 px-4 py-2">Активность</th>
            <th className="border border-gray-300 px-4 py-2">Действия</th>
          </tr>
        </thead>
        <tbody>
          {devices.map((device) => (
            <tr key={device.mac_address} className="hover:bg-gray-50">
              <td className="border border-gray-300 px-4 py-2">{device.title}</td>
              <td className="border border-gray-300 px-4 py-2">{device.mac_address}</td>
              <td className="border border-gray-300 px-4 py-2">{device.is_active ? "Активно" : "Неактивно"}</td>
              <td className="border border-gray-300 px-4 py-2 flex space-x-2">
                <button
                  onClick={() => handleEdit(device.mac_address)}
                  className="px-4 py-2 bg-yellow-500 text-white rounded-md hover:bg-yellow-600 transition duration-200"
                >
                  Редактировать
                </button>
                <button
                  onClick={() => handleDelete(device.mac_address)}
                  className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 transition duration-200"
                >
                  Удалить
                </button>
                <button
                  onClick={() => handleOpen(device.mac_address)}
                  className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition duration-200"
                >
                  Просмотр
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
  };

