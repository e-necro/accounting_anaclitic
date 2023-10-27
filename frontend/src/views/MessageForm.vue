<template>
  <div class="response-message dialog" :class="[showed, showedType]" >
      <div class="dlg-wrap">
        <div class="closing_cross" @click="closeForm"></div>
        <div class="row modal-content">
          <div class="modal-body">
              <h2 v-if="showedType == 'success'" class="modal-caption">Успешно!</h2>
              <h2 v-else-if="showedType == 'error'" class="modal-caption">Ошибка!</h2>
              <div class="response-message__text">{{ sResult }}</div>
          </div>
        </div>
      </div>
    </div>
</template>


<script>

  export default {
    name: "McvMessageForm",
    data() {
      return {
        showed: '',
        showedType: '',
        sResult:''
      }
    },
    methods: {
      closeForm(){
        this.showed = '';
      },
      openForm(className, text) {
        this.showedType = className;
        this.sResult = text;
        this.showed = 'dialog_open';
        // setTimeout(() => {
        //   this.showed = '';
        // }, 5000);
      }
    },
    mounted() {
      // this.showed = 'dialog_open';
      // setTimeout(() => {
      //   this.showed = '';
      // }, 5000);
    }
  }

</script>