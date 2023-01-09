import authApi from '@/api/auth'

const state = {
  isSubmitting: false,
  currentUser: null,
  validationErrors: null,
  isLoggedIn: null
}

const mutations = {
  registerStart(state) {
      state.isSubmitting = true
      state.validationErrors = null
  },
  registerSuccess(state, payload) {
    state.isSubmitting = false
    state.currentUser = payload
    state.isLoggedIn = true
  },
  registerFailure(state, payload) {
    state.isSubmitting = false
    state.validationErrors = payload
  }
}

const actions = {
  register(context, credentials) {
    return new Promise(resolve => {
      context.commit('registerStart')
      authApi.register(credentials)
        .then(response => {
          console.log('response ', response)
          context.commit('registerSuccess'.response.data.user) ///TODO: с этим возвратом разобраться, т.е. отдать в нужном виде!!!!
          resolve(response.data.user) /// возвращает этого юзера туда, где вызвано был метод (/views/Register.vue в данном случае)
        })
        .catch(result => {
          context.commit('registerFailure', result.response.data.errors) ///TODO: та же лаза с данными
          console.log('result errors', result)
        })
    })

  }
}

export default {
  state,
  mutations,
  actions
}