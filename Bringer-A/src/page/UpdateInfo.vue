<template>
  <v-layout justify-center>
    <v-flex xs12 md6>
      <v-card>
        <v-container>
          <v-text-field v-model="username" disabled label="Username" outline/>
          <v-text-field v-model="password0" label="Old Password" hint="This Field must be Filled" type="password" outline/>
          <v-text-field v-model="password1" label="New Password" hint="Leave Blank if donnot Want to Change" type="password" outline/>
          <v-text-field v-model="password2" label="Repeat Password" hint="Repeat Your new Password" type="password" outline/>
          <v-text-field v-model="email" label="Email" hint="Input your new Email" outline/>
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
    username: Store.getters.username,
    password0: "",
    password1: "",
    password2: "",
    email:Store.getters.email,
    error: ""
  }),
  methods: {
    submit() {
      if (this.check()) {
        this.axios
          .post(
            "http://localhost:8000/updateuser",
            JSON.stringify({
              username: this.username,
              password: this.password0,
              newpassword: this.password1==""?this.password0:this.password1,
              email: this.email
            })
          )
          .then(res => {
            if (res.data == "Done") {
              router.push("logout");
            } else {
              this.error = res.data;
            }
          });
      }
    },
    check() {
      if (this.password0 == "") {
        this.error = "Old password cannot be empty";
        return false;
      } else if (this.password1 != this.password2) {
        this.error = "Confirmation mismatched";
        return false;
      } else if (this.email == "") {
        this.error = "email cannot be empty";
        return false;
      } else if (this.username.password1 < 6) {
        this.error = "new password should at least 6 characters";
        return false;
      } else if (!this.CheckEmail()) {
        this.error = "email is not valid";
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
