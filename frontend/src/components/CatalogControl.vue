<template>
    <div v-if="autoUpd === true" class="control_no-data">
      <img class="control-no-data-loader" src="@/assets/img/giphy.gif">
    </div>
    <div v-else class="control" >
      <a class="control-edit" @click.prevent="editAuto"></a>
      <a class="control-delete" @click.prevent="deleteAuto"></a>
    </div>
  </template>
  
  <script>
//   TODO: иконки добавить. Прописать методы
  import axios from 'axios'
  export default {
    name: "McvControlAutor",
    props: {
      currentUser: {
        type: Object,
        required: true
      },
      id: {
        type: String,
        required: true
      },
      carName: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        sResult: null,
        autoUpd: null
      }
    },
    methods: {
     deleteAuto(e) {
      e.preventDefault();
      let res = confirm('Действительно хотите удалить машину ~ ' + this.carName + '~ ? \r\n (не получится если к ней уже привязаны ремонты)');
      if (res) {
        this.autoUpd = true;
        let oData = {}
        oData['user_id'] = this.currentUser._id
        oData['token'] = this.currentUser.token
        oData['id'] = this.id

        axios.post('/delete_my_auto', oData)
          .then((res) => {
            if (res.data.deleted == true) {
              this.sResult = 'Удалено'
            } else if (res.data.deleted == 'have_data') {
              this.sResult = "К машине привязаны ремонты. Сначала нужно их удалить";
            } else if (res.data.deleted == 'no_data') {
              this.sResult = 'У текущего пользователя нет авто с таким id';
            } else {
              this.sResult = 'Произошла ошибка. Попробуйте еще раз';
            }
            
            if (this.sResult == 'Удалено') {
              this.$root.$refs.showMessageForm.openForm('success', this.sResult);
              this.$emit('reload', 'added');
            } else {
              this.$root.$refs.showMessageForm.openForm('error', this.sResult);
            }
            this.autoUpd = null;
          })
          .catch((error) => {
            this.autoUpd = null;
            console.error(error)
          })
      }
     },
     editAuto() {
        this.autoUpd = true;
        let oData = {}
        oData['ID'] = this.id;
        let result = new Promise((resolve,) => this.$emit('edits', oData, resolve) );
        result.then((value) => {
          if (value == true) {
            this.$root.$refs.showMessageForm.openForm('success', 'Данные обновлены');
            this.$emit('reload', 'added');
          } else if (value == false) {
            this.$root.$refs.showMessageForm.openForm('error', "Что-то пошло не так, попробуйте еще раз");
            this.$emit('reload', 'added');
          }
          this.autoUpd = null;    
        })
     }

    },
    mounted() {
    }
  }
  
  </script>