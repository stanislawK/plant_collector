<template>
  <div>
    <v-app>
      <v-layout justify-center>
        <v-flex xs12 sm6 text-xs-center>
          <v-btn
          color="info"
          to="/login"
          >
            Zaloguj
          </v-btn>
          <v-btn
          color="success"
          to="/register"
          >
            Zarejestuj
          </v-btn>
        </v-flex>
      </v-layout>
    </v-app>
  </div>
</template>

<script>
export default {


}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
