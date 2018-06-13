<template>
  <table>
    <thead>
    <th scope="col">Present</th>
    <th scope="col">Past</th>
    <th scope="col">Future</th>
    </thead>
    <tbody>
    <tr>
      <td>
        <ConjugationComponent
          v-bind:inflection="conjugation.terazniejszy"
          v-bind:time="'0'">
        </ConjugationComponent>
      </td>
      <td>
        <ConjugationComponent
          v-bind:inflection="conjugation.przeszly"
          v-bind:time="'1'">
        </ConjugationComponent>
      </td>
      <td>
        <ConjugationComponent
          v-bind:inflection="conjugation.przyszly"
          v-bind:time="'2'">
        </ConjugationComponent>
      </td>
    </tr>
    </tbody>
  </table>
</template>

<script>
  import ConjugationComponent from './ConjugationComponent';

  export default {
    name: "VerbInflectionComponent",
    props: ['description'],
    components: {ConjugationComponent},
    data() {
      return {
        descriptionLocally: this.description,
      };
    },
    computed: {
      conjugation: function() {
        return this.descriptionLocally.koniugacja;
      },
    },
  }
</script>

<style scoped>

</style>
