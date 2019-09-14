<template>
  <div>
    <v-card style="margin-block-end: 2em;">
      <v-card-text>
        <h2>About Me</h2>
      </v-card-text>
      <v-divider/>
      <v-layout column>
        <v-container>
          <v-flex xs12 sm6>
            <v-slider v-model="slider" :min="100" :max="512" label="Size"></v-slider>
          </v-flex>
          <v-flex xs12 sm6 align-center layout text-xs-center>
            <v-avatar :size="avatarSize" color="grey lighten-4">
              <img
                src="https://secure.gravatar.com/avatar/6160fc0a17c153c47aaf52fde6236368?s=512"
                alt="avatar"
              >
            </v-avatar>
          </v-flex>
        </v-container>
        <v-flex sm12>
          <v-card-text>
            <h3>9646516</h3>
            <h3>
              <a
                href="https://www.bupt.edu.cn/"
                style="text-decoration: blink;color:#00A1F1;"
              >Beijing University of Posts and Telecommunications</a>
            </h3>
            <h3>
              <b style="color:black;">Codeforces:</b>
              <a
                href="https://codeforces.com/profile/9646516"
                style="color:#AA00AA;text-decoration: blink;"
              >9646516</a>
            </h3>
            <h3>
              <b style="color:black;">Tieba:</b>
              <a
                href="http://tieba.baidu.com/home/main?un=9646516"
                style="color:#3385FF;text-decoration: blink;"
              >9646516</a>
            </h3>
            <h3>
              <b style="color:black;">Zhihu:</b>
              <a
                href="https://www.zhihu.com/people/9646516-92/activities"
                style="color:#399FFF;text-decoration: blink;"
              >9646516</a>
            </h3>
            <h3>
              <b style="color:black;">Github:</b>
              <a
                href="https://github.com/9646516"
                style="color:#24292E;text-decoration: blink;"
              >9646516</a>
            </h3>
            <h3>
              <b style="color:black;">Contact:</b>
              <a
                href="mailto:zyq855@gmail.com"
                style="color:#80407B;text-decoration: blink;"
              >zyq855#gmail.com</a>
            </h3>
          </v-card-text>
        </v-flex>
      </v-layout>
    </v-card>
    <v-card style="margin-block-end: 2em;">
      <v-card-text>
        <h2>Intro</h2>
      <v-divider/>
        <h4>Supported By Vue and Vuetify</h4>
        <h4>Copyright 2019-2019.9646516.All Rights Reserved</h4>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  data: () => ({
    slider: 200
  }),

  computed: {
    avatarSize() {
      return `${this.slider}px`;
    }
  }
};
</script>