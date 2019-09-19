<template>
  <v-layout justify-center>
    <v-flex xs12 md6>
      <v-card>
        <v-container>
          <div align="center" justify="center">
            <v-flex xs12>
              <img v-bind:src="this.$store.getters.gravatar(256)" class="wpd_gravatar" />
            </v-flex>
            <v-divider />
          </div>
          <v-text-field v-model="username" label="Username" outline />
          <v-text-field v-model="password" label="Password" type="password" outline />
          <v-text-field v-model="password2" label="Repeat Password" type="password" outline />
          <v-text-field v-model="nickname" label="Nickname" outline />
          <v-text-field v-model="email" label="Email" outline />
          <div>
            <v-select
              v-model="gender"
              :items="genderList"
              persistent-hint
              return-object
              outline
              label="Gender"
            />
          </div>
          <v-alert :value="true" class="mb-3" type="info" outline>
            <span>Your Avatar is Bind With Your Email In</span>
            <a href="https://cn.gravatar.com/">
              <strong>
                <span>Gravatar</span>
              </strong>
            </a>
          </v-alert>
          <v-btn block @click="submit">Submit</v-btn>
          <v-card-text style="color:red;">{{error}}</v-card-text>
        </v-container>
      </v-card>
    </v-flex>
  </v-layout>
</template>
<script>
import router from "@/router.js";
import Store from "@/store.js";
export default {
  data: () => ({
    username: "",
    password: "",
    password2: "",
    email: "",
    error: "",
    nickname: "",
    genderList: ["Male", "Female", "Secret"],
    gender: ""
  }),
  methods: {
    submit() {
      if (this.check()) {
        if (this.$store.getters.Token == "") {
          this.axios
            .get("http://10.105.242.93:23333/rinne/GetCSRF/")
            .then(res => {
              Store.dispatch("setToken", res.data.CSRFToken);
              this.send();
            });
        } else {
          this.send();
        }
      }
    },
    send() {
      var form =
        "csrfmiddlewaretoken=" +
        escape(this.$store.getters.Token) +
        "&username=" +
        escape(this.username) +
        "&password=" +
        escape(this.password) +
        "&email=" +
        escape(this.email) +
        "&nickname=" +
        escape(this.nickname) +
        "&gender=" +
        escape(this.gender);
      console.log(form);
      this.axios
        .post("http://10.105.242.93:23333/rinne/Register/", form)
        .then(res => {
          if (res.data.status == "OK") {
            router.push({
              name: "Login",
              params: { text: "Register succeed,Please Login First" }
            });
          } else {
            this.error = res.data.status;
          }
        });
    },
    check() {
      if (this.username == "") {
        this.error = "Username cannot be Empty";
        return false;
      } else if (this.password == "") {
        this.error = "Password cannot be Empty";
        return false;
      } else if (this.password2 == "") {
        this.error = "Repeat your Password";
        return false;
      } else if (this.email == "") {
        this.error = "Email cannot be Empty";
        return false;
      } else if (this.password.length < 6) {
        this.error = "Password should at least 6 characters";
        return false;
      } else if (!this.CheckEmail()) {
        this.error = "Email is not valid";
        return false;
      } else if (this.password != this.password2) {
        this.error = "Confirmation mismatched";
        return false;
      } else if (this.gender == "") {
        this.error = "Gender is Empty";
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
