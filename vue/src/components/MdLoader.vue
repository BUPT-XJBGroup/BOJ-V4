<template>
  <v-card-text>
    <v-flex v-html="renderContent"></v-flex>
  </v-card-text>
</template>
<script>
import { DisableHtml, EnableHtml } from "@/katex";
export default {
  props: {
    text: {
      type: String,
      default: ""
    },
    html: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    renderContent() {
      return this.html
        ? EnableHtml.render(this.text)
        : DisableHtml.render(this.text);
    }
  }
};
</script>
<style>
@import "highlight.js/styles/vs2015.css";
code {
  font-family: "Fira Code", "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  line-height: 23px;
  font-size: 15px;
}
pre {
  width: 65em;
}
</style>
