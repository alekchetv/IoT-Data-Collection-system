import axios from "axios";

const axiosInstance = axios.create({
  baseURL: `${import.meta.env.VITE_API_PROTOCOL}://${import.meta.env.VITE_IP_HOST}:${import.meta.env.VITE_API_PORT}`, // автоматическая подстановка из .env
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true, // если нужно (например, для cookie)
});
console.log(import.meta.env.VITE_IP_HOST)
export default axiosInstance;
