<template>
  <div>
    <table v-if="hasDeclination">
      <thead>
      <tr>
        <th scope="col" v-if="hasSingular">Singular</th>
        <th scope="col" v-if="hasPlural">Plural</th>
      </tr>
      </thead>
      <tbody>
        <tr v-for="n in nList" v-bind:title="nListVariations[n]">
          <td v-if="hasSingular">{{ declination[0][n] }}</td>
          <td v-if="hasPlural">{{ declination[1][n] }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  export default {
    name: "DeclinationComponent",
    // level is used only for adjectives
    props: {
      declination: {
        type: Object,
        required: true,
      },
      level: {
        type: [String],
        validator: function(value) {
          // available values for prop 'level'
          return ['0', '1', '2'].indexOf(value) !== -1;
        },
      },
    },
    data() {
      return {
        nList: [...Array(7).keys()],
        nListVariations: ['Mianownik', 'Dopełniacz', 'Celownik', 'Biernik', 'Narzędnik', 'Miejscownik', 'Wołacz'],
        declinationLocally: this.declination,
        levelLocally: this.level,
      };
    },
    mounted() {
      this.emptyDataPropagator();
    },
    computed: {
      // hasData is globally scoped function, created as mixin in main.js file
      hasDeclination() {
        return this.hasData(this.declinationLocally);
      },
      hasSingular() {
        return this.hasDeclination && this.hasData(this.declinationLocally[0]);
      },
      hasPlural() {
        return this.hasDeclination && this.hasData(this.declinationLocally[1]);
      },
    },
    methods: {
      emptyDataPropagator() {
        if (!this.hasData(this.declinationLocally[0]) && !this.hasData(this.declinationLocally[1])) {
          console.log('lack of data');
          console.log(this.levelLocally);
          this.$parent.$emit('emptyDataDetection', this.levelLocally);
        }
      }
    },

  }
</script>

<style scoped>
  table tr {
    border: 2px solid #1d2124;
  }
  table tr td {
    border: 1px solid darkblue;
  }
  table th {
    border: 1px solid darkblue;
  }
</style>
