<template>
  <div class="container catalog-page">
    <h1>Каталоги</h1>
    <!-- 
    воткнуть во vue.config.js чтоб он sass обрабатывал
    https://cli.vuejs.org/guide/css.html#passing-options-to-pre-processor-loaders
    -->
    <mcv-auto-catalog />
  </div>
</template>

<script>

import McvAutoCatalog from '@/components/AutoCatalog'


export default {
  name: "McvCreateCatalog",
  components: {
    McvAutoCatalog,
  },
}
</script>
