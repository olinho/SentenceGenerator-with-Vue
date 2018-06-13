<template>
  <div class="inline-group">
    <h3>Filter by part of speech</h3>
    <div class="row">
      <div v-for="(mapperVal, num, mapperIndex) in partOfSpeechMapper"
          v-bind:key="'partOfSpeech'+mapperIndex">
        <div style="margin: 10px;"
             v-bind:class="[{positive: isChecked[num]}]"
        >
          <input type="checkbox" name="listOfPartOfSpeech"
                 v-model="isChecked[num]"
                 :id="mapperIndex"
                 :key="num"
                 v-on:click="click(num)">
          <label v-bind:for="num"> {{partOfSpeechMapper[num]}}</label>
        </div>
      </div>
    </div>
    <hr>
  </div>

</template>

<script>
  export default {
    name: 'PartOfSpeechSelector',
    data() {
      return {
        isChecked: [],
      };
    },
    props: ['partOfSpeechMapper'],
    methods: {
      click(filterNum) {
        console.log('Filter ' + filterNum.toString() + ' has been already clicked.');
        this.$parent.$emit('updateFilter', filterNum);
      },
    },
  }
</script>

<style scoped>


</style>
