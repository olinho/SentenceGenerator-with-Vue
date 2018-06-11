import Vue from 'vue';
import Router from 'vue-router';
import Ping from '@/components/Ping';
import Words from '@/components/Words';
import PolishDict from '@/components/PolishDict';
import WordsManager from '@/components/WordsManager';
import Inflection from '@/components/InflectionComponent';


Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/words_manager',
      name: 'WordsManager',
      component: WordsManager,
    },
    {
      path: '/words',
      name: 'Words',
      component: Words,
    },
    {
      path: '/polish_dict',
      name: 'PolishDict',
      component: PolishDict,
    },
    {
      path: '/inflection',
      name: 'Inflection',
      component: Inflection,
    }
  ],
  mode: 'history',
});
