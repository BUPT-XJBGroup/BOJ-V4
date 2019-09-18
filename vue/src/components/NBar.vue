<template>
  <v-navigation-drawer :width="width" style=" background: rgba(255, 255, 255, 0.9);" enable-resize-watcher app>
    <v-toolbar flat class="primary lighten-3">
      <v-list class="pa-0">
        <v-list-tile avatar>
          <v-list-tile-avatar>
            <img v-bind:src=this.$store.getters.gravatar(512)
              @click.stop="enlarge"
            >
          </v-list-tile-avatar>

          <v-list-tile-content>
            <v-list-tile-title>{{this.$store.getters.username}}</v-list-tile-title>
          </v-list-tile-content>

          <v-list-tile-action>
            <v-btn icon flat @click.stop="decay">
              <v-icon>mdi-windows</v-icon>
            </v-btn>
          </v-list-tile-action>
        </v-list-tile>
      </v-list>
    </v-toolbar>

    <v-list>
      <v-list-tile v-for="i in Active" :key="i.text" :to="i.router">
        <v-layout>
          <v-list-tile-action>
            <v-icon>{{i.image}}</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>{{i.text}}</v-list-tile-title>
          </v-list-tile-content>
        </v-layout>
      </v-list-tile>
    </v-list>
  </v-navigation-drawer>
</template>




<script>
import Store from "@/store.js";
export default {
  data() {
    return {
      width: 250,
      contents: [
        {
          text: "Login",
          image: "mdi-rocket",
          router: "/login",
        },
        {
          text: "Logout",
          image: "mdi-home",
          router: "/logout",
        },
        {
          text: "Markdown",
          image: "mdi-spa",
          router: "/markdown",
        },
        {
          text: "Setting",
          image: "mdi-delta",
          router: "/setting",
        },
        {
          text: "Problem",
          image: "mdi-coffin",
          router: "/problems",
        },
        {
          text: "About",
          image: "mdi-alpha",
          router: "/about",
        },
        {
          text: "Add",
          image: "mdi-beta",
          router: "/add",
        }
      ]
    };
  },
  methods: {
    enlarge() {
      this.width = 250;
    },
    decay() {
      this.width = 70;
    }
  },
  computed: {
    Active: function() {
      return this.contents.filter(function(x) {
        return !(x.text=="Login"&&Store.getters.isLogin)&&!(x.text=="Logout"&&!Store.getters.isLogin)&&!(x.text=="Setting"&&!Store.getters.isLogin)&&!(x.text=="Add"&&!Store.getters.IsStaff);
      });
    }
  }
};
</script>
<style>
html,
*,
:after,
:before {
  box-sizing: border-box;
}
button {
  border-style: none;
}
* {
  font-family: "Fira Code", "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
