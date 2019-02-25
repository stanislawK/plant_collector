import Vue from 'vue';
import Vuex from 'vuex';

import register from './modules/register';
import auth from './modules/auth';
import plant from './modules/plant';

Vue.use(Vuex);


const store = new Vuex.Store({
  state: {},
  getters: {},
  mutations: {},
  actions: {},

  modules: {
    register,
    auth,
    plant
  }
})

export default store;
