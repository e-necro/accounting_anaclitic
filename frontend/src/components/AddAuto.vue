<template>
  <div class="add-auto dialog" :class="showed">
    <label class="dlg-back" for="dialog_state"></label>
      <div class="dlg-wrap">
        <div class="closing_cross" @click="closeForm"></div>
        <div class="row modal-content">
          <div class="modal-body">
            <h2 class="modal-caption">{{ title }}</h2>
            <div v-if="sResult !== null" class="add-auto__result"> {{ sResult }}</div>
            <form v-else class="add-auto__cont">
              <label for="add-auto-name">
                Название: 
                <input type="text" id="auto-name" name="auto-name" v-model="name" required title="Название машины не может быть пустым">
              </label>
              <label for="add-auto-comment">
                Краткое описание: 
                <input type="text" id="auto-comment" name="auto-comment" v-model="comment" required title="Добавьте описание">
              </label>
              <label for="add-auto-date">
                Дата покупки:
                <input type="text" id="auto-date" name="auto-date" v-model="date" required title="Дата тоже нужна">
              </label>
              <div class="button-container">
                <button @click="closeForm">Отмена</button>
                <button @click="saveAuto" :disabled="disabled">Сохранить</button>
              </div>
            </form>
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
    },
    // toShow: {
    //   type: Boolean,
    //   required: true
    // }
  },
  data() {
    return {
      disabled: false,
      name: null,
      comment: null,
      date: null,
      sResult: null,
      showed: '',
      resolver: null,
      auto_id: null,
      title: 'Добавление автомобиля'
    }
  },
  // watch: {
  //   toShow: function(newVal, ) {
  //     if (newVal === true) {
  //       this.showed = 'dialog_open';
  //     } else {
  //       this.showed = '';
  //     }
  //   }
  // },
  methods: {
    saveAuto(e) {
      e.preventDefault();
      if (this.name.trim() !== '' && this.comment.trim() !== '' && this.date ) {
        this.disabled = true;
        let oData = {}
        oData['user_id'] = this.currentUser._id
        oData['token'] = this.currentUser.token
        oData['name'] = this.name.trim()
        oData['comment'] = this.comment.trim()
        oData['date'] = this.date

        if (this.auto_id === null) {
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
        } else {
          oData['auto_id'] = this.auto_id;
          axios.post('/upd_my_auto', oData)
            .then((res) => {
              if (res.data.updated == true) {
                this.sResult = 'Данные обновлены!'
                this.$emit('close-form', 'updated');                
              } else {
                this.sResult = "Ошибка изменения. Попробуйте еще раз"
              }
              
            })
            .catch((error) => {
              console.error(error)
            })
          this.auto_id = null;
          this.resolver = null;
        }
        setTimeout(() => {
          this.closeForm();
        }, 3000);
        this.disabled = false;
      }
    },
    closeForm(){
      // поменять данные родительского компонента?
      if (this.resolver !== null) {
        this.resolver('cancel');
      }
      this.$emit('close-form', 'closed');
      this.showed = '';
    },
    openForEdit(params, resolve) {
      this.showed = 'dialog_open';
      this.name = params['name'];
      this.comment = params['comment'];
      this.date = params['date'];
      this.auto_id = params['_id'];
      this.title = '';
      this.resolver = resolve;
      this.sResult = null;
    },
    openForAdd() {
      this.showed = 'dialog_open';
      this.name = null;
      this.comment = null;
      this.date = null;
      this.auto_id = null;
      this.title = 'Добавление автомобиля';
      this.resolver=null
      this.sResult = null;
    }
  },
  mounted() {
    // this.openForEdit()
    this.title = 'Добавление автомобиля'
  }, 
}

</script>