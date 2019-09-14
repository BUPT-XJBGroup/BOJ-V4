 <template>
  <v-layout justify-center>
    <v-flex xs12 md6>
      <v-card>
        <v-container>
          <v-text-field v-model="username" label="Username" prepend-icon="mdi-account"/>
          <v-text-field
            v-model="password"
            label="Password"
            type="password"
            prepend-icon="mdi-lock"
          />
          <v-layout row wrap>
            <v-card-text>
              <router-link :to="{ name: 'Register' }">Register</router-link>
            </v-card-text>
            <v-card-text style="color:red;">{{error}}</v-card-text>
          </v-layout>
          <v-btn block @click="login">Login</v-btn>
        </v-container>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import Store from "@/store.js";
import router from "@/router.js";
export default {
  mounted() {
    try {
      this.error = this.$route.params.text;
    } catch (e) {
      this.error = "";
    }
  },
  data: () => ({
    username: "",
    password: "",
    error: ""
  }),
  methods: {
    login() {
      if (this.check()) {
        this.axios
          .post(
            "http://localhost:8000/login",
            JSON.stringify({
              username: this.username,
              password: this.password
            })
          )
          .then(res => {
            if (res.data != "Failed") {
              Store.dispatch("initState", res.data)
                .then(() => {
                  router.push("markdown");
                })
                .catch(error => {
                  this.error = "Login Failed";
                });
            } else {
              this.error = "Wrong Username or Password";
            }
          });
      }
    },
    check() {
      if (this.username == "") {
        this.error = "Username cannot be empty";
        return false;
      } else if (this.password == "") {
        this.error = "Password cannot be empty";
        return false;
      } else {
        return true;
      }
    }
  }
};
</script>
