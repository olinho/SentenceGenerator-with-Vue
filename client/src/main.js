// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import Vue from 'vue';
import App from './App';
import router from './router';

Vue.config.productionTip = false;

Vue.use(BootstrapVue);


// globally scoped data
Vue.mixin({
  methods: {
    // globally scoped function
    hasData(el) {
      return Object.keys(el).length;
    },
  },
  filters: {
    flatten: function(data) {
      if (Array.isArray(data)) {
        return data.join("; ");
      } else {
        return data;
      }
    },
  },
});

/* eslint-disable no-new */
const app = new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});
