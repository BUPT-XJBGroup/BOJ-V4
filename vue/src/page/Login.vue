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
    var vm = this;
    this.axios.get("http://10.105.242.93:23333/accounts/login/").then(res => {
      console.log(res);
      var arr,
        reg = new RegExp("csrfmiddlewaretoken' value='(.*)'");
      if ((arr = res.data.match(reg))) {
        vm.csrfmiddlewaretoken = unescape(arr[1]);
        document.cookie = "csrftoken=" + escape(unescape(arr[1])) + ";";
      } else console.log("not found crsf value");
      console.log(vm.csrfmiddlewaretoken);
    });
  },
  data: () => ({
    csrfmiddlewaretoken: "",
    username: "",
    password: "",
    error: ""
  }),
  methods: {
    login() {
      if (this.check()) {
        var form =
          "csrfmiddlewaretoken=" +
          escape(this.csrfmiddlewaretoken) +
          "&username=" +
          escape(this.username) +
          "&password=" +
          escape(this.password);
        var vm = this;
        this.axios
          .post("http://10.105.242.93:23333/accounts/login/", form)
          .catch(res => {
            vm.error = res;
            return;
          });
        console.log("OK");
        this.showname();
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
    },
    showname() {
      var vm = this;
      this.axios
        .get("http://10.105.242.93:23333/rinne/SelfInfo")
        .then(res => {
          Store.dispatch("initState", res.data).then(() => {
            router.push("/");
          });
        })
        .catch(res => {
          vm.error = res;
        });
    }
  }
};
</script>
