<template>
  <div class="auto-catalog">
    <h1>Каталог машин</h1>
    <div v-if="autoList === null" class="auto-catalog_no-data">
      <img class="auto-catalog_list-no-data-loader" src="@/assets/img/giphy.gif">
    </div>

    <div v-else-if="autoList.length !== 0" class="auto-catalog_list" >
      <div class="item item-title">
        <div class="item__number">№</div>
        <div class="item__name">Название</div>
        <div class="item__comment">Описание машины</div>
        <div class="item__date"> Дата покупки</div>
        <div class="item__control"></div>
      </div>
      <div class="item" v-for="(auto, index) in autoList" :key="auto._id">
        <div class="item__number"> {{ index }} </div>
        <div class="item__name">{{ auto.name }}</div>
        <div class="item__comment">{{ auto.comment }}</div>
        <div class="item__date">{{ auto.date }}</div>
        <div class="item__control"> <catalog-control :id="key"></catalog-control></div>
      </div>
      <h3 v-if="!showAddForm"><a href="" @click.prevent="showForm(true)">Добавить еще машину?</a></h3>
      <mcv-add-auto 
        v-if="showAddForm" 
        :current-user="currentUser"
        @close-form="reloadPage"
        ></mcv-add-auto>
    </div>

    <div v-else class="auto-catalog_list-no-data-add">
      <h3 v-if="!showAddForm">Машин не нашлось. <a href="" @click.prevent="showForm(true)">Добавить?</a></h3>
      <mcv-add-auto 
        v-if="showAddForm" 
        :current-user="currentUser"
        @close-form="reloadPage"
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
      showAddForm: false,
    }
  },
  components: {
    McvAddAuto
    // McvRepairCatalog,
  },
  computed: {
    currentUser() {
      return this.$store.getters[getterTypes.currentUser]
    },
  },
  methods: { 
    getMessage(user) {
      if (user !== null) {
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
    },
    reloadPage: function(param) {
      if (param == 'added') {
        this.autoList = null;
        this.showAddForm = false; 
        this.getMessage(this.currentUser);
      } else {
        this.showAddForm = false; 
      }
    }
  },
  mounted() {
    this.ii = 0;
    let $this = this;
    (function myLoop(i) {
      setTimeout(function() {
        let user =  $this.$store.getters[getterTypes.currentUser];
        if (user !== null) {
          $this.getMessage(user)   
          return 1
        }
        if (--i) myLoop(i);
      }, 1000)
    })(20);
    
  }
}

</script>