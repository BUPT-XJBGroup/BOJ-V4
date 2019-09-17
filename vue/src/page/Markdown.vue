<template>
  <v-card>
    <v-container>
      <MdLoader :text="require('@/assets/test.md')" html></MdLoader>
    </v-container>
  </v-card>
</template>

<script>
import MdLoader from "@/components/MdLoader";

export default {
  components: {
    MdLoader
  }
};
</script>
<style>

</style>
