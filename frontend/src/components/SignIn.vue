<template>
  <div class="register-form">
    <v-app id="register">
      <v-layout justify-center>
        <v-flex xs12 sm6>
          <v-alert
          type="error"
          :value="error_msg ? true : false"
          @click="error_msg=''"
          transition="slide-y-transition"
          >{{error_msg}}</v-alert>
          <v-progress-circular
            v-if="spinner"
            :size="50"
            color="green"
            indeterminate>
          </v-progress-circular>
          <form>
            <v-text-field
            v-model="username"
            label="Nazwa użytkownika"
            required
            :error-messages="usernameErrors"
            @input="$v.username.$touch()"
            @blur="$v.username.$touch()"
            ></v-text-field>
            <v-text-field
            v-model="password"
            label="Hasło"
            :append-icon="show1 ? 'visibility_off' : 'visibility'"
            :type="show1 ? 'text' : 'password'"
            @click:append="show1 = !show1"
            required
            :error-messages="passwordErrors"
            @input="$v.password.$touch()"
            @blur="$v.password.$touch()"
            ></v-text-field>
            <v-btn @click="onSubmit">Zaloguj</v-btn>
          </form>
        </v-flex>
      </v-layout>
    </v-app>
  </div>
</template>

<script>
import { maxLength, required } from 'vuelidate/lib/validators'

export default {
  data() {
    return {
      username: '',
      password: '',
      show1: false,
      error_msg: '',
      spinner: false
    }
  },

  validations: {
    username: { required, maxLength: maxLength(10) },
    password: { required, minLength: maxLength(50) }
  },

  methods: {
    onSubmit() {
      const loginData = {
        username: this.username,
        password: this.password
      }
      this.error_msg = ''
      if(!this.$v.$invalid) {
        this.spinner = true
        this.$store.dispatch('auth/login', loginData)
        .then( res => {
          this.spinner = false
          this.clearForm()
          this.$router.push('/')
        }, error => {
          this.spinner = false
          this.clearForm()
          const err = error.response.data.message
          if (err.password) {
            this.error_msg = "Nieprawidłowa nazwa użytkownika, lub hasło"
          } else if (err.includes('Invalid credentials')) {
            this.error_msg = "Nieprawidłowa nazwa użytkownika, lub hasło"
          } else if (err.includes("wasn't comifired")) {
            this.error_msg = ("Rejestracja nie została dokończona.\
                              Sprawdź skrzynkę email")
          } else if (err.includes("already logged in")) {
            this.error_msg = ("Jesteś już zalogowany")
          } else {
            console.log(error)
          }
        })
      }
    },
    clearForm() {
      this.$v.$reset()
      this.username = ''
      this.password = ''
    }
  },

  computed: {
    usernameErrors() {
      const errors = []
      if (!this.$v.username.$dirty) return errors
      !this.$v.username.maxLength && errors.push(
        'Wprowadź poprawną nazwę użytkownika'
      )
      !this.$v.username.required && errors.push(
        'Nazwa użytkownika jest wymagana'
      )
      return errors
    },
    passwordErrors() {
      const errors = []
      if (!this.$v.password.$dirty) return errors
      !this.$v.password.required && errors.push(
        'Hasło jest wymagane'
      )
      return errors
    },
  },
}
</script>

<style lang="css">
</style>
