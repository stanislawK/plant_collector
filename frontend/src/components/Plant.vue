<template>
  <div id="plant">
    <v-layout>
     <v-flex xs12 sm6 offset-sm3>
       <v-card>
         <span v-if="plant_img">
           <v-img
             :src="plant_img"
             aspect-ratio="2.75"
           ></v-img>
           <p></p>
           <p></p>
         </span>
         <v-card-title primary-title>
           <div>
             <h3 class="headline mb-0">{{ name }}</h3>
             <p><em>{{ latin }}</em></p>
             <div v-for="desc in descriptions">
               {{ desc.content }}
               <span v-if="desc.source">
                 <a href="desc.source">Źródło</a>
               </span>
               <br />
             </div>
           </div>
         </v-card-title>

         <v-card-actions>
           <v-btn flat color="orange">Share</v-btn>
           <v-btn flat color="orange" @click="onGetPlant">Explore</v-btn>
         </v-card-actions>
       </v-card>
     </v-flex>
   </v-layout>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: '',
      latin: '',
      descriptions: '',
      plant_img: ''
    }
  },
  methods: {
    onGetPlant() {
      this.$store.dispatch('plant/getPlant', 1)
      .then(res => {
        this.onGetImage()
        this.name = res.data.name
        this.latin = res.data.latin
        this.descriptions = res.data.descriptions
      })
    },
    onGetImage() {
      this.$store.dispatch('plant/getImage', 1)
      .then(res => {
        const blob = new Blob([res.data], {type : 'image/jpg'})
        const fileReader = new FileReader()
        fileReader.addEventListener('load', () => {
          this.plant_img = fileReader.result
        })
        fileReader.readAsDataURL(blob)
      })
    }
  }
}
</script>

<style lang="css" scoped>
</style>
