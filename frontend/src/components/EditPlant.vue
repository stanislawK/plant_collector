<template lang="html">
  <div id="plant">
    <v-layout justify-center>
     <v-flex xs12 sm8 md6 text-xs-center>
       <v-card>
         <span v-if="plant_img">
           <v-img
             :src="plant_img"
             height="300"
             contain
           ></v-img>
           <p></p>
           <p></p>
         </span>
         <v-card-title primary-title>
           <div>
             <form>
               <v-text-field
               v-model="name"
               label="Nazwa polska"
               required
               @input="$v.name.$touch()"
               @blur="$v.name.$touch()"
               ></v-text-field>
               <v-text-field
               v-model="latin"
               label="Nazwa Łacińska"
               hint="To pole nie jest obowiązkowe"
               ></v-text-field><br />
               <span class="grey--text">Trudność</span>
               <v-rating
               v-model="difficulty"
               background-color="green lighten-3"
               :length=10
               color="green"
               medium
               ></v-rating>
             </form>
             <div v-for="desc in descriptions">
               <form>
                 <v-textarea
                 v-model="desc.content"
                 hint="Opis rośliny"
                 label="Opis"
                 auto-grow
                 ></v-textarea>
                 <v-text-field
                 v-model="desc.source"
                 label="Źródło"
                 hint="Link do strony z której pochodzi opis"
                 ></v-text-field>
               </form>
               <br />
             </div>
           </div>
         </v-card-title>

         <v-card-actions>
           <v-btn flat color="orange" @click="onEditPlant">Edytuj</v-btn>
           <v-btn flat color="orange" @click="onGetPlant">Explore</v-btn>
         </v-card-actions>
       </v-card>
     </v-flex>
   </v-layout>
  </div>
</template>

<script>
import { required } from 'vuelidate/lib/validators'

export default {
  data() {
    return {
      name: '',
      latin: '',
      descriptions: '',
      plant_img: '',
      difficulty: 0,
      plant_id: this.$route.params.plant_id,
    }
  },
  validations: {
    name: { required }
  },
  methods: {
    onGetPlant() {
      this.$store.dispatch('plant/getPlant', this.plant_id)
      .then(res => {
        this.onGetImage()
        this.name = res.data.name
        this.latin = res.data.latin
        this.descriptions = res.data.descriptions
        this.difficulty = res.data.difficulty
      })
    },
    onGetImage() {
      this.$store.dispatch('plant/getImage', this.plant_id)
      .then(res => {
        const blob = new Blob([res.data], {type : 'image/jpg'})
        const fileReader = new FileReader()
        fileReader.addEventListener('load', () => {
          this.plant_img = fileReader.result
        })
        fileReader.readAsDataURL(blob)
      })
    },
    onEditPlant() {
      const nameData = {
        name: this.name,
        latin: this.latin,
        difficulty: this.difficulty
      }
      this.$store.dispatch('plant/editName', [nameData, this.plant_id])
      .then( res => {
        console.log(res.data)
      }, error => {
        console.log(error)
      })
      for (let desc of this.descriptions) {
        console.log(desc)
        const descData = {
          description: desc.content,
          source: desc.source
        }
        this.$store.dispatch(
          'plant/editDesc', [descData, this.plant_id, desc.id]
        )
        .then( res => {
          console.log(res.data)
        }, error => {
          console.log(error.response)
        })
      }
    }
  }
}
</script>

<style lang="css" scoped>
</style>
