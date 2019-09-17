import Vue from 'vue'
import md5 from 'js-md5'
import Vuex from 'vuex'
Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    username: sessionStorage.getItem("username") ? sessionStorage.getItem("username") : "Anonymous",
    isLogin: sessionStorage.getItem("isLogin") == "true" ? true : false,
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
        state.email = "";
        state.IsStaff = false;
        sessionStorage.setItem("isLogin", "false");
        sessionStorage.setItem("username", "");
        sessionStorage.setItem("email", "");
        sessionStorage.setItem("IsStaff", "false");
      }
    },
    userEmail(state, Url) {
      state.email = Url ? Url : "";
    },
    userIsStaff(state, IsStaff) {
      state.IsStaff = IsStaff == true ? true : false;
    }
  },
  actions: {
    setUser({ commit }, username) {
      commit("userStatus", username);
    },
    setEmail({ commit }, email) {
      commit("userEmail", email);
    },
    setStaff({ commit }, IsStaff) {
      commit("userIsStaff", IsStaff);
    },
    initState({ commit }, name,email,staff) {
      commit("userStatus", name);
      commit("userEmail", email);
      commit("userIsStaff", staff);
      sessionStorage.setItem("isLogin", "true");
      sessionStorage.setItem("username", name);
      sessionStorage.setItem("email", email);
      sessionStorage.setItem("IsStaff", staff?"true":"false");
    },
    logout({ commit }) {
      commit("userStatus", "");
    }
  }
})

export default store
