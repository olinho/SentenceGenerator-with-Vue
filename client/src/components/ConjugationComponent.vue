<template>
  <div>
    <table v-if="isPresentTime">
      <thead>
      <th scope="col">-</th>
      </thead>
      <tbody>
      <tr v-for="n in nList">
        <td v-bind:title="nListPersonMasculine[n]">{{ inflection[n] }}</td>
      </tr>
      </tbody>
    </table>
    <table v-else>
      <thead>
      <th scope="col">Masculine</th>
      <th scope="col">Feminine</th>
      </thead>
      <tbody>
      <tr v-for="n in nList">
        <td v-bind:title="nListPersonMasculine[n]">
          {{ inflection.meski[n] | flatten }}</td>
        <td v-bind:title="nListPersonFeminine[n]">
          {{ inflection.zenski[n] | flatten }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  export default {
    name: "ConjugationComponent",
    props: ['inflection', 'time'],
    data() {
      return {
        nList: [...Array(6).keys()],
        nListPersonMasculine: ['ja', 'ty', 'on', 'my', 'wy', 'oni'],
        nListPersonFeminine: ['ja', 'ty', 'ona', 'my', 'wy', 'one'],
        inflectionLocally: this.inflection,
        timeLocally: this.time,
      };
    },
    computed: {
      isPresentTime() {
        return this.timeLocally === '0';
      },
    },
  }
</script>

<style scoped>

</style>
