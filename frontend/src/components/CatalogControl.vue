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
      }
    },
    data() {
      return {
        sResult: null,
      }
    },
    methods: {
     deleteAuto() {
        
     }
    },
    mounted() {
    }
  }
  
  </script>