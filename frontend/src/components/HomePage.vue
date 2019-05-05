<template>
  <div>
    <v-app>
      <v-layout justify-center>
        <v-flex xs12 sm6 text-xs-center>
          <v-alert
          type="success"
          :value="successAlert"
          @click="onCloseAlert"
          dismissible
          transition="slide-y-transition"
          >{{successAlert}}</v-alert>
          <v-alert
          type="error"
          :value="notFoundAlert"
          @click="notFoundAlert = false"
          dismissible
          transition="slide-y-transition"
          >Strona o podanym adresie nie istnieje</v-alert>
          <v-btn
          color="info"
          to="/login"
          >
            Zaloguj
          </v-btn>
          <v-btn
          color="success"
          to="/register"
          >
            Zarejestuj
          </v-btn>
        </v-flex>
      </v-layout>
    </v-app>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  props: {
    pageNotFound: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      notFoundAlert: this.pageNotFound
    }
  },
  methods: {
    onCloseAlert() {
      this.$store.commit('auth/clearMsg')
    }
  },
  computed: {
    ...mapGetters({
      successAlert: 'auth/getMsg'
    })
  },
  beforeRouteLeave (to, from, next) {
    if (this.successAlert) {
      this.onCloseAlert()
    }
    if (this.notFoundAlert) {
      this.notFoundAlert = false
    }
    return next()
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
