<template>
  <div v-if="remontUpd === true" class="control_no-data">
    <img class="control-no-data-loader" src="@/assets/img/giphy.gif">
  </div>
  <div v-else class="control" >
    <a class="control-edit" @click.prevent="editRemont"></a>
    <a class="control-delete" @click.prevent="deleteRemont"></a>
  </div>
</template>

<script>
//   TODO: иконки добавить. Прописать методы
import axios from 'axios'
export default {
  name: "McvControlRemont",
  props: {
    currentUser: {
      type: Object,
      required: true
    },
    id: {
      type: String,
      required: true
    },
    autoId: {
      type: String,
      required: true
    },
    remontName: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      sResult: null,
      remontUpd: null
    }
  },
  methods: {
   deleteRemont(e) {
    e.preventDefault();
    let res = confirm('Действительно хотите удалить выбранную строку с ремонтом ~ ' + this.remontName + '~ ? \r\n (не получится если есть дочерние ремонты)');
    if (res) {
      this.remontUpd = true;
      let oData = {}
      oData['user_id'] = this.currentUser._id
      oData['token'] = this.currentUser.token
      oData['id'] = this.id
      oData['auto_id'] = this.autoId

      axios.post('/delete_my_remont', oData)
        .then((res) => {
          if (res.data.deleted == true) {
            this.sResult = 'Удалено'
          } else if (res.data.deleted == 'have_data') {
            /// TODO: вот тут бы видеть эти дочерние ремонты. А как их отображать-то?
            this.sResult = "К ремонту привязаны дочерние ремонты. Сначала нужно их удалить";
          } else if (res.data.deleted == 'no_data') {
            this.sResult = 'У текущего пользователя нет ремонта с таким id';
          } else {
            this.sResult = 'Произошла ошибка. Попробуйте еще раз';
          }
          
          if (this.sResult == 'Удалено') {
            this.$root.$refs.showMessageForm.openForm('success', this.sResult);
            this.$emit('reload', ['deleted', this.autoId ]); 
          } else {
            this.$root.$refs.showMessageForm.openForm('error', this.sResult);
          }
          this.remontUpd = null;
        })
        .catch((error) => {
          this.remontUpd = null;
          console.error(error)
        })
    }
   },
   editRemont() {
      this.remontUpd = true;
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
        this.remontUpd = null;    
      })
   }

  },
  mounted() {
  }
}

</script>