<template>
  <div class="lk-page">
    <div class="container page">
      <div class="row">
        <h1>Профиль</h1>
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
  name: 'McvUserProfile',
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
    // isSubmitting() {
    //   return this.$store.state.auth.isSubmitting
    // },
    // validationErrors() {
    //   return this.$store.state.auth.validationErrors
    // }
  },
  methods: {
  }
})
</script>
