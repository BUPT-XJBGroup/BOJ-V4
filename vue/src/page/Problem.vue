<template>
  <v-layout>
    <v-flex>
      <v-progress-circular v-if="!done" indeterminate />
      <v-card>
        <v-card-title class="headline">Details</v-card-title>
        <v-card-text>
          id:{{data.id}}
          <v-divider />
          time_limit:{{data.time_limit}}
          <v-divider />
          memory_limit:{{data.memory_limit}}
          <v-divider />
          code_length_limit:{{data.code_length_limit}}
          <v-divider />
          is_checked:{{data.is_checked}}
          <v-divider />
          is_spj:{{data.is_spj}}
          <v-divider />
          superadmin:{{data.superadmin}}
        </v-card-text>
      </v-card>
      <v-card>
        <v-card-title class="headline">Description</v-card-title>
        <MdLoader v-if="done" :text="desc.desc" html></MdLoader>
        <v-card-title class="headline">Sample Input</v-card-title>
        <MdLoader v-if="done" :text="desc.sample_in" html></MdLoader>
        <v-card-title class="headline">Sample Output</v-card-title>
        <MdLoader v-if="done" :text="desc.sample_out" html></MdLoader>
      </v-card>
      <v-btn large color="primary" v-if="this.$store.getters.IsStaff" @click="edit">
        <v-icon left>mdi-book</v-icon>Edit
      </v-btn>
      <v-divider />
    </v-flex>
  </v-layout>
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
        "http://10.105.242.93:23333/rinne/GetProblemDetails/?index=" +
          this.$route.params.id
      )
      .then(res => {
        this.data = res.data;
        this.desc = JSON.parse(this.data.desc);
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
      data: {},
      desc: {}
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