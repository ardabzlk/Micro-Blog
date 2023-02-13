<template>
      <v-footer absolute dark padless>
        <v-card
          flat
          tile
          class="lighten-1 white--text text-center footer__card pa-0"
        >
          <v-card-text>
            <v-btn
              v-for="(item, index) in icons"
              :key="index"
              class="mx-4 white--text"
              icon
              :href="item.url"
              target="_blank"
            >
              <v-icon size="24px">
                {{ item.icon }}
              </v-icon>
            </v-btn>
          </v-card-text>

          <v-card-text class="white--text pt-0"> </v-card-text>

          <v-divider></v-divider>

          <v-card-text class="white--text">
            {{ new Date().getFullYear() }} — <strong>Micro-Blog</strong>
          </v-card-text>
        </v-card>
      </v-footer>
</template>
<script>
export default {
  name: "footer-component",
  data() {
    return {
      icons: [
        {
          icon: "mdi-github",
          url: "https://github.com/ardabzlk/Micro-Blog-Playground",
        },
        {
          icon: "mdi-linkedin",
          url: "https://www.linkedin.com/in/ardabozlak/",
        },
      ],
    };
  },
};
</script>
