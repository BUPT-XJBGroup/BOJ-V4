<template>
  <div id="app">
    <v-app>
      <NBar/>
      <v-content>
        <keep-alive>
          <v-container>
            <router-view/>
          </v-container>
        </keep-alive>
      </v-content>
    </v-app>
  </div>
</template>

<script>
import NBar from "@/components/NBar";
export default {
  name: "App",
  components: {
    NBar
  }
};
</script>
<style>
.theme--light.v-sheet {
  background: rgba(255, 255, 255, 0.85)!important;
}
.theme--light.v-card {
  background: rgba(255, 255, 255, 0.85)!important;
}
.theme--light.application {
  background: rgba(255, 255, 255, 0)!important;
}
</style>
