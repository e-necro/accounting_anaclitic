<template>
  <div class="lk-page">
    <div class="container page">
      <div class="row">
        <h1>Remonts</h1>
          <mcv-validation-errors 
            v-if="validationErrors" 
            :validation-errors = "validationErrors" 
          />


        </div>
      </div>
    </div>
</template>

<script>
import {mapState} from 'vuex'

import McvValidationErrors from '@/components/ValidationErrors'
import { actionTypes, getterTypes } from '@/store/modules/auth'
import axios from 'axios'

export default ({
  name: 'McvRemonts',
  data() {
    return {
      autoList: null
    }
  },
  components: {
    McvValidationErrors,
  },
  computed: {
    ...mapState({
      validationErrors: state => state.auth.validationErrors
    })
  },
  mounted() {
    // собрать на основе компонента Article с курса получение данных авто по айдшнику и юзеру.
    // Это будет вывод инфы по самой тачке.
    // Дальше дергаем данные по ремонтам к этой тачке... 
    let $this = this;
    (function myLoop(i) {
      setTimeout(function() {
        let user =  $this.$store.getters[getterTypes.currentUser];
        if (user !== null) {
          $this.getAuto(user, $this.$route.params.slug)   
          return 1
        }
        if (--i) myLoop(i);
      }, 1000)
    })(20);
  },
  methods: {
    getAuto(user, slug) {
      if (user !== null) {
        axios.post('/get_my_auto',{user_id: user._id, token: user.token, auto_id: slug})
        .then((res) => {
          console.log(res)
          this.autoList = res.data /// TODO: херится autoList почему-то. Не всегда доступен. Или это в плагине проблема отображения?
        })
        .catch((error) => {
          console.error(error)
        })
      }
    }
  }
})
</script>
