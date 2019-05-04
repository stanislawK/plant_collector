<template>
  <div>
    <v-app>
      <app-header></app-header>
      <v-content>
        <v-container fluid>
          <v-alert
          type="success"
          :value="successAlert"
          @click="onCloseAlert"
          dismissible
          transition="slide-y-transition"
          >{{successAlert}}</v-alert>
          <router-view/>
        </v-container>
      </v-content>
    </v-app>
  </div>
</template>
<script>
  import { mapGetters } from 'vuex'
  import Header from './components/Header.vue'
  export default {
    components: {
      'app-header': Header
    },
    methods: {
      onCloseAlert() {
        this.$store.commit('auth/clearMsg')
      }
    },
    beforeCreate() {
      this.$store.dispatch('auth/tryAutoLogin')
    },
    computed: {
      ...mapGetters({
        successAlert: 'auth/getMsg'
      })
    }
  }
</script>
<style>
</style>
