<template>
  <v-layout justify-center>
    <v-card flat>
      <v-container>
        <h1>Profile</h1>
        <v-divider/>
        <img v-bind:src="this.$store.getters.gravatar(256)" class="wpd_gravatar">
        <v-card-text>
          <tr>
            <td>username:</td>
            <td>{{this.$store.getters.username}}</td>
          </tr>
          <tr>
            <td>email:</td>
            <td>{{this.$store.getters.email}}</td>
          </tr>
          <tr>
            <td>token:</td>
            <td>{{this.$store.getters.token}}</td>
          </tr>
          <tr>
            <td>isLogin:</td>
            <td>{{this.$store.getters.isLogin}}</td>
          </tr>
          <tr>
            <td>IsStaff:</td>
            <td>{{this.$store.getters.IsStaff}}</td>
          </tr>
        </v-card-text>
        <v-btn large color="primary" @click="edit">
          <v-icon left>mdi-book</v-icon>Edit
        </v-btn>
      </v-container>
    </v-card>
  </v-layout>
</template>
<script>
import Router from "@/router";
export default {
  methods: {
    edit() {
      Router.push({ name: "UpdateInfo" });
    }
  }
};
</script>
