<template>
  <v-card>
    <v-layout class="curtain" align-center justify-center>
      <div class="text-xs-center">
        <v-img src="https://userpic.codeforces.com/418179/title/417a566cb97fc802.jpg" />
        <v-divider color="white" class="mt-4 mb-4" />
        <div class="headline">Welcome to</div>
        <div class="headline">Excited Online Judge</div>
        <div class="headline">欢迎使用Excited OJ。</div>
      </div>
    </v-layout>
    <div class="headline">Announcement</div>
    <v-divider />
    <v-progress-circular v-if="!done" indeterminate />
    <v-card v-for="i in data" :key="i.pk" class="mb-4">
      <router-link
        :to="{'name': 'Announcement', params: {'id': i.pk}}"
        :style="{cursor: 'pointer'}"
        tag="div"
      >
        <v-container>
          <v-flex>
            <v-layout>
              <v-card-text class="headline">{{i.title}}</v-card-text>
              <v-icon class="mdi-18px" v-if="i.is_sticky">vertical_align_top</v-icon>
            </v-layout>
          </v-flex>
          <v-divider />
          <v-card-text>{{i.brief}}</v-card-text>
          <v-divider />
          <v-card-text>
            <div>Author:{{i.author}}</div>
            <div>Update:{{i.update_time}}</div>
          </v-card-text>
        </v-container>
      </router-link>
    </v-card>
  </v-card>
</template>
<script>
export default {
  mounted() {
    this.axios.defaults.withCredentials = true;
    var vm = this;
    vm.axios
      .get("http://10.105.242.93:23333/rinne/GetAnnouncementList/")
      .then(r => {
        this.data = r.data.data;
        this.done = true;
        console.log(r);
      })
      .catch(function(error) {
        console.log(error);
      });
  },
  data() {
    return {
      done: false,
      data: []
    };
  }
};
</script>
<style scoped>
.curtain {
  opacity: 0.8;
  margin-top: 10px;
  margin-left: 10px;
  margin-right: 10px;
  height: 600px;
}
</style>