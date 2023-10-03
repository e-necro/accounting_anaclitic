<template>
  <div class="auto-catalog">
      <h1>Каталог машин</h1>
      {{ currentUser }}
      {{ autoList }}
  </div>
</template>

<script>
import McvRepairCatalog from '@/components/RepairCatalog'
import axios from 'axios'
import { getterTypes } from '@/store/modules/auth';

export default {
  name: "McvAutoCatalog",
  data() {
    return {
      currentAuto: null,
      autoList: [],
      userData: null
    }
  },
  components: {
    McvRepairCatalog,
  },
  computed: {
    currentUser() {
      this.userData = this.$store.getters[getterTypes.currentUser]
      return this.userData
    },
  },
  methods: { 
    getMessage(user) {
      axios({
        method: 'get',
        url: '/',
        data: {
          user_id: user._id,
          token: user.token
        }
      })
        .then((res) => {
          this.autoList = res.data
        })
        .catch((error) => {
          console.error(error)
        })
    }
  },
  watch: {
    userData: function(oldData, newData) {
      // console.log(oldData)
      // console.log(newData)
      ///TODO: выяснить как в том курсе проверяется авторизация/
      this.getMessage(oldData)
    }
  },
  mounted() {
    // this.getMessage()
  }
}

</script>