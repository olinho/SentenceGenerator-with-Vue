<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h3>Words Manager</h3>
        <br>
        <div id="dynamic-component-demo" class="demo">
          <button
            v-for="tab in tabs"
            v-bind:key="tab"
            v-bind:class="['tab-button', {active: currentTab === tab }]"
            v-on:click="currentTab = tab">{{ tab }}</button>

        </div>
      </div>
    </div>
  </div>

</template>

<script>

  export default {
    name: 'WordsManager',
    data() {
      return {
        currentTab: 'Equal',
        tabs: ['Equal', 'Higher', 'The highest'],
      };
    },
    computed: {
      currentTabComponent() {
        return 'tab-' + this.currentTab.toLowerCase();
      },
    },
  }
</script>

<style scoped>
  .tab-button {
    padding: 6px 10px;
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    border: 1px solid #ccc;
    cursor: pointer;
    background: #f0f0f0;
    margin-bottom: -1px;
    margin-right: -1px;
  }
  .tab-button:hover {
    background: #e0e0e0;
  }
  .tab-button.active {
    background: #e0e0e0;
  }
  .tab {
    border: 1px solid #ccc;
    padding: 10px;
  }
</style>
