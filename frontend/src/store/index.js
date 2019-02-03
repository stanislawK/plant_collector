import Vue from 'vue';
import Vuex from 'vuex';
import register from './modules/register';
import signin from './modules/signin';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {},
  getters: {},
  mutations: {},
  actions: {},

  modules: {
    register,
    signin
  }
})

export default store;
