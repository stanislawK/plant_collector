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

const token = localStorage.getItem('token')
if (token) {
  axios.defaults.headers.common['Authorization'] = 'Bearer ' + token
}

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
