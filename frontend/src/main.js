import 'bootstrap/dist/css/bootstrap.css';


import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router'
import store from '@/store'
import mainStyles from '@/assets/css/main.css'



createApp(App)
  .use(store)
  .use(router)
  .use(mainStyles)
  .mount('#app')
