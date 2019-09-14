<template>
  <v-layout justify-center>
    <v-flex xs12 md6>
      <v-card>
        <v-container>
          <v-text-field v-model="username" label="Username" outline/>
          <v-text-field v-model="password" label="Password" type="password" outline/>
          <v-text-field v-model="password2" label="Repeat Password" type="password" outline/>
          <v-text-field v-model="email" label="Email" outline/>
          <v-btn block @click="submit">Submit</v-btn>
          <v-card-text style="color:red;">{{error}}</v-card-text>
        </v-container>
      </v-card>
    </v-flex>
  </v-layout>
</template>
<script>
import router from "@/router.js";
export default {
  data: () => ({
    username: "",
    password: "",
    password2: "",
    email: "",
    error: ""
  }),
  methods: {
    submit() {
      if (this.check()) {
        this.axios
          .post(
            "http://localhost:8000/adduser",
            JSON.stringify({
              username: this.username,
              password: this.password,
              email: this.email
            })
          )
          .then(res => {
            if (res.data == "Done") {
              router.push("login");
            } else {
              this.error = res.data;
            }
          });
      }
    },
    check() {
      if (this.username == "") {
        this.error = "username cannot be empty";
        return false;
      } else if (this.password == "") {
        this.error = "password cannot be empty";
        return false;
      } else if (this.password2 == "") {
        this.error = "repeat your password";
        return false;
      } else if (this.email == "") {
        this.error = "email cannot be empty";
        return false;
      } else if (this.username.password < 6) {
        this.error = "password should at least 6 characters";
        return false;
      } else if (!this.CheckEmail()) {
        this.error = "email is not valid";
        return false;
      } else if (this.password != this.password2) {
        this.error = "Confirmation mismatched";
        return false;
      } else {
        return true;
      }
    },
    CheckEmail() {
      var reg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
      return reg.test(this.email);
    }
  }
};
</script>
