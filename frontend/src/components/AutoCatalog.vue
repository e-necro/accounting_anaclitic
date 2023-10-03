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
    }
  },
  components: {
    McvRepairCatalog,
  },
  computed: {
    currentUser() {
      let currentUser1 = this.$store.getters[getterTypes.currentUser]
      this.getMessage(currentUser1)
      return currentUser1
    },
  },
  methods: { 
    getMessage(user) {
      if (user !== null) {
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
    }
  },
  mounted() {
    // this.getMessage()
  }
}

</script>