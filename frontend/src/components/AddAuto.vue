<template>
  <div class="add-auto dialog" :class="showed">
    <label class="dlg-back" for="dialog_state"></label>
      <div class="dlg-wrap">
        <div class="closing_cross" @click="closeForm"></div>
        <div class="row modal-content">
          <div class="modal-body">
            <h2 class="modal-caption">Добавление автомобиля</h2>
            <div v-if="sResult !== null" class="add-auto__result"> {{ sResult }}</div>
            <div v-else class="add-auto__cont">
              <label for="add-auto-name">
                Название: 
                <input type="text" id="auto-name" name="auto-name" v-model="name" required>
              </label>
              <label for="add-auto-comment">
                Краткое описание: 
                <input type="text" id="auto-comment" name="auto-comment" v-model="comment" required>
              </label>
              <label for="add-auto-date">
                Дата покупки:
                <input type="text" id="auto-date" name="auto-date" v-model="date" required>
              </label>
              <div class="button-container">
                <button @click="closeForm">Отмена</button>
                <button @click="saveAuto">Сохранить</button>
              </div>
            </div>
          </div>
        </div>
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
      sResult: null,
      showed: ''
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
              this.$emit('close-form', 'added');
              // window.location.reload()
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
      this.$emit('close-form', 'closed');
      this.showed = '';
    }
  },
  mounted() {
    this.showed = 'dialog_open';
  }
}

</script>