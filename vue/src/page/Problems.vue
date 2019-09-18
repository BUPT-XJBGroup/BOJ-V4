<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="desserts"
      :search="search"
      hide-actions
      :rows-per-page-items="text_per_page"
      :pagination.sync="pagination"
      class="elevation-1"
    >
      <template v-slot:items="props">
        <router-link
          :to="{'name': 'Problem', params: {'id': props.item.uid}}"
          :style="{cursor: 'pointer',background:props.item.solved?  'peachpuff;':'none'}"
          tag="tr"
        >
          <td>{{ props.item.uid }}</td>
          <td>{{props.item.name }}</td>
          <td>{{ props.item.time_limit }}</td>
          <td>{{ props.item.memory_limit }}</td>
          <td>{{ props.item.superadmin}}</td>
        </router-link>
      </template>
    </v-data-table>
    <div class="text-xs-center pt-2">
      <v-pagination v-model="pagination.page" :length="pages"></v-pagination>
    </div>
  </div>
</template>
<script>
export default {
  name: "Problems",
  mounted() {
    this.axios.defaults.withCredentials = true;
    var vm = this;
    vm.axios
      .get("http://10.105.242.93:23333/rinne/GetProblemList/")
      .then(response => {
        vm.desserts = response.data.problem;
        vm.pagination.totalItems = vm.desserts.length;
      })
      .catch(function(error) {
        console.log(error);
      });
  },
  data() {
    return {
      done: true,
      search: "",
      pagination: {},
      text_per_page: [12],
      headers: [
        { text: "UID", align: "left", sortable: false, value: "uid" },
        { text: "Name", sortable: false, value: "name" },
        { text: "Time Limit", sortable: false, value: "time_limit" },
        { text: "Memory Limit", sortable: false, value: "memory_limit" },
        { text: "Owner", sortable: false, value: "superadmin" }
      ],
      desserts: [{}]
    };
  },
  computed: {
    pages() {
      if (
        this.pagination.rowsPerPage == null ||
        this.pagination.totalItems == null
      )
        return 0;
      else
        return Math.ceil(
          this.pagination.totalItems / this.pagination.rowsPerPage
        );
    }
  },
  methods: {}
};
</script>