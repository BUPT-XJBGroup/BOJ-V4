<template>
  <v-layout>
    <v-progress-circular v-if="!done" indeterminate/>
    <v-layout justify-center v-if="done">
      <v-flex xs12 md10>
        <v-card v-for="i in articles" :key="i.title" style="margin-block-end: 2em;">
          <v-card-text>
            <router-link
              :to="{ name: 'Article' , params: {id: i.id } }"
              style="font-size:x-large;"
            >{{i.title}}</router-link>
          </v-card-text>
          <v-divider/>
          <v-card-text>Uid={{i.id}} Catalogue: {{i.cat}}</v-card-text>
          <v-card-text>Brief: {{i.brief}}</v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-layout>
</template>

<script>
export default {
  name: "Articles",
  mounted() {
    this.axios.get("http://localhost:8000/list").then(response => {
      this.articles = response.data;
      this.done = true;
    });
  },
  data() {
    return {
      done: false,
      articles: [
        {
          title: "",
          id: 0,
          category: "",
          publishe_at: "",
          intro: ""
        }
      ]
    };
  },
  components: {}
};
</script>
<style>
a {
  text-decoration: blink;
}

</style>