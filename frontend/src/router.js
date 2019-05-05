import Vue from 'vue'
import VueRouter from 'vue-router'
import store from './store'
import HomePage from './components/HomePage.vue'
import Register from './components/Register.vue'
import Confirmation from './components/Confirmation.vue'
import SignIn from './components/SignIn.vue'
import AddPlant from './components/AddPlant.vue'
import Plant from './components/Plant.vue'
import Plants from './components/Plants.vue'
import EditPlant from './components/EditPlant.vue'

Vue.use(VueRouter)

export const homeRoute = {
  path: '/',
  name: 'home',
  component: HomePage,
  name: 'HomePage'
};
export const registerRoute = {
  path: '/register',
  component: Register,
  name: 'Register'
};
export const confirmationRoute = {
  path: '/confirm/:id',
  component: Confirmation,
  name: 'Confirmation'
};
export const loginRoute = {
  path: '/login',
  component: SignIn,
  name: 'Login'
};
export const plantRoute = {
  path: '/plant',
  component: Plant,
  name: 'Plant'
};
export const newPlantRoute = {
  path: '/plant/new',
  component: AddPlant,
  name: 'NewPlant'
};
export const editPlantRoute = {
  path: '/plant/:plant_id/edit',
  component: EditPlant,
  name: 'EditPlant'
};
export const plantsRoute = {
  path: '/plants',
  component: Plants,
  name: 'Plants'
};
export const pageNotFoudRoute = {
  path: '*',
  name: 'PageNotFound',
  component: HomePage,
  props: { pageNotFound: true }
};

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    homeRoute,
    registerRoute,
    confirmationRoute,
    loginRoute,
    plantRoute,
    newPlantRoute,
    editPlantRoute,
    plantsRoute,
    pageNotFoudRoute
  ]
});

const openRoutes =
[
  homeRoute.name,
  confirmationRoute.name,
  registerRoute.name,
  loginRoute.name
];

router.beforeEach((to, from, next) => {
  if (to.name === pageNotFoudRoute) {
    return next();
  }

  if (openRoutes.includes(to.name)) {
    return next();
  }

  // Redirect to login if unauthenticated user tries to access closed route
  if (!store.getters['auth/isLoggedIn'] && !openRoutes.includes(to.name)) {
    return next({ path: loginRoute.path });
  }
  return next();
});

export default router;
