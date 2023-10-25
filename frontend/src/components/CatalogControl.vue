<template>
    <div class="control" >
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
      }
    },
    methods: {
     deleteAuto() {
      let res = confirm('Действительно хотите удалить машину ~ ' + this.carName + '~ ? \r\n (не получится если к ней уже привязаны ремонты)');
      if (res) {
        let oData = {}
        oData['user_id'] = this.currentUser._id
        oData['token'] = this.currentUser.token
        oData['id'] = this.id

        axios.post('/delete_my_auto', oData)
          .then((res) => {
            if (res.data.deleted == true) {
              this.sResult = 'Готово'
              window.location.reload()
            } else if (res.data.deleted == 'have_data') {
              this.sResult = "К машине привязаны ремонты. Сначала нужно их удалить";
            } else {
              this.sResult = 'Произошла ошибка. Попробуйте еще раз';
            }
            
          })
          .catch((error) => {
            console.error(error)
          })
      }
     },
     editAuto() {
        console.log('currentUser: ', this.currentUser, ' id: ', this.id, ' carname: ', this.carName)
        
     }

    },
    mounted() {
    }
  }
  
  </script>