import axios from '@/api/axios'


const register = credentials => {
  return axios.post('/register', {user: credentials})
}

const login = credentials => {
  return axios.post('/login', {user: credentials})
}

const getCurrentUser = () => {
  return axios.get('/user')
}

export default {
  register,
  login,
  getCurrentUser
}