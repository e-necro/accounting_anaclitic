<template>
  <div class="add-remont dialog" :class="showed">
    <label class="dlg-back" for="dialog_state"></label>
      <div class="dlg-wrap">
        <div class="closing_cross" @click="closeForm"></div>
        <div class="row modal-content">
          <div class="modal-body">
            <h2 class="modal-caption">{{ title }}</h2>
            <div v-if="sResult !== null" class="add-remont__result"> {{ sResult }}</div>
            <form v-else class="add-remont__cont" action="javascript:void(0);">
              <label for="add-remont-name">
                Название: 
                <input type="text" id="remont-name" name="remont-name" v-model="remont_name" required title="Название ремонта не может быть пустым">
              </label>
              <label for="add-remont-parent" >
                  <!-- <p data-tooltip="н-р, замена тормозных колодок относится к ремонту колеса, которая в свою очередь относится к ремонту ходовки и т.д. Смотря что уже было добавлено.">
                    Есть ли родительский ремонт? <br/>
                    НЕ обязательно<br/>
                  </p> -->
                <div id="category_container"></div>
              </label>
              <label for="add-remont-start_date">
                Дата начала ремонта:
                <input type="date" id="remont-date-start" name="remont-date-start" v-model="start_date"  title="">
              </label>
              <label for="add-remont-end_date">
                Дата окончания ремонта:
                <input type="date" id="remont-date-end" name="remont-date-end" v-model="end_date"  title="">
              </label>
              <label for="add-remont-end_date">
                Примерное затраченное время(сколько часов):
                <input type="number" min="1" max="1000" id="remont-elapced-time" name="remont-elapced-time" v-model="remont_elapced_time"  title="1">
              </label>
              <label for="add-remont-price">
                Затраченная сумма:
                <input type="number" min="0" id="remont-price" name="remont-price" v-model="remont_price"  title="">
              </label>
              <label for="add-remont-comment">
                Краткое описание: 
                <input type="text" id="remont-comment" name="remont-comment" v-model="remont_comment" required title="Добавьте описание">
              </label>
              <div class="button-container">
                <button @click="closeForm">Отмена</button>
                <button @click="saveRemont" :disabled="disabled">Сохранить</button>
              </div>
            </form>
          </div>
        </div>
      </div>
  </div>
</template>

<script>

import axios from 'axios'

export default {
  name: "McvRemontAdd",
  props: {
    currentUser: {
      type: Object,
      required: true
    },
    auto_id: {
      type: Number,
      required: true
    }
    // toShow: {
    //   type: Boolean,
    //   required: true
    // }
  },
  data() {
    return {
      disabled: false,
      remont_name: null,
      remont_comment: null,
      remont_category_id: null,
      remont_category_html_parent: '',
      remont_category_html_childs: '',
      remont_price: null,
      remont_elapced_time: null,
      start_date: null,
      end_date: null,
      sResult: null,
      showed: '',
      resolver: null,
      title: 'Добавление ремонта',
    }
  },
  components: {

  },
  computed: {
 
  },
  methods: {
    saveRemont(e) {
      e.preventDefault();
      this.disabled = true;
      // TODO: если будет родитель выбран, то на бэке рассчитать top_parent_id и level
      if (this.remont_name.trim() !== '' && this.remont_price > 0 ) {
        let oData = {}
        oData['user_id'] = this.currentUser._id
        oData['token'] = this.currentUser.token
        oData['name'] = this.remont_name.trim()
        oData['comment'] = this.remont_comment.trim()
        oData['category_id'] = this.remont_category_id
        oData['price'] = this.remont_price
        oData['start_date'] = this.start_date
        oData['end_date'] = this.end_date
        oData['elapced_time'] = this.remont_elapced_time


        oData['auto_id'] = this.auto_id;
        axios.post('/add_my_remont', oData)
          .then((res) => {/// TODO: дальше не делано
            /*
            * Добавляются данные, но нет parent_id и тд. так же проверки успешности добавления нету. ну и поведение формы проверить тоже
            */
            if (res.data.updated == true) {
              this.sResult = 'Данные обновлены!'             
            } else {
              this.sResult = "Данные не изменены. Те же самые? Попробуйте еще раз"
            }
            this.$emit('close-form', 'updated');   
          })
          .catch((error) => {
            console.error(error)
          })
        this.resolver = null;

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
      this.updatedCategories();
      this.showed = 'dialog_open';
      this.name = params['name'];
      this.comment = params['comment'];
      if (params['date_create'] !== undefined) {
        this.date = params['date_create'];
      }
      // this.auto_id = params['_id'];
      this.title = '';
      this.resolver = resolve;
      this.sResult = null;
    },
    openForAdd() {
      this.updatedCategories();
      this.showed = 'dialog_open';
      this.name = null;
      this.comment = null;
      let dt = new Date().toISOString().slice(0,10);
      this.date = dt;
      // this.auto_id = null;
      // this.title = 'Добавление ремонта'; тупо чтоб не светилось
      this.resolver=null
      this.sResult = null;
    },
    updatedCategories() {
      /*
      - Сделать 2 переменки для родительских и дочерних категорий. В родительской по дефолту первая же вывбирается. И автоматом подгружаются ее дочерние (тут замутить функцию, что обновлять вывод дочерних будет). 
      - так же добавить кнопки добавления категорий. Лучше отдельной формой, где редактировать и удалять их можно. После закрытия формы послать запрос на обновление категорий в родительской форме
      
      */
      if (this.$store.categories) {
        // нарисовать  html 
        this.remont_category_html_parent = `
          <div id="parent_category" >
            <h5 data-id=''>Категория ремонта: <p> </p></h5>
          <ul class="add-remont-category-list add-remont-category-list_parent">
        `;
        let sdopClass = ' selected';
        let ii = 0;
        for (const [key, item] of Object.entries(this.$store.categories)) {
          this.remont_category_html_parent += `<li class="add-remont-category-item ` +sdopClass+ `" data-category-id="${key}">${item.name}</li>`;
          if (sdopClass.length > 0) {
            sdopClass = '';
          }
          
          if ('children' in item) {
            if (ii == 0) {
              this.remont_category_html_childs += `<ul class="add-remont-category-list add-remont-category-list_child showed" data-parent-id="${key}">`;
              ii++;
            } else {
              this.remont_category_html_childs += `<ul class="add-remont-category-list add-remont-category-list_child" data-parent-id="${key}">`;
            }
              this.remont_category_html_childs += `<li class="add-remont-category-item add-remont-category-item_child" data-category-id="-1">не выбрано</li>`;
              for (const [keyChild, child] of Object.entries(item.children)) {
                this.remont_category_html_childs += `<li class="add-remont-category-item add-remont-category-item_child" data-category-id="${keyChild}">${child.name}</li>`;
            }
            this.remont_category_html_childs += `</ul>`;
          }
          
        }
        this.remont_category_html_childs += `</div>`; /// for id="child_category"
        this.remont_category_html_parent += `</ul> </div>`;

        this.remont_category_html_parent += `<div id="child_category" data-id='-1'>Подкатегория ремонта: <p>не выбрано</p>`;


        // воткнуть в контейнер и првязать события
        let category_container = document.getElementById('category_container');
        category_container.innerHTML = this.remont_category_html_parent + this.remont_category_html_childs;

        document.querySelector('#parent_category > h5').dataset.id = document.getElementsByClassName('add-remont-category-item selected')[0].dataset.categoryId;
        document.querySelector('#parent_category > h5').innerHTML = 'Категория ремонта: <p>' + document.getElementsByClassName('add-remont-category-item selected')[0].innerHTML + '</p>';
        let parentItems = document.getElementsByClassName('add-remont-category-item')
        let categorySelectorLabelid = '#parent_category > h5 > p';

        for (let i = 0; i < parentItems.length; i++) {
          parentItems[i].addEventListener('click', function(event)  { 
            let category_id = event.target.dataset.categoryId;
            if (event.target.classList.value.includes('add-remont-category-item_child')) {
              // значит тыкнут был вариант из подкатегорий
              categorySelectorLabelid = '#child_category > p';
            } else {
              categorySelectorLabelid = '#parent_category > h5 > p';
            }
            
            let parentNaimer = document.querySelector(categorySelectorLabelid);
            parentNaimer.dataset.id = category_id;
            parentNaimer.innerHTML = event.target.innerHTML;
            Array.from(parentItems).forEach(function(el) {
              el.classList.remove('selected');
            }); 
            this.classList.add('selected');

            // childs
            let childs =  document.querySelectorAll('.add-remont-category-list_child');
            Array.from(childs).forEach((el) => {
              el.classList.remove('showed');
            })
            
            let childItem = document.querySelector('.add-remont-category-list_child[data-parent-id="' + category_id + '"]');
            
            if (childItem !== undefined) { 
              childItem.classList.add('showed');
            }

          }, false);
        }

      }
    }
  },
  mounted() {
    // this.openForEdit()
    // this.title = 'Добавить ремонт';
    
  }, 
}

</script>