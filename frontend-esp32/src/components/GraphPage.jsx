import { useLocation } from 'react-router-dom'
import Chart from './Charts'
import { useEffect, useState } from "react";
import axios from "axios";
import Header from "./Header"
function Graph() {
    const location = useLocation()
    const {mac_address} = location.state || {}
    const [sensor_data, sensorData] = useState([]);
    const [device_title, deviceTitle] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);



    useEffect(() => {

      const fetchData = async () => {
          try {
              const formattedMac = {
                  mac_address: mac_address,
                };
            
              axios.post("http://192.168.39.9:8000/data_records/get_data", formattedMac)
                .then(response => {
                  sensorData(response.data.data);
                  deviceTitle(response.data.device_title);
                  setLoading(false);
                
                })
                .catch(error => {
                  setError(error.message);
                  setLoading(false);
                });
          } catch (error) {
            console.error('Ошибка при получении данных', error)
          }
        }
        fetchData()
      const interval = setInterval(fetchData, 3000) 

      return () => clearInterval(interval)


    }, []);

    const formattedData = sensor_data.map(sensor =>({
      sensor_type: sensor.sensor_type,
      output_data: sensor.output_data.map(item => ({
        date: new Date(item.created_date).toLocaleTimeString(), 
        value: item.value
      })).slice().reverse()
    }))


    return (
      <div>
        <Header />
        <h1 className="text-xl font-bold text-center mb-3">Устройство: {device_title}</h1>

        <h2 className="text-l font-bold text-center mb-3">{mac_address}</h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
      {formattedData.map((sensor) => (
        <Chart sensor_data={sensor.output_data} sensor_type={sensor.sensor_type} />
      ))}
      </div>
      </div>
    )
  }
  
  export default Graph