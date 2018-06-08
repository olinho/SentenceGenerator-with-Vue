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
              <span v-bind:class="incomingDataClass">{{ incomingDataStatus }}</span>
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
          <div class="d-lg-inline-flex">
            <template v-for="(mapperVal, num, mapperIndex) in partOfSpeechMapper">
                <div style="margin: 10px;">
                  <input type="checkbox" name="listOfPartOfSpeech"
                       :id="mapperIndex"
                       :key="num"
                       v-on:click="updateLastlyClickedFilter(num)">
                  <label v-bind:for="num"> {{partOfSpeechMapper[num]}}</label>
                </div>
            </template>
          </div>
          <hr>
          <div>{{ activeFilters }}</div>
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
              <tr v-for="(item, key, index) in filteredDict"
                  :key="index"
                  v-if="getListOfActivePartOfSpeechFilters().indexOf(item.czesc_mowy) > -1">
                <td v-bind:class="[{positive: item.updated > 0}]">
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
  import inflection from './inflection';

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
        activeFilters: {},
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
        // this.partOfSpeechFilterManager[val] = !this.partOfSpeechFilterManager[val];
        console.log(this.partOfSpeechFilterManager[val]);
      },
    },
    computed: {
      incomingDataClass() {
        return {
          positive: this.incomingDataStatus === 'success',
          negative: this.incomingDataStatus !== 'success',
        }
      },
    },
    mounted() {
      this.setFocus();
    },
    created() {
      this.getWords();
      this.getPartOfSpeechMapper();
      this.selectAllPartOfSpeechFilters();
    },
    methods: {
      getListOfActivePartOfSpeechFilters() {
        let filteredPartOfSpeechNumList = [];
        Object.keys(this.activeFilters).forEach((k) => {
          if (this.activeFilters[k]) {
            filteredPartOfSpeechNumList.push(parseInt(k));
          }
        });
        return filteredPartOfSpeechNumList;
      },
      updateLastlyClickedFilter(num) {
        let newBool = !this.partOfSpeechFilterManager[num];
        this.$set(this.partOfSpeechFilterManager, num, newBool);
        this.updateActiveFilters();
      },
      selectAllPartOfSpeechFilters() {
        Object.keys(this.activeFilters).forEach((k) => {
          this.$set(this.activeFilters, k, true);
        });
      },
      updateActiveFilters() {
        let partOfSpeechManager = this.partOfSpeechFilterManager;
        Object.keys(partOfSpeechManager).forEach((k) => {
          if (partOfSpeechManager[k]) {
            this.$set(this.activeFilters, k, true);
          } else {
            this.$set(this.activeFilters, k, false);
          }
        });
      },
      updateFilteredWords() {
        let filterList = this.getListOfActivePartOfSpeechFilters();
        let newDict = {};
        let oldDict = this.filteredDict !== {} ? this.filteredDict : this.words;
        Object.keys(oldDict).forEach((k) => {
          try {
            let node = oldDict[k];
            let nodeKeyName = 'czesc_mowy';
            if  (hasNodeKey(node,nodeKeyName)){
              if (filterList.indexOf(node[nodeKeyName]) > -1) {
                newDict[k] = oldDict[k];
              }
            }
          } catch (e) {
          }
        });
        this.filteredDict = newDict;
      },
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

  function hasNodeKey(node, keyName) {
    try {
      return keyName in node;
    } catch (e) {
      console.log(' not in');
    }

  }
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
