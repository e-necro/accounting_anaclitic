<template>
  <div class="response-message dialog" :class="[showed, showedType]" >
    <label class="dlg-back" for="dialog_state"></label>
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
        if (this.showedType == 'success') {
          this.showed = '';
          window.location.reload
        } 
      },
      openForm(className, text) {
        this.showedType = className;
        this.sResult = text;
        this.showed = 'dialog_open';
        setTimeout(() => {
          if (this.showedType == 'success') {
            this.showed = '';
            window.location.reload;
          }
        }, 3000);
      }
    },
    mounted() {
      // this.showed = 'dialog_open';
      setTimeout(() => {
        this.showed = '';
      }, 5000);
    }
  }

</script>