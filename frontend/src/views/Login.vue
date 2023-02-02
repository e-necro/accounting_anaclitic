<template>
  <div class="auth-page">
    <div class="container page">
      <div class="row">

        <div class="col-md-6 offset-md-3 col-xs-12">
          <h1 class="text-xs-center " >Sign in</h1>
          <p class="text-xs-center">
            <router-link :to="{name: 'register'}">Need an account?</router-link>
          </p>

          <mcv-validation-errors 
            v-if="validationErrors" 
            :validation-errors = "validationErrors" 
          />

          <form @submit.prevent="onSubmit" >
            <fieldset ng-disabled="$ctrl.isSubmitting">


              <fieldset class="form-group">
                <input class="form-control form-control-lg " type="email" placeholder="Email" 
                  v-model="email" 
                >
              </fieldset>

              <fieldset class="form-group">
                <input class="form-control form-control-lg " type="password" placeholder="Password"
                  v-model="password"   
                >
              </fieldset>

              <button 
                class="btn btn-lg btn-primary pull-xs-right" 
                type="submit"
                :disabled="isSubmitting"
              >
              Sign in
              </button>
            </fieldset>
          </form>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import {mapState} from 'vuex'

import McvValidationErrors from '@/components/ValidationErrors'
import { actionTypes } from '@/store/modules/auth'
import md5 from "blueimp-md5"

export default ({
  name: 'McvLogin',
  data() {
    return {
      email: '',
      password: '',
    }
  },
  components: {
    McvValidationErrors,
  },
  computed: {
    ...mapState({
      isSubmitting: state => state.auth.isSubmitting,
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
    onSubmit() {
      // this.$store.commit('registerStart')
      let pass = md5(this.password + '140' + this.email + '+++')
      this.$store.dispatch(actionTypes.login, 
        {
          email: this.email, 
          password: pass
        }).then(() => {
          this.$router.push({name: 'home'}) /// TODO: редиект проверить
        })
    }
  }
})
</script>
