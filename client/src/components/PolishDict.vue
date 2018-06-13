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
          <br><br>
          <PartOfSpeechSelector
            v-bind:partOfSpeechMapper="partOfSpeechMapper">
          </PartOfSpeechSelector>
          <div>{{ activeFilters }}</div>
          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col" style="width: 10%">Word</th>
                <th scope="col" style="width: 10%">Part of speech</th>
                <th scope="col" style="width: 50%">Inflection</th>
                <th scope="col" style="width: 10%">Management</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(wordNode, key, index) in filteredDict"
                  :key="index"
                  v-show="doesShowWord(wordNode)">
                <td v-bind:class="[{positive: wordNode.updated > 0}]">
                  {{ key }}
                </td>
                <td>{{ mapNumPartOfSpeechToName(wordNode.czesc_mowy) }}</td>
                <!--<td>{{ getInflection(item) }}</td>-->
                <Inflection v-bind:description="wordNode">
                </Inflection>
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
                          v-model="wordAdditionForm.word"
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
  import PartOfSpeechSelector from './PartOfSpeechSelector';
  import Inflection from './InflectionComponent';

  export default {
    name: 'PolishDict',
    components: {PartOfSpeechSelector, Inflection},
    data() {
      return {
        question: '',
        answer: 'Nothing to filter',
        incomingDataStatus: '',
        updatedWord: '',
        words: {},
        filteredDict: {},
        activeFilters: {},
        partOfSpeechMapper: {},
        partOfSpeechFilterManager: {},
        lastlyClickedPartOfSpeechNumFilter: -1,
        wordAdditionForm: {
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
        return this.incomingDataStatus === 'success' ? 'positive' : 'negative';
      },
    },
    mounted() {
      this.setFocus();
    },
    created() {
      this.getWords();
      this.getPartOfSpeechMapper();
      this.selectAllPartOfSpeechFilters();
      this.$on('updateFilter', this.updateLastlyClickedFilter);
    },
    methods: {
      doesShowWord(item) {
        return this.getListOfActivePartOfSpeechFilters().indexOf(item.czesc_mowy) > -1;
      },
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
        console.log('Updating active filters...');
        let partOfSpeechManager = this.partOfSpeechFilterManager;
        Object.keys(partOfSpeechManager).forEach((k) => {
          if (partOfSpeechManager[k]) {
            this.$set(this.activeFilters, k, true);
          } else {
            this.$set(this.activeFilters, k, false);
          }
        });
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
        this.wordAdditionForm.word = '';
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
          word: this.wordAdditionForm.word,
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

<style>
  .positive {
    background-color: #71dd8a;
    border: 1px solid;
  }
  .negative {
    background-color: #C21F39;
  }
  .tab-button.active {
    background: #e0e0e0;
  }
  table tr:nth-child(3) {
    width: 250px;
  }
</style>
