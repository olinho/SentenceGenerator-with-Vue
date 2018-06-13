<template>
  <div v-if="hasData(description)">
    <AdjectiveGenderInflectionComponent
      v-if="hasData(description.deklinacja.meski)"
      v-bind:genderDeclination="description.deklinacja.meski"
      v-bind:gender="'Masculine'"
    ></AdjectiveGenderInflectionComponent>
    <AdjectiveGenderInflectionComponent
      v-if="hasData(description.deklinacja.zenski)"
      v-bind:genderDeclination="description.deklinacja.zenski"
      v-bind:gender="'Feminine'"
    ></AdjectiveGenderInflectionComponent>
    <AdjectiveGenderInflectionComponent
      v-if="hasData(description.deklinacja.nijaki)"
      v-bind:genderDeclination="description.deklinacja.nijaki"
      v-bind:gender="'Neuter'"
    ></AdjectiveGenderInflectionComponent>
  </div>
</template>

<script>
  import AdjectiveGenderInflectionComponent from './AdjectiveGenderInflectionComponent';

  export default {
    name: "AdjectiveInflectionComponent",
    components: {AdjectiveGenderInflectionComponent},
    data() {
      return {
      };
    },
    props: ['description'],
  }
</script>

<style scoped>

</style>
