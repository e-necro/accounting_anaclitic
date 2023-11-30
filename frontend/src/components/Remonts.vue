<template>
  <div class="lk-page">
    <div class="container page">
        <h1>Remonts</h1>
        <a class="rollback-link" @click="$router.go(-1)"> Назад</a>
          <mcv-validation-errors 
            v-if="validationErrors" 
            :validation-errors = "validationErrors" 
          />

          <div v-if="autoList === null" class="auto_descr">
            <img class="auto_descr-no-data-loader" src="@/assets/img/giphy.gif">
          </div>

          <div v-else-if="autoList.length !== 0" class="auto_descr" :class="{loaded : autoList.length !== 0 }">
            <h3 class="auto_descr--title">
              {{ autoList[0].name }}
            </h3>
            <div class="auto_descr--text">
              {{ autoList[0].comment }}
            </div>
            <div class="auto_desc--text_dt" v-if="autoList[0].date_create !== null">
              Куплена {{ autoList[0].date_create }} 
            </div>
            <hr>
          </div>

          <div v-if="remontList === null && autoList !== null" class="auto_descr">
            <img class="auto_descr-no-data-loader" src="@/assets/img/giphy.gif">
          </div>
          <div v-else-if="remontList !== null  &&  remontList.length !== 0 && autoList !== null" class="auto_remonts">
              <h3>Список ремонтов:</h3>
              <div class="item item-title">
                <div class="item__number">№</div>
                <div class="item__name">Название</div>
                <div class="item__comment">Описание</div>
                <div class="item__price">Цена</div>
                <div class="item__date">Дата начала ремонта</div>
                <div class="item__date">Дата окончания ремонта</div>
                <div class="item__elapced-time">Примерное время работ(часы)</div>
                <div class="item__control"></div>
              </div>
              <div v-for="(remont, index) in remontList" :key="remont._id" :data-id="remont._id" class="item">
                  <div class="item__number"> {{ index }} </div>
                  <div class="item__name">{{ remont.name }}</div>
                  <div class="item__comment">{{ remont.comment }}</div>
                  <div class="item__price">{{ remont.price }}</div>
                  <div class="item__date">{{ remont.start_date }}</div>
                  <div class="item__date">{{ remont.end_date }}</div>
                  <div class="item__elapced-time">{{ remont.elapced_time }}</div>
                  <div class="item__control"> 
                    <!-- <mcv-catalog-control 
                      :id="auto._id" 
                      :current-user="currentUser" 
                      :car-name="auto.name" 
                      @reload="reloadPage"
                      @edits="editItem" 
                    ></mcv-catalog-control> -->
                  </div>
              </div>
          </div>
          <div v-else-if='autoList !== null'>
            Нету ремонтиков. Добавить ссылку на форму
          </div>



      </div>
    </div>
</template>

<script>
import {mapState} from 'vuex'

import McvValidationErrors from '@/components/ValidationErrors'
import {  getterTypes } from '@/store/modules/auth' //actionTypes
import axios from 'axios'

export default ({
  name: 'McvRemonts',
  data() {
    return {
      autoList: null,
      remontList: null,
    }
  },
  components: {
    McvValidationErrors,
  },
  computed: {
    ...mapState({
      validationErrors: state => state.auth.validationErrors
    })
  },
  mounted() {
    // собрать на основе компонента Article с курса получение данных авто по айдшнику и юзеру.
    // Это будет вывод инфы по самой тачке.
    // Дальше дергаем данные по ремонтам к этой тачке... 
    let $this = this;
    (function myLoop(i) {
      setTimeout(function() {
        let user =  $this.$store.getters[getterTypes.currentUser];
        if (user !== null) {
          $this.getAuto(user, $this.$route.params.slug)   
          return 1
        }
        if (--i) myLoop(i);
      }, 1000)
    })(20);
  },
  methods: {
    getAuto(user, slug) {
      if (user !== null) {
        axios.post('/get_my_auto',{user_id: user._id, token: user.token, auto_id: slug})
        .then((res) => {
          this.autoList = res.data 
          if (this.autoList !== null) {
            this.getAutoRemonts(user, slug)
          }
        })
        .catch((error) => {
          console.error(error)
        })
      }
    },
    getAutoRemonts(user, slug) {
      axios.post('/get_my_remonts',{user_id: user._id, token: user.token, auto_id: slug})
        .then((res) => {
          this.remontList = res.data 
          console.log(this.remontList)
        })
        .catch((error) => {
          console.error(error)
        })
    }
  }
})
</script>