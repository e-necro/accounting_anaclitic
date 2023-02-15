import 'bootstrap/dist/css/bootstrap.css';


import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router'
import store from '@/store'
import bootstrapStyles from '@/assets/css/bootstrap_imported.css' ///TODO: помимо этих стилей, надо свои прикрутить, выяснив как с ними вообще работается. На тот же SASS
import mainStyles from '@/assets/css/main.css'




createApp(App)
  .use(store)
  .use(router)
  .use(bootstrapStyles)
  .use(mainStyles)
  .mount('#app')
