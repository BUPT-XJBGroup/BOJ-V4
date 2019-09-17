<template>
  <v-layout>
    <v-flex>
      <v-card>
        <v-progress-circular v-if="!done" indeterminate/>
        <v-card-text>
          <h2>Title: {{data.title}}</h2>
          <h2>Uid: {{data.id}}</h2>
          <h2>Catalogue: {{data.cat}}</h2>
          <h2>Brief: {{data.brief}}</h2>
          <v-btn large color="primary" v-if="this.$store.getters.IsStaff" @click="edit">
            <v-icon left>mdi-book</v-icon>Edit
          </v-btn>
        </v-card-text>
        <v-divider/>
        <v-card-text>
          <MdLoader v-if="done" :text="data.content.toString()" html></MdLoader>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import MdLoader from "@/components/MdLoader";
import Router from "@/router";
export default {
  name: "Article",
  components: {
    MdLoader
  },
  mounted() {
    this.axios
      .post(
        "http://localhost:8000/article",
        JSON.stringify({
          id: this.$route.params.id
        })
      )
      .then(res => {
        this.data = res.data;
        this.done = true;
      });
  },
  data() {
    return {
      done: false,
      data: {}
    };
  },
  methods: {
    edit() {
      Router.push({
        name: "Edit",
        params: { id: this.data.id }
      });
    }
  }
};
</script>