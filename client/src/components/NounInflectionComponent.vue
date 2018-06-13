<template>
  <DeclinationComponent
    v-bind:declination="description.deklinacja">
  </DeclinationComponent>
</template>

<script>
  import DeclinationComponent from './DeclinationComponent';

  export default {
    name: "NounInflectionComponent",
    components: {DeclinationComponent},
    data() {
      return {};
    },
    props: ['description'],
  }
</script>

<style scoped>

</style>
