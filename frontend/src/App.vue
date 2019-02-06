<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> |
      <router-link to="/register">Zarejestruj się</router-link> |
      <router-link to="/login">Zaloguj</router-link> |
      <span v-if="isLoggedIn"><a @click="onLogout">Wyloguj</a></span> |
    </div>
    <router-view/>
  </div>
</template>
<script>
  export default {
    created() {
      this.$store.dispatch('auth/tryAutoLogin')
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
<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
