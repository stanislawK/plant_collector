<template lang="html">
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
          <v-alert
          type="success"
          :value="successAlert"
          @click="successAlert = !successAlert"
          transition="slide-y-transition"
          >Wysłano pomyślnie. Sprawdź swoją skrzynkę email, w celu dokończenia rejestracji</v-alert>
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
            v-model="email"
            label="Email"
            required
            :error-messages="emailErrors"
            @input="$v.email.$touch()"
            @blur="$v.email.$touch()"
            ></v-text-field>
            <v-text-field
            v-model="password"
            label="Hasło"
            :append-icon="show1 ? 'visibility_off' : 'visibility'"
            :type="show1 ? 'text' : 'password'"
            hint="Min. 8 znaków w tym duże, małe litery, cyfry, oraz znak specjalny"
            @click:append="show1 = !show1"
            required
            :error-messages="passwordErrors"
            @input="$v.password.$touch()"
            @blur="$v.password.$touch()"
            ></v-text-field>
            <v-text-field
            v-model="repeatPassword"
            label="Powtórz hasło"
            :append-icon="show1 ? 'visibility_off' : 'visibility'"
            :type="show1 ? 'text' : 'password'"
            @click:append="show1 = !show1"
            required
            :error-messages="repeatPasswordErrors"
            @input="$v.repeatPassword.$touch()"
            @blur="$v.repeatPassword.$touch()"
            ></v-text-field>
            <v-btn @click="onSubmit">Wyślij</v-btn>
          </form>
        </v-flex>
      </v-layout>
    </v-app>
  </div>
</template>

<script>
import { email, minLength, maxLength, required, helpers, sameAs } from 'vuelidate/lib/validators'

const strength = helpers.regex('strength', /^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*()\-_+<,>.?/~`]).{8,}$/)

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      repeatPassword: '',
      show1: false,
      error_msg: '',
      successAlert: false,
    }
  },

  validations: {
    username: { required, maxLength: maxLength(10) },
    email: { required, email } ,
    password: { required, minLength: minLength(8), strength },
    repeatPassword: { required, sameAsPassword: sameAs('password') }
  },

  methods: {
    onSubmit() {
      const registerData = {
        username: this.username,
        email: this.email,
        password: this.password,
      }
      if (!this.$v.$invalid) {
        this.error_msg = ''
        this.$store.dispatch('register/signup', registerData)
        .then(res => {
          if (res.status == '201') {
            this.successAlert = true;
            this.error_msg = ''
            this.clearForm()
          }
        }, error => {
          const msg = error.response.data.message
          if (msg == "User with that username already exist") {
            this.error_msg = 'Ta nazwa użytkownika instnieje, spróbuj innej'
          } else {
            this.error_msg = 'Błąd rejestracji, spróbuj ponownie'
          }
        })
      } else {
        this.error_msg = "Pola muszą być  wypełnione poprawnie"
      }
    },
    clearForm() {
      this.$v.$reset()
      this.username = ''
      this.email = ''
      this.password = ''
      this.repeatPassword = ''
    }
  },

  computed: {
    usernameErrors() {
      const errors = []
      if (!this.$v.username.$dirty) return errors
      !this.$v.username.maxLength && errors.push(
        'Nazwa nie może być dłuższa niż 10 znaków'
      )
      !this.$v.username.required && errors.push(
        'Nazwa użytkownika jest wymagana'
      )
      return errors
    },
    emailErrors() {
      const errors = []
      if (!this.$v.email.$dirty) return errors
      !this.$v.email.email && errors.push(
        'Wprowadź poprawny adres email'
      )
      !this.$v.email.required && errors.push(
        'Adres email jest wymagany'
      )
      return errors
    },
    passwordErrors() {
      const errors = []
      if (!this.$v.password.$dirty) return errors
      !this.$v.password.minLength && errors.push(
        'Hasło musi mieć min. 8 znaków'
      )
      !this.$v.password.required && errors.push(
        'Hasło jest wymagane'
      )
      !this.$v.password.strength && errors.push(
        'Hasło musi zawierać dużą, małą literę, cyfrę, oraz znak specjalny'
      )
      return errors
    },
    repeatPasswordErrors() {
      const errors = []
      if (!this.$v.repeatPassword.$dirty) return errors
      !this.$v.repeatPassword.sameAsPassword && errors.push(
        'Hasła muszą być takie same'
      )
      !this.$v.repeatPassword.required && errors.push(
        'Powtórzenie hasła jest wymagane'
      )
      return errors
    },
  }
}
</script>

<style>
  .v-alert {
    cursor: pointer;
    text-align: left;
  }
  .v-text-field__details {
    padding: 0.2em;
  }
  .register-form {
    margin: 1em;
  }
</style>
