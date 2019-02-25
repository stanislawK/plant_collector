<template lang="html">
  <div class="confirmation">
      <v-layout justify-center>
        <v-flex xs12 sm6>
          <v-progress-circular
            v-if="spinner"
            :size="50"
            color="green"
            indeterminate>
          </v-progress-circular>
          <div class="unsuccessful" v-if="error">
            <v-alert
            :value="error"
            dismissible
            type="error"
            transition="slide-y-transition">
            {{error}}
            </v-alert>
            <v-btn v-if="!confirmed" to='/register'>Zarejestuj się</v-btn>
            <v-btn v-if="expired" to=''>Wygeneruj nowy link</v-btn>
            <v-btn v-if="confirmed" to='/login'>Zaloguj się</v-btn>
          </div>
          <div class="successful" v-if="success">
            <v-alert
            :value="success"
            dismissible
            type="success"
            transition="slide-y-transition">
            Pomyślnie potwerdzono rejestrację.
            </v-alert>
            <v-btn to='/login'>Zaloguj się</v-btn>
          </div>
        </v-flex>
      </v-layout>
  </div>
</template>

<script>
export default {
  data() {
      return {
        error: '',
        success: '',
        expired: '',
        confirmed: '',
        spinner: true
      }
  },

  created() {
      this.checkConfirmation()
  },

  methods: {
    checkConfirmation() {
      const confId = this.$route.params.id
      this.$store.dispatch('register/confirmation', confId)
        .then(res => {
          this.spinner = false
          if(res.status == 200){
            this.success = true
          }
        }, error => {
          this.spinner = false
          const err = error.response.data.message
          if(err.includes('not found')) {
            this.error = ('Podane potwierdzenie nie istnieje.\
                          Sprawdź link ponownie, lub zarejestuj się')
          } if(err.includes('expired')) {
            this.error = ('Link wygasł. Wygeneruj nowy.');
            this.expired = true
          } if(err.includes('already')) {
            this.error = ('Jesteś już zarejestrowany.');
            this.confirmed = true
          }
        })
    },
  },
}
</script>

<style scoped>
  .confirmation {
    margin: 1em;
  }
</style>
