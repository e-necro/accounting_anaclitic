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
// import { actionTypes } from '@/store/modules/auth'

export default ({
  name: 'McvRemonts',
  data() {
    return {
      
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
  },
  methods: {
  }
})
</script>
