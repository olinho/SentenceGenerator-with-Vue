<template>
  <div>
    <td>
      <a href="#" @click.prevent="seen = !seen">Inflection</a>
        <div @click.alt.prevent="seen = !seen">
          <div v-if="seen">
            <NounInflectionComponent
              v-if="description.czesc_mowy === 0"
              v-bind:description="description">
            </NounInflectionComponent>
            <VerbInflectionComponent
              v-if="description.czesc_mowy === 1"
              v-bind:description="description">
            </VerbInflectionComponent>
            <AdjectiveInflectionComponent
              v-if="description.czesc_mowy === 2"
              v-bind:description="description">>
            </AdjectiveInflectionComponent>
          </div>
        </div>
    </td>

  </div>
</template>

<script>
  import NounInflectionComponent from './NounInflectionComponent';
  import AdjectiveInflectionComponent from './AdjectiveInflectionComponent';
  import VerbInflectionComponent from './VerbInflectionComponent';

  export default {
    name: "Inflection",
    components: {AdjectiveInflectionComponent, NounInflectionComponent, VerbInflectionComponent},
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
