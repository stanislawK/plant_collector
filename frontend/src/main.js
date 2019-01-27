import Vue from 'vue'
import App from './App.vue'
import Vuelidate from 'vuelidate'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import router from './router'
import store from './store/index.js'

Vue.config.productionTip = false
Vue.use(Vuelidate)
Vue.use(Vuetify)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
