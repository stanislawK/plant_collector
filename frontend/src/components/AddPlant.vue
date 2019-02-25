<template lang="html">
  <div id="newPlant">
    <v-stepper v-model="page">
      <v-stepper-header>
        <v-stepper-step :complete="page > 1" step="1">Nazwa</v-stepper-step>

        <v-divider></v-divider>

        <v-stepper-step :complete="page > 2" step="2">Opis</v-stepper-step>

        <v-divider></v-divider>

        <v-stepper-step step="3">Zdjęcie</v-stepper-step>
      </v-stepper-header>

      <v-stepper-items>
        <v-stepper-content step="1">
          <v-card
            class="mb-5"
            height="40vh"
          >
            <form>
              <v-text-field
              v-model="name"
              label="Nazwa polska"
              required
              :error-messages="nameErrors"
              @input="$v.name.$touch()"
              @blur="$v.name.$touch()"
              ></v-text-field>
              <v-text-field
              v-model="latin"
              label="Nazwa Łacińska"
              hint="To pole nie jest obowiązkowe"
              ></v-text-field>
              <p>
                Trudonść:
              </p>
              <v-rating
              v-model="difficulty"
              background-color="green lighten-3"
              :length=10
              color="green"
              medium
              ></v-rating>
            </form>
          </v-card>

          <v-btn
            color="primary"
            @click="onAddName"
          >
            Dalej
          </v-btn>

          <v-btn flat @click="onCleanPlantData">Anuluj</v-btn>
        </v-stepper-content>

        <v-stepper-content step="2">
          <v-card
            class="mb-5"
            height="40vh"
          >
          <p>
            Nazwa polska: {{name}}
          </p>
          <p>
            Nazwa łacińska: {{latin}}
          </p>
          <form>
            <v-textarea
            v-model="description"
            box
            label="Opis"
            auto-grow
            ></v-textarea>
            <v-text-field
            v-model="source"
            label="Źródło"
            ></v-text-field>
          </form>
          </v-card>

          <v-btn
            color="primary"
            @click="onAddDescription"
          >
            Dalej
          </v-btn>

          <v-btn flat @click="onDeletePlant">Anuluj</v-btn>
        </v-stepper-content>

        <v-stepper-content step="3">
          <v-card
            class="mb-5"
            color="grey lighten-1"
            height="200px"
          >

          </v-card>

          <v-btn
            color="primary"
            @click="page = 1"
          >
            Continue
          </v-btn>

          <v-btn flat>Cancel</v-btn>
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
  </div>

</template>

<script>
import { required } from 'vuelidate/lib/validators'

export default {
  data() {
    return {
      page: 0,
      name: '',
      latin: '',
      difficulty: 1,
      description: '',
      source: ''
    }
  },
  validations: {
    name: { required }
  },
  methods: {
    onAddName() {
      const names = {
        name: this.name,
        latin: this.latin,
        difficulty: this.difficulty
      }
      if (!this.$v.$invalid) {
        this.$store.dispatch('plant/addName', names)
        .then(res => {
          if (res.status == 201) {
            this.page = 2
          }
        })
      }
    },
    onAddDescription() {
      if (this.description) {
        const description = {
          description: this.description,
          source: this.source
        }
        this.$store.dispatch('plant/addDesc', description)
        .then(res => {
          if (res.status == 201) {
            this.page = 3
          } else {
            this.page = 3
          }
        })
      }
    },
    onCleanPlantData() {
      this.$store.commit('plant/cleanPlantState')
      this.$router.push('/')
    },
    onDeletePlant() {
      this.$store.dispatch('plant/deletePlant')
      .then(res => {
        this.$router.push('/')
      })
    }
  },
  computed: {
    nameErrors() {
      const errors = []
      if (!this.$v.name.$dirty) return errors
      !this.$v.name.required && errors.push(
        'Nazwa jest wymagana'
      )
      return errors
    },
  }
}
</script>

<style lang="css">
</style>
