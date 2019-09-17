<template>
  <v-container>
    <v-layout justify-center row wrap>
      <v-flex xs12 sm10 md8 lg6 xl4>
        <v-card>
          <v-toolbar light>
            <v-tabs v-model="tabs" centered>
              <v-tab v-for="n in 3" :key="n">{{TabList[n]}}</v-tab>
            </v-tabs>
          </v-toolbar>

          <v-tabs-items v-model="tabs">
            <v-tab-item>
              <v-card-text>
                <div align="center" justify="center">
                  <v-flex xs12>
                    <img v-bind:src="this.$store.getters.gravatar(256)" class="wpd_gravatar" />
                  </v-flex>
                  <v-divider />
                </div>

                <v-form @submit.prevent="submit">
                  <div>
                    <v-select
                      v-model="gender"
                      :items="genderList"
                      prepend-icon="mdi-account-multiple-outline"
                      class="mt-1"
                      persistent-hint
                      return-object
                      single-line
                    />
                  </div>
                  <v-text-field
                    v-model="username"
                    label="Username"
                    disabled
                    prepend-icon="mdi-iframe"
                  />
                  <v-text-field
                    v-model="nickname"
                    label="Nickname"
                    prepend-icon="mdi-iframe-outline"
                  />

                  <v-text-field v-model="email" label="Email" prepend-icon="mdi-book" />
                  <v-text-field
                    v-model="isstaff"
                    label="IsStaff"
                    disabled
                    prepend-icon="mdi-emoticon-cool"
                  />
                  <v-text-field
                    v-model="isteacher"
                    label="IsTeacher"
                    disabled
                    prepend-icon="mdi-emoticon-cool"
                  />
                  <v-alert :value="true" class="mb-3" type="info" outline>
                    <span>You can change your Avatar In</span>
                    <a href="https://cn.gravatar.com/">
                      <strong>
                        <span>Gravatar</span>
                      </strong>
                    </a>
                    <span>With Your Email</span>
                  </v-alert>
                  <v-btn block type="submit">Submit</v-btn>
                </v-form>
              </v-card-text>
            </v-tab-item>

            <v-tab-item>
              <v-card flat>
                <v-card-text>
                  <v-text-field
                    v-model="password0"
                    label="Old Password"
                    hint="This Field must be Filled"
                    type="password"
                    outline
                  />
                  <v-text-field
                    v-model="password1"
                    label="New Password"
                    hint="Leave Blank if donnot Want to Change"
                    type="password"
                    outline
                  />
                  <v-text-field
                    v-model="password2"
                    label="Repeat Password"
                    hint="Repeat Your new Password"
                    type="password"
                    outline
                  />
                  <v-btn block type="submit">Submit</v-btn>
                </v-card-text>
              </v-card>
            </v-tab-item>
            <v-tab-item>
              <v-card flat v-if="this.isstaff">
                <v-sheet class="pa-5">
                  <v-switch v-model="SetTeacher" inset :label="`Is Teacher`"></v-switch>
                  <v-switch v-model="SetStaff" inset :label="`Is Staff`"></v-switch>
                  <v-switch v-model="SetActive" inset :label="`Is Active`"></v-switch>
                  <v-btn block type="submit">Submit</v-btn>
                </v-sheet>
              </v-card>
              <v-card flat v-if="!this.isstaff">
                <v-card-text>
                  <v-card-title class="headline">You Cannot See This Page</v-card-title>
                </v-card-text>
              </v-card>
            </v-tab-item>
          </v-tabs-items>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>


<script>
import Router from "@/router";
export default {
  methods: {
    edit() {
      Router.push({ name: "UpdateInfo" });
    }
  },
  mounted() {
    this.username = this.$store.getters.username;
    this.nickname = this.$store.getters.nickname;
    this.gender = this.$store.getters.gender;
    this.email = this.$store.getters.email;
    this.isstaff = this.$store.getters.IsStaff;
    this.isteacher = this.$store.getters.IsTeacher;
    this.SetTeacher = this.isteacher;
    this.SetStaff = this.isstaff;
    this.SetActive = true;
  },
  data: () => ({
    tabs: null,
    TabList: ["", "Setting", "Password", "Manage"],
    username: "",
    nickname: "",
    gender: "",
    email: "",
    isteacher: false,
    isstaff: false,
    SetTeacher: false,
    SetStaff: false,
    SetActive: false,
    genderList: ["Male", "Female", "Secret"],
    password0: "",
    password1: "",
    password2: ""
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
              newpassword:
                this.password1 == "" ? this.password0 : this.password1,
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
