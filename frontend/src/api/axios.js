import axios from 'axios';

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5000/';  // the FastAPI backend

export default axios