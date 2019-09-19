 <template>
  <v-layout justify-center>
    <v-flex xs12 md6>
      <v-card>
        <v-container>
          <v-text-field v-model="username" label="Username" prepend-icon="mdi-account" />
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
        var vm = this;
        this.axios.defaults.withCredentials = true;
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
        escape(this.password);
      console.log(form);
      console.log(this.$store.getters.Token);
      this.axios
        .post("http://10.105.242.93:23333/rinne/Login/", form)
        .then(res => {
          console.log(res);
          if (res.data.status == "OK") {
            Store.dispatch("initState", res.data.data).then(() => {
              router.push("/");
            });
          } else {
            this.error = "Login Faied";
          }
        });
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
