import Vue from 'vue'
import md5 from 'js-md5'
import Vuex from 'vuex'
Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    username: sessionStorage.getItem("username") ? sessionStorage.getItem("username") : "Anonymous",
    isLogin: sessionStorage.getItem("isLogin") == "true" ? true : false,
    token: sessionStorage.getItem("token") ? sessionStorage.getItem("token") : "",
    email: sessionStorage.getItem("email") ? sessionStorage.getItem("email") : "",
    IsStaff: sessionStorage.getItem("IsStaff") == "true" ? true : false,
  },
  getters: {
    username: function (state) {
      return state.username;
    },
    email: function (state) {
      return state.email;
    },
    token: function (state) {
      return state.token;
    },
    isLogin: function (state) {
      return state.isLogin;
    },
    gravatar: (state) => (size) => {
      return 'https://secure.gravatar.com/avatar/' + md5(state.email.toLowerCase()) + "?s=" + size;
    },
    IsStaff: function (state) {
      return state.IsStaff;
    },
  },
  mutations: {
    userStatus(state, user) {
      if (user) {
        state.username = user;
        state.isLogin = true
      } else if (user == "") {
        state.username = "Anonymous";
        state.isLogin = false;
        state.token = "";
        state.email = "";
        state.IsStaff = false;
        sessionStorage.setItem("token", "");
        sessionStorage.setItem("isLogin", "false");
        sessionStorage.setItem("username", "");
        sessionStorage.setItem("email", "");
        sessionStorage.setItem("IsStaff", "false");
      }
    },
    userEmail(state, Url) {
      state.email = Url ? Url : "";
    },
    userToken(state, userToken) {
      state.token = userToken ? userToken : "";
    },
    userIsStaff(state, IsStaff) {
      state.IsStaff = IsStaff == true ? true : false;
    }
  },
  actions: {
    setToken({ commit }, token) {
      commit("userToken", token);
    },
    setUser({ commit }, username) {
      commit("userStatus", username);
    },
    setEmail({ commit }, email) {
      commit("userEmail", email);
    },
    setStaff({ commit }, IsStaff) {
      commit("userIsStaff", IsStaff);
    },
    initState({ commit }, data) {
      commit("userToken", data.token);
      commit("userStatus", data.username);
      commit("userEmail", data.email);
      commit("userIsStaff", data.IsStaff);
      sessionStorage.setItem("token", data.token);
      sessionStorage.setItem("isLogin", "true");
      sessionStorage.setItem("username", data.username);
      sessionStorage.setItem("email", data.email);
      sessionStorage.setItem("IsStaff", data.IsStaff?"true":"false");
    },
    logout({ commit }) {
      commit("userStatus", "");
    }
  }
})

export default store
