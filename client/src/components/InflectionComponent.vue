<template>
  <div>
    <td v-if="description.czesc_mowy === 0">{{ description.deklinacja }}</td>
    <td v-else-if="description.czesc_mowy === 1">{{ description.koniugacja }}</td>
    <td v-else-if="description.czesc_mowy === 2">{{ description.deklinacja }}</td>
    <td v-else></td>
  </div>
</template>

<script>
  export default {
    name: "Inflection",
    data() {
      return {};
    },
    props: ['description'],
  }
</script>

<style scoped>

</style>
