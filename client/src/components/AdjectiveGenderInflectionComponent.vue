<template>
  <div class="container">
    <hr>
    <h2>{{ gender }}</h2>
    <table>
      <thead>
      <tr>
        <th scope="col" v-if="this.hasDataOnLevel[0]">Adjective</th>
        <th scope="col" v-if="this.hasDataOnLevel[1]">Comperative form</th>
        <th scope="col" v-if="this.hasDataOnLevel[2]">Superlative form</th>
      </tr>
      </thead>
      <tbody>
      <tr>
          <td v-show="hasDataOnLevel[0]">
            <DeclinationComponent
              v-bind:declination="genderDeclination.rowny"
              v-bind:level="'0'">
            </DeclinationComponent>
          </td>
          <td v-show="hasDataOnLevel[1]">
            <DeclinationComponent
              v-bind:declination="genderDeclination.wyzszy"
              v-bind:level="'1'">
            </DeclinationComponent>
          </td>
          <td v-show="hasDataOnLevel[2]">
            <DeclinationComponent
              v-bind:declination="genderDeclination.najwyzszy"
              v-bind:level="'2'">
            </DeclinationComponent>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import DeclinationComponent from './DeclinationComponent';

  export default {
    name: "AdjectiveGenderInflectionComponent",
    components: {DeclinationComponent},
    props: ['genderDeclination', 'gender'],
    data() {
      return {
        // if node for given level has any data
        hasDataOnLevel: [true, true, true],
      };
    },
    created() {
      this.$on('emptyDataDetection', this.updateDataStatusForLevel);
    },
    methods: {
      updateDataStatusForLevel(num) {
        this.$set(this.hasDataOnLevel, num, false);
        console.log('updating data status for level ' + this.hasDataOnLevel);
      },
    },
  };
</script>

<style scoped>
  div {
    text-align: center;
  }
  table {
    text-align: center;
  }
  table th {
    border: 2px solid #007bff;
  }
</style>
