import axios from 'axios'
import { API_HOST, API_PORT } from './config'

const instance = axios.create({
    baseURL: `${API_HOST}:${API_PORT}`
})

instance.interceptors.request.use((config) => {
    config.headers.Authorization = `Bearer ${localStorage.getItem('token')}`
    return config // Путь свободен, продолжаем выполнение запроса
})

export default instance
