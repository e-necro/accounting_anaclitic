import axios from '@/api/axios'


const register = credentials => {
  return axios.post('/register', {user: credentials})
}

export default {
  register
}