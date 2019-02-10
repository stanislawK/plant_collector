<template>
  <div class="header">
      <v-navigation-drawer
        fixed
        v-model="drawer"
        right
        app
      >
        <v-list dense>
          <v-list-tile to='/'>
            <v-list-tile-action>
              <v-icon>home</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Home</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile to="/login">
            <v-list-tile-action>
              <v-icon>exit_to_app</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Zaloguj</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile v-if="isLoggedIn" @click="onLogout">
            <v-list-tile-action>
              <v-icon>power_settings_new</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Wyloguj</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile to="/register">
            <v-list-tile-action>
              <v-icon>assignment</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Zarejestruj</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-navigation-drawer>
      <v-toolbar color="cyan" dark fixed app>
        <v-spacer></v-spacer>
        <v-toolbar-title>Application</v-toolbar-title>
        <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
      </v-toolbar>

  </div>
</template>

<script>
export default {
  data() {
    return {
      drawer: false
    }
  },
  methods: {
    onLogout() {
      this.$store.dispatch('auth/logout')
      .then(() => {
        this.$router.push('/')
      })
    }
  },
  computed: {
    isLoggedIn() {
      return this.$store.getters['auth/isLoggedIn']
    }
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .header {
      min-height: 20vh !important;
    }
</style>
