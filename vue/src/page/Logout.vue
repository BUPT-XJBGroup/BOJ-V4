<template>
  <v-layout />
</template>
<script>
import Store from "@/store.js";
import router from "@/router.js";
export default {
  mounted() {
    var d = new Date(0).toGMTString();
    window.document.cookie = "csrftoken=0;path=/;expires=" + d;
    Store.dispatch("logout").then(router.push("markdown"));
  }
};
</script>
