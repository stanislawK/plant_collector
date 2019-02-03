import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from './views/Home.vue'
import Register from './components/Register.vue'
import Confirmation from './components/Confirmation.vue'
import SignIn from './components/SignIn.vue'

Vue.use(VueRouter)

export default new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    },
    {
      path: '/register', component: Register
    },
    {
      path: '/confirm/:id', component: Confirmation
    },
    {
      path: '/login', component: SignIn
    },
  ]
})
