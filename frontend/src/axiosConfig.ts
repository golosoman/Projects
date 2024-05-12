import axios from 'axios'
import { API_HOST, API_PORT } from './config'

const instance = axios.create({
    baseURL: `${API_HOST}:${API_PORT}`
})

export default instance
