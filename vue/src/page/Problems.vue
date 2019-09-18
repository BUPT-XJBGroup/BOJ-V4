<template>
  <v-sheet>
    <v-layout justify-center v-if="done">
      <v-progress-circular v-if="!done" indeterminate />
      <v-flex xs12 md10>
        <v-card v-for="i in articles" :key="i[0]" style="margin-block-end: 2em;">
          <v-card-text>
            <router-link
              :to="{ name: 'Problem' , params: {id: i[1] } }"
              style="font-size:x-large;"
            >uid={{i[0]}} name={{i[1]}}</router-link>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout justify-center v-if="done">
      <v-pagination v-model="page" :length="6"></v-pagination>
    </v-layout>
  </v-sheet>
</template>

<script>
export default {
  name: "Articles",
  mounted() {
    this.axios
      .get("http://10.105.242.93:23333/rinne/GetProblemList")
      .then(response => {
        this.articles = response.data.problem;
        this.done = true;
        console.log(response);
      });
  },
  data() {
    return {
      done: false,
      articles: [[]],
      page: 1
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