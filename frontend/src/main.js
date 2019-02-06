import Vue from 'vue'
import App from './App.vue'
import Vuelidate from 'vuelidate'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import axios from 'axios'
import router from './router'
import store from './store/index.js'

Vue.config.productionTip = false
Vue.use(Vuelidate)
Vue.use(Vuetify)

axios.defaults.baseURL = 'http://0.0.0.0:5000'
axios.interceptors.response.use(response => {
  return response;
}, err => {
  const refresh = localStorage.getItem('refresh_token')
  if (err.response.status == 401 && refresh) {
    store.dispatch('auth/logoutRefresh')
  } else {
    console.log(err.response.status)
    console.log(err.response.data.msg)
  }
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
