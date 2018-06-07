<template>
    <div class="container">
      <div class="row">
        <div class="col-sm-10">
          <div class="row">
            <div class="col-sm-5">
              <h3>Polish Dictionary</h3>
            </div>
            <div class="col-sm-5">
              <label>Incoming data status:</label>
              <span v-if="this.incomingDataStatus === 'success'" class="positive">{{incomingDataStatus}}</span>
              <span v-else class="negative">{{incomingDataStatus}}</span>
              <br>
              <div>{{updatedWord}}</div>
            </div>
          </div>
          <hr><br/><br/>
          <button type="button" class="btn btn-success btn-sm" v-b-modal.word-modal>
            Add word
          </button>
          <br><br>
          <input ref="searchInputRef" v-model="question" title="searcher">
          <p>{{ answer }}</p>
          <p>{{ searchingText }}</p>
          <br><br>
          <h3>Filter by part of speech</h3>
          <div class="btn-group"
               v-for="num in Object.keys(this.partOfSpeechMapper)"
          >
            <input type="checkbox" v-bind:id="num" v-model="partOfSpeechFilterManager[num]">
              <label v-bind:for="num"> {{partOfSpeechMapper[num]}}</label>
          </div>
          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">Word</th>
                <th scope="col">Part of speech</th>
                <th scope="col">Inflection</th>
                <th scope="col">Management</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, key, index) in filteredDict" :key="index">
                <td v-if="item.updated > 0" class="positive">
                  {{ key }}
                </td>
                <td v-else>
                  {{ key }}
                </td>
                <td>{{ mapNumPartOfSpeechToName(item.czesc_mowy) }}</td>
                <!--<td>{{ getInflection(item) }}</td>-->
                <inflection v-bind:description="item">
                </inflection>
                <td>
                  <button class="btn btn-warning btn-sm">Update</button>
                  <button class="btn btn-danger btn-sm">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <b-modal ref="addWordModal"
               id="word-modal"
               title="Add a new word"
               hide-footer>
        <b-form @submit="onSubmit" @reset="onReset" class="w-100">
          <b-form-group id="form-word-group"
                        label="Word:"
                        label-for="form-word-input">
            <b-form-input id="form-word-input"
                          type="text"
                          v-model="addWordForm.word"
                          required
                          placeholder="Enter word">
            </b-form-input>
          </b-form-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-form>
      </b-modal>
    </div>
</template>

<script>
  import axios from 'axios';
  import inflection from "./inflection";

  export default {
    name: 'PolishDict',
    components: {inflection},
    data() {
      return {
        question: '',
        answer: 'Nothing to filter',
        searchingText: '',
        incomingDataStatus: '',
        updatedWord: '',
        words: {},
        filteredDict: {},
        partOfSpeechMapper: {},
        partOfSpeechFilterManager: {},
        lastlyClickedPartOfSpeechNumFilter: -1,
        addWordForm: {
          word: '',
        },
      };
    },
    watch: {
      question() {
        this.answer = 'Waiting for finishing writing...';
        this.filterWords();
      },
      lastlyClickedPartOfSpeechNumFilter: function(val) {
        console.log('Lastly clicked: ' + val);
        console.log(this.partOfSpeechFilterManager[val]);
        this.partOfSpeechFilterManager[val] = !this.partOfSpeechFilterManager[val];
        console.log(this.partOfSpeechFilterManager[val]);
      },
    },
    mounted() {
      this.setFocus();
    },
    created() {
      this.getWords();
      this.getPartOfSpeechMapper();
      // this.debouncedGetAnswer = _.debounce(this.filterWords, 500);
    },
    methods: {
      onChangePartOfSpeechFilter(num) {
        this.lastlyClickedPartOfSpeechNumFilter = num;
        this.partOfSpeechFilterManager[num] = !this.partOfSpeechFilterManager[num];
        console.log(this.partOfSpeechFilterManager[num]);
      },
      getWords() {
        const path = 'http://localhost:5000/polish_dict';
        axios.get(path)
          .then((res) => {
            this.words = res.data.dictionary;
            this.incomingDataStatus = res.data.status;
            this.filteredDict = this.words;
          })
          .catch((error) => {
            console.log(error);
          });
      },
      initForm() {
        this.addWordForm.word = '';
      },
      addWord(payload) {
        const path = 'http://localhost:5000/polish_dict';
        axios.post(path, payload)
          .then((res) => {
            this.getWords();
            this.updatedWord = res.data.updated_word;
          })
          .catch((error) => {
            console.log(error);
            this.getWords();
          });
      },
      onSubmit(evt) {
        evt.preventDefault();
        this.$refs.addWordModal.hide();
        const payload = {
          word: this.addWordForm.word,
        };
        this.addWord(payload);
        this.initForm();
      },
      onReset(evt) {
        evt.preventDefault();
        this.$refs.addWordModal.hide();
        this.initForm();
      },
      setFocus() {
        this.$refs.searchInputRef.focus();
      },
      filterWords() {
        let text = this.question;
        this.filteredDict = Object.keys(this.words)
          .filter(key => key.startsWith(text))
          .reduce((filtered, key) => {
            filtered[key] = this.words[key];
            return filtered;
          }, {});
        let filteredWords = Object.keys(this.filteredDict);
        this.answer = filteredWords.length > 0 && text ? filteredWords : '';
      },
      getPartOfSpeechMapper() {
        const path = 'http://localhost:5000/part_of_speech_mapper';
        axios.get(path)
          .then((res) => {
            this.partOfSpeechMapper = res.data;
            this.resetPartOfSpeechFilterManager();
          })
          .catch((error) => {
            console.log(error);
          });
      },
      resetPartOfSpeechFilterManager() {
        Object.keys(this.partOfSpeechMapper).forEach((key) => {
          this.partOfSpeechFilterManager[key] = false;
        });
      },
      mapNumPartOfSpeechToName(t) {
        return this.partOfSpeechMapper[t];
      },
      getInflection(description) {
        let partOfSpeech = description['czesc_mowy'];
        let odmianaNodeName = '';
        if (partOfSpeech === 0) {
          odmianaNodeName = 'koniugacja';
        } else if (partOfSpeech === 1) {
          odmianaNodeName = 'deklinacja';
        } else if (partOfSpeech === 2) {
          odmianaNodeName = 'deklinacja';
        }
        else {
          odmianaNodeName = '';
        }
        return odmianaNodeName;
      },
    },
  };
</script>

<style scoped>
  .positive {
    background-color: #71dd8a;
  }
  .negative {
    background-color: #C21F39;
  }
  .tab-button.active {
    background: #e0e0e0;
  }
</style>