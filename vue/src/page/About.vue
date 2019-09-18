<template>
  <div>
    <v-card style="margin-block-end: 2em;">
      <v-card-text>
        <v-card-title class="headline">About</v-card-title>
        <v-divider />
      </v-card-text>
      <v-layout column>
        <v-container>
          <v-flex xs12 sm6>
            <v-slider v-model="slider" :min="100" :max="512" label="Size"></v-slider>
          </v-flex>
          <v-flex xs12 sm6 align-center layout text-xs-center>
            <v-avatar :size="avatarSize" color="grey lighten-4">
              <img
                src="https://gss3.bdstatic.com/7Po3dSag_xI4khGkpoWK1HF6hhy/baike/c0%3Dbaike92%2C5%2C5%2C92%2C30/sign=dc707ea38e5494ee932f074b4c9c8b9b/aec379310a55b319c46a7d6941a98226cffc171e.jpg"
                alt="avatar"
              />
            </v-avatar>
          </v-flex>
        </v-container>
        <v-flex sm12>
          <v-card-text>
            <v-card-title class="headline">BOJV4-Refreshed</v-card-title>
            <v-card-title class="headline">Supported By Vue and Vuetify</v-card-title>
            <v-card-title class="headline">Develop And Maintain By BUPT ACM Team</v-card-title>
            <v-card-title class="headline">
              <a style="color:black;">Contact:</a>
              <a
                href="mailto:buptacm@qq.com"
                style="color:#80407B;text-decoration: blink;"
              >buptacm@qq.com</a>
            </v-card-title>
          </v-card-text>
        </v-flex>
      </v-layout>
    </v-card>
    <v-card style="margin-block-end: 2em;">
      <v-card-text>
        <v-card-title class="headline">Develop Team</v-card-title>
        <v-divider />
        <v-flex>
          <a href="https://github.com/wangzitian0">
            <v-avatar size="135px" tile>
              <img src="https://avatars3.githubusercontent.com/u/8103666?s=400" />
            </v-avatar>
          </a>
          <a href="https://github.com/Little-Wallace">
            <v-avatar size="135px" tile>
              <img src="https://avatars0.githubusercontent.com/u/16376959?s=400" />
            </v-avatar>
          </a>
          <a href="https://github.com/MyonKeminta">
            <v-avatar size="135px" tile>
              <img src="https://avatars3.githubusercontent.com/u/9948422?s=400" />
            </v-avatar>
          </a>
          <a href="https://github.com/dimpurr">
            <v-avatar size="135px" tile>
              <img src="https://avatars3.githubusercontent.com/u/5173244?s=400" />
            </v-avatar>
          </a>
        </v-flex>

        <v-flex>
          <a href="https://github.com/birdstorm">
            <v-avatar size="135px" tile>
              <img src="https://avatars0.githubusercontent.com/u/15857134?s=400" />
            </v-avatar>
          </a>
          <a href="https://github.com/Mr-Phoebe">
            <v-avatar size="135px" tile>
              <img src="https://avatars2.githubusercontent.com/u/15867761?s=400" />
            </v-avatar>
          </a>
          <a href="https://github.com/Macaulish64">
            <v-avatar size="135px" tile>
              <img src="https://avatars1.githubusercontent.com/u/20122039?s=400" />
            </v-avatar>
          </a>
          <a href="https://github.com/fipped">
            <v-avatar size="135px" tile>
              <img src="https://avatars2.githubusercontent.com/u/9395718?s=400" />
            </v-avatar>
          </a>
        </v-flex>

        <v-flex>
          <a href="https://github.com/hoowater">
            <v-avatar size="135px" tile>
              <img src="https://avatars2.githubusercontent.com/u/10193211?s=400" />
            </v-avatar>
          </a>
          <a href="https://github.com/9646516">
            <v-avatar size="135px" tile>
              <img src="https://avatars2.githubusercontent.com/u/38785664?s=400" />
            </v-avatar>
          </a>
        </v-flex>
        <v-divider />
        <v-card-title class="headline">Copyright 2016-2019 BUPT ACM Team.All Rights Reserved</v-card-title>
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