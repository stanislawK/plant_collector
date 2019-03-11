<template>
  <div>
    <v-app>
      <app-header></app-header>
      <router-view/>
    </v-app>
  </div>
</template>
<script>
  import Header from './components/Header.vue'
  export default {
    components: {
      'app-header': Header
    },
    beforeCreate() {
      this.$store.dispatch('auth/tryAutoLogin')
    },
  }
</script>
<style>
</style>
