<template>
  <v-layout/>
</template>
<script>
import Store from "@/store.js";
import router from "@/router.js";
export default {
  mounted() {
    Store.dispatch("logout").then(router.push("markdown"));
  }
};
</script>
