<template>
  <mcv-topbar/>
    <router-view/>
    <mcv-message-form ref="showMessageForm" />
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

</style>

<script>

import McvTopbar from './components/Topbar'
import McvMessageForm from './views/MessageForm.vue';
import { actionTypes } from './store/modules/auth';

export default {
  name: 'McvApp',
  components: {
    McvTopbar,
    McvMessageForm
  },
  mounted() {
    this.$store.dispatch(actionTypes.getCurrentUser)
  }
  
}
</script>