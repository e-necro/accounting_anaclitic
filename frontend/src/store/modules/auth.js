import authApi from '@/api/auth'

const state = {
  isSubmitting: false,

}

const mutations = {
  registerStart(state) {
      state.isSubmitting = true
  },
  registerSuccess(state) {
    state.isSubmitting = false
  },
  registerFailure(state) {
    state.isSubmitting = false
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
          resolve(response.data.user)
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