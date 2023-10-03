<template>
  <div class="repair-catalog">
      <h1>Каталог ремонтов к машине {{ auto.name }}</h1>
  </div>
</template>

<script>


export default {
  name: "McvRepairCatalog",
  props: {
    auto_id: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      auto: null,
      repairList: null
    }
  },
  methods: {
    created() {
      // TODO: по адйшинку auto_id выдернуть машину и ремонты, к ней привязанные
    }
  }
}

</script>