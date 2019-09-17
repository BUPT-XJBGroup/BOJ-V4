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
    <link rel="stylesheet" href="../fade/myblog.css">
    <ul class="cb-slideshow">
      <li>
        <span class="li_img1"></span>
      </li>
      <li>
        <span class="li_img2"></span>
      </li>
      <li>
        <span class="li_img3"></span>
      </li>
      <li>
        <span class="li_img4"></span>
      </li>
      <li>
        <span class="li_img5"></span>
      </li>
      <li>
        <span class="li_img6"></span>
      </li>
    </ul>
  </div>
</template>

<script>
import "@/fade/jquery.min.js";
import "@/fade/fade.js";
import NBar from "@/components/NBar";
export default {
  name: "App",
  components: {
    NBar
  }
};
</script>
<style>
@import "/fade/myblog.css";
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
