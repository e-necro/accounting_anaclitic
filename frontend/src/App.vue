<template>
  <mcv-topbar/>
    <router-view/>
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

import McvTopbar from '@/components/Topbar'
import { actionTypes } from './store/modules/auth';

export default {
  name: 'McvApp',
  components: {
    McvTopbar,
  },
  mounted() {
    this.$store.dispatch(actionTypes.getCurrentUser)
  }
  
}
</script>