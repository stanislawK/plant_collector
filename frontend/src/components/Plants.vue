<template>
  <div id="plants">
      <v-container
        fluid
        grid-list-md
        grey
        lighten-4
      >
        <v-layout row wrap>
          <v-flex
            v-for="plant in plants"
            :key="plant.id"
            xs12
            sm6
            md4
            text-xs-center
          >
            <v-card @click="dialog=true; selectedPlant=plant.id">
              <v-img
                :src="plant.img"
                height="300px"
                contain
              >
              </v-img>
              <v-card-actions class="white justify-center">
                <v-subheader>
                  {{plant.name}}{{' '}}
                  <em> {{plant.latin}}</em>
                </v-subheader>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
         <v-dialog
         v-model="dialog"
         width="600"
         >
          <app-plant :plant_id="selectedPlant"></app-plant>
        </v-dialog>
  </div>
</template>

<script>
import Plant from './Plant.vue'
export default {
  components: {
    'app-plant': Plant
  },
  data () {
    return {
      plants: [],
      dialog: false,
      selectedPlant: ''
    }
  },
  created() {
    this.$store.dispatch('plant/getPlants')
    .then(res => {
      const plants = res.data.plants
      for (let plant of plants) { plant.img = '' }
      this.plants = plants
      this.onGetImages()
    }, err => {
      console.log(err.response.data)
    })
  },
  methods: {
    onGetImages() {
      for (let plant of this.plants) {
        if (plant.images.length) {
          this.$store.dispatch('plant/getImage', plant.id)
          .then(res => {
            const blob = new Blob([res.data], {type : 'image/jpg'})
            const fileReader = new FileReader()
            fileReader.addEventListener('load', () => {
              plant.img = fileReader.result
            })
            fileReader.readAsDataURL(blob)
          })
          .catch(err => {
            if (err.response.status == 404) {
              plant.img = ''
            }
          })
        }
      }
    }
  }
}
</script>

<style lang="css" scoped>
  #plants {
    white-space: pre;
  }
</style>
