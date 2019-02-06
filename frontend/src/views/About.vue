<template>
  <div class="about">
    <h1>This is an about page</h1>
    <p>
      {{user}}
    </p>
  </div>
</template>
<script>
export default {
  name: 'home',
  data() {
    return {
      user: ''
    }
  },
  created() {
    this.$store.dispatch('auth/fetchUser')
  },
  computed: {
    getUser() {
      this.user = this.$store.getters['auth/getUser']
    }
  }
}
</script>
