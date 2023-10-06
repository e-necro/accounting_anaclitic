<template>
  <div class="auto-catalog">
    <h1>Каталог машин</h1>
    <div v-if="autoList === null" class="auto-catalog_no-data">
      <img class="auto-catalog_list-no-data-loader" src="@/assets/img/giphy.gif">
    </div>

    <div v-else-if="autoList.length !== 0" class="auto-catalog_list" >
      {{ autoList }}
    </div>

    <div v-else class="auto-catalog_list-no-data-add">
      <h3 v-if="!showAddForm">Машин не нашлось. <a href="" @click.prevent="showForm(true)">Добавить?</a></h3>
      <mcv-add-auto 
        v-if="showAddForm" 
        :current-user="currentUser"
        ></mcv-add-auto>
    </div>  
  </div>
</template>

<script>
// import McvRepairCatalog from '@/components/RepairCatalog'
import McvAddAuto from '@/components/AddAuto'
import axios from 'axios'
import { getterTypes } from '@/store/modules/auth';

export default {
  name: "McvAutoCatalog",
  data() {
    return {
      currentAuto: null,
      autoList: null,
      showAddForm: false
    }
  },
  components: {
    McvAddAuto
    // McvRepairCatalog,
  },
  computed: {
    currentUser() {
      let currentUser1 = this.$store.getters[getterTypes.currentUser]
      this.getMessage(currentUser1)
      return currentUser1
    },
  },
  methods: { 
    // TODO: вызоов этого метода сбоит на маке. Или это не только на маке?
    getMessage(user) {
      if (user !== null) {
        // axios({
        //   method: 'post',
        //   url: '/get_my_auto',
        //   data: {
        //     user_id: user._id,
        //     token: user.token
        //   }
        // })
        axios.post('/get_my_auto',{user_id: user._id, token: user.token})
        .then((res) => {
          this.autoList = res.data
        })
        .catch((error) => {
          console.error(error)
        })
      }
    },
    showForm(toShow) {
      this.showAddForm = toShow
    }
  },
  mounted() {
    // this.getMessage()
  }
}

</script>