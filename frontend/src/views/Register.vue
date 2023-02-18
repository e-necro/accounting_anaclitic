<template>
  <div class="auth-page">
    <div class="container page">
      <div class="row">

        <div class="col-md-6 offset-md-3 col-xs-12">
          <h1 class="text-xs-center " >Sign up</h1>
          <p class="text-xs-center">
            <!-- <router-link :to="{name: 'login'}">Have an account?</router-link> -->
          </p>

          <mcv-validation-errors 
            v-if="validationErrors" 
            :validation-errors = "validationErrors" 
          />

          <form @submit.prevent="onSubmit" >
            <fieldset >

              <fieldset class="form-group" >
                <input 
                  class="form-control form-control-lg " 
                  type="text" 
                  placeholder="Username"
                  v-model="username" 
                  required="required"
                >
              </fieldset>

              <fieldset class="form-group">
                <input 
                  class="form-control form-control-lg " 
                  type="email" 
                  placeholder="Email" 
                  v-model="email" 
                  required="required"
                >
              </fieldset>

              <fieldset class="form-group">
                <input 
                  class="form-control form-control-lg " 
                  type="password" 
                  placeholder="Password"
                  v-model="password"   
                  required="required"
                >
              </fieldset>

              <fieldset class="form-group">
                <input 
                  class="form-control form-control-lg " 
                  type="password" 
                  placeholder="Password again"
                  v-model="passwordCheck"   
                  required="required"
                >
              </fieldset>

              <button 
                class="btn btn-lg btn-primary pull-xs-right" 
                type="submit"
                :disabled="isSubmitting"
              >
                Sign up
              </button>
            </fieldset>
          </form>
        </div>
        
      </div>
    </div>
  </div>
</template>

<script>

import McvValidationErrors from '@/components/ValidationErrors'
import { actionTypes } from '@/store/modules/auth'
import md5 from "blueimp-md5"

export default ({
  name: 'McvRegister',
  data() {
    return {
      email: '',
      password: '',
      passwordCheck: '',
      username: ''
    }
  },
  components: {
    McvValidationErrors,
  },
  computed: {
    // не стал mapState импортить как в логине
    isSubmitting() {
      return this.$store.state.auth.isSubmitting
    },
    validationErrors() {
      return this.$store.state.auth.validationErrors
    }
  },
  methods: {
    onSubmit() {
      // this.$store.commit('registerStart')
      ///actionTypes.register
      // в md5 пароль загнать
      let pass = md5(this.password + '140' + this.email + '+++')
      if (this.password !== this.passwordCheck) {
        this.$store.commit('registerFailure', {passwords: " not match"})
      } else {
          this.$store.dispatch(actionTypes.register, 
          {
            email: this.email, 
            username: this.username, 
            password: pass
          }).then(user => {
            console.log('succesfully register user ', user)
            this.$router.push({name: 'home'})
          })
        }
      }
  }
})
</script>
