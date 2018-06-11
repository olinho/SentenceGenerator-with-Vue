<template>
    <div class="container">
      <ul id="words">
        <li v-for="(item, key, index) in words"
          :key="index"
        >
          <lu>{{key}}: {{item}}</lu>
          <lu>Elements: {{item.length}}</lu>
        </li>
      </ul>
      <p>{{ words }}</p>
    </div>
</template>

<script>
  import axios from 'axios';

    export default {
      name: 'Words',
      data() {
        return {
          words: {},
        };
      },
      methods: {
        getWords() {
          const path = 'http://localhost:5000/words';
          axios.get(path)
            .then((res) => {
              this.words = res.data;
            })
            .catch((error) => {
              console.log(error);
            });
        },
      },
      created() {
        this.getWords();
      },
    };
</script>

<style scoped>

</style>
