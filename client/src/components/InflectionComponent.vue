<template>
  <div>
    <td>
      <a href="#" @click.prevent="seen = !seen">Inflection</a>
        <div v-if="seen">
          <NounInflectionComponent
            v-if="description.czesc_mowy === 0"
            v-bind:description="description">
          </NounInflectionComponent>
          <AdjectiveInflectionComponent
            v-if="description.czesc_mowy === 2"
            v-bind:description="description">>
          </AdjectiveInflectionComponent>
        </div>
    </td>

  </div>
</template>

<script>
  import NounInflectionComponent from './NounInflectionComponent';
  import AdjectiveInflectionComponent from './AdjectiveInflectionComponent';

  export default {
    name: "Inflection",
    components: {AdjectiveInflectionComponent, NounInflectionComponent},
    data() {
      return {
        seen: false,
      };
    },
    props: ['description'],
    created() {
      console.log('Created inflection component');
    },
  };
</script>

<style scoped>

</style>
