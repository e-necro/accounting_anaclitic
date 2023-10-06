<template>
  <div class="add-auto">
    <h2>Добавление автомобиля</h2>
    <div v-if="sResult !== null" class="add-auto__result"> {{ sResult }}</div>
    <div v-else class="add-auto__cont">
      <label for="auto-name">
        Название: 
        <input type="text" id="auto-name" name="auto-name" :value="name" required>
      </label>
      <label for="auto-comment">
        Краткое описание: 
        <input type="text" id="auto-comment" name="auto-comment" :value="comment" required>
      </label>
      <label for="auto-date">
        Дата покупки:
        <input type="text" id="auto-date" name="auto-date" :value="date" required>
      </label>
      <button @click="closeForm">Отмена</button>
      <button @click="saveAuto">Сохранить</button>
    </div>
  </div>
</template>

<script>

import axios from 'axios'
// TODO: прицепить календарь!! 
export default {
  name: "McvAddAuto",
  props: {
    currentUser: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      name: null,
      comment: null,
      date: null,
      sResult: null
    }
  },
  methods: {
    saveAuto() {
      if (this.name.trim() !== '' && this.comment.trim() !== '' && this.date ) {
        let oData = {}
        oData['user_id'] = this.currentUser._id
        oData['token'] = this.currentUser.token
        oData['name'] = this.name.trim()
        oData['comment'] = this.comment.trim()
        oData['date'] = this.date

        axios.post('/add_my_auto', oData)
          .then((res) => {
            if (res.data._id) {
              this.sResult = 'Успешно добавлено!'
              window.location.reload()
            } else {
              this.sResult = "Ошибка добавления. Попробуйте еще раз"
            }
            
          })
          .catch((error) => {
            console.error(error)
          })
      }
    },
    closeForm(){
      // поменять данные родительского компонента?
    }
  }
}

</script>