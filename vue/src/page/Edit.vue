<template>
  <v-card>
    <v-form>
      <v-container>
        <v-layout row wrap>
          <v-flex xs12>
            <v-text-field v-model="title" clearable label="Title" type="text"/>
            <v-text-field v-model="cat" clearable label="Catalogue" type="text"/>
            <v-text-field v-model="brief" clearable label="Brief" type="text"/>
            <v-textarea
              v-model="content"
              v-if="!preview"
              auto-grow
              clearable
              rows="10"
              label="Content"
            />
            <MdLoader v-if="preview" :text="content"></MdLoader>
            <v-toolbar height="48" flat>
              <v-switch v-model="preview" :label="`Preview: ${preview.toString()}`"></v-switch>
              <v-btn large color="primary" @click="submit">
                <v-icon left>mdi-target</v-icon>Submit
              </v-btn>
            </v-toolbar>
            <h2 style="color:red;">
              {{message}}
              <v-fade-transition>
                <v-progress-circular v-if="loading" size="24" color="info" indeterminate></v-progress-circular>
              </v-fade-transition>
            </h2>
          </v-flex>
        </v-layout>
      </v-container>
    </v-form>
  </v-card>
</template>
<script>
import MdLoader from "@/components/MdLoader";
export default {
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
        this.title = res.data.title;
        this.cat = res.data.cat;
        this.content = res.data.content;
        this.brief = res.data.brief;
      });
  },
  data: () => ({
    title: "",
    cat: "",
    content: "",
    brief: "",
    message: "",
    loading: false,
    preview: false
  }),
  methods: {
    submit() {
      if (this.check()) {
        this.loading = true;
        this.message = "Waiting for it...";
        this.axios
          .post(
            "http://localhost:8000/updateitem",
            JSON.stringify({
              token: this.$store.getters.token,
              id: this.$route.params.id,
              title: this.title,
              cat: this.cat,
              brief: this.brief,
              content: this.content
            })
          )
          .then(res => {
            this.loading = false;
            this.message = res.data;
          });
      }
    },
    check() {
      if (this.title == "") {
        this.message = "Title cannot be empty";
        return false;
      } else if (this.cat == "") {
        this.message = "Catalogue cannot be empty";
        return false;
      } else if (this.brief == "") {
        this.message = "Brief cannot be empty";
        return false;
      } else if (this.content == "") {
        this.message = "Content cannot be empty";
        return false;
      } else {
        return true;
      }
    }
  }
};
</script>
<style>
</style>
