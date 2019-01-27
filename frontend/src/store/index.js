import Vue from 'vue';
import Vuex from 'vuex';
import register from './modules/register';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {},
  getters: {},
  mutations: {},
  actions: {},

  modules: {
    register
  }
})

export default store;
