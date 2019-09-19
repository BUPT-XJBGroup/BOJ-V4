<template>
  <v-flex>
    <v-progress-circular v-if="!done" indeterminate />
    <v-card style="margin-block-end: 2em;">
      <v-card-title class="headline">Details</v-card-title>
      <v-card-text>
        is_sticky:{{data.is_sticky}}
        <v-divider />
        update_time:{{data.update_time}}
        <v-divider />
        author:{{data.author}}
        <v-divider />
        last_update_user:{{data.last_update_user}}
        <v-divider />
        create_time:{{data.create_time}}
        <v-divider />
        pk:{{data.pk}}
      </v-card-text>
    </v-card>
    <v-card style="margin-block-end: 2em;">
      <v-card-title class="headline">{{data.title}}</v-card-title>
      <v-divider />
      <MdLoader v-if="done" :text="data.content" html></MdLoader>
    </v-card>
    <v-btn large color="primary" v-if="this.$store.getters.IsStaff" @click="edit">
      <v-icon left>mdi-book</v-icon>Edit
    </v-btn>
    <v-divider />
  </v-flex>
</template>

<script>
import MdLoader from "@/components/MdLoader";
import Router from "@/router";
export default {
  name: "Problem",
  components: {
    MdLoader
  },
  mounted() {
    this.axios.defaults.withCredentials = true;
    this.axios
      .get(
        "http://10.105.242.93:23333/rinne/GetAnnouncementDetails/?index=" +
          this.$route.params.id
      )
      .then(res => {
        this.data = res.data;
        this.done = true;
      })
      .catch(res => {
        Router.push({
          name: "Error",
          params: { text: res }
        });
      });
  },
  data() {
    return {
      done: false,
      data: {}
    };
  },
  methods: {
    edit() {}
  }
};
</script>