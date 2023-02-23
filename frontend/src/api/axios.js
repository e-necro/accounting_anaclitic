import axios from 'axios';
import {getItem} from '@/helpers/persistanceStorage'

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5000/';  // the FastAPI backend

axios.interceptors.request.use(config => {
    const token = getItem('accessToken')
    const authorizationToken = token ? `Token ${token}`: ''
    config.headers.Authorization = authorizationToken
    return config
})

export default axios