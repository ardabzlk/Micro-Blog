<template>
  <div>
    <v-app-bar app color="primary" class="mb-12" dark>
      <div class="d-flex align-center">
        <router-link to="/" class="cursor-pointer">
        <v-img src="@/assets/logo-black.svg" max-height="80" max-width="150"></v-img>
        </router-link>
      </div>

      <v-spacer></v-spacer>

      <router-link to="/"><div class="white--text mx-2">Home</div></router-link>
      <router-link to="/Posts"
        ><div class="white--text mx-2">Posts</div></router-link
      >

      <router-link to="/user"
        ><div class="white--text mx-2">User</div></router-link
      >
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon color="white" dark v-bind="attrs" v-on="on">
            <v-icon>mdi-account</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item>
            <v-list-item-title>
             
        
             
                <div class="secondary--text font-weight-black cursor-pointer"
                        @click="goToProfile(currentUser)"
            
                >
                  {{ this.currentUser.username }}
                </div>
           </v-list-item-title
            ></v-list-item
          >

          <v-list-item>
            <v-list-item-title
              class="text-primary"
              style="cursor: pointer"
              @click="logout()"
              ><div class="primary--text cursor-pointer">
                Logout
              </div></v-list-item-title
            >
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
    <router-view />
    <FooterC></FooterC>
  </div>
</template>

<script>
import { LOGOUT } from "@/core/services/store/auth.module";
import { mapGetters, mapState } from "vuex";
import FooterC from "./Footer.vue";
export default {
  data() {
    return {
      menuItems: [{ title: "Profile", route: "/user" }],
    };
  },
  components: {
    FooterC,
  },

  mounted() {
    if (!this.isAuthenticated) {
      this.$router.push({ name: "login" }).then(() => {
        this.$store.dispatch(LOGOUT);
      });
    }
  },
  beforeDestroy() {
    this.logout();
  },
  methods: {
    logout() {
      this.$store.dispatch(LOGOUT);
      this.$router.push("Login");
    },
        goToProfile(item) {
      this.$router.push({ name: "Profile", params: { userID: item.uid.$oid } });
      console.log(item);
    },
  },

  computed: {
    ...mapState({
      errors: (state) => state.auth.errors,
    }),
    ...mapGetters(["isAuthenticated", "currentUser"]),
  },
};
</script>

<style></style>
