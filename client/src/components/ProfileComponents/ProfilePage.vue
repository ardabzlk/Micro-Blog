<template>
  <v-container fluid class="profile-section">
    <v-card class="mx-auto mt-6 pt-6" elevation="0  ">
      <v-row justify="center">
        <v-col
          align-self="start"
          class="d-flex justify-center align-center pa-0"
          cols="12"
        >
          <v-avatar
            class="profile avatar-center-heigth avatar-shadow"
            color="grey"
            size="164"
          >
            <v-icon x-large>mdi-account</v-icon>
          </v-avatar>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col>
          <h2 class="text-center">
            {{ this.userDetails.username }}
          </h2>
        </v-col>
      </v-row>
      <v-row class="d-flex justify-center" >
        <v-col cols="4">
          <v-text-field
            v-model="this.userDetails.email"
            prepend-icon="mdi-gmail"
            label="Mail"
            disabled
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" class="text-end">
          <v-list-item-content class="sutitles">
            <v-list-item-title class="text-h6"> {{postList.length}} </v-list-item-title>
            <v-list-item-subtitle class="text-caption"
              >Posts</v-list-item-subtitle
            >
          </v-list-item-content>
        </v-col>
        <v-col cols="6" class="text-start">
          <v-list-item-content class="sutitles">
            <v-list-item-title class="text-h6"> {{total_like }} </v-list-item-title>
            <v-list-item-subtitle class="text-caption"
              >Likes</v-list-item-subtitle
            >
          </v-list-item-content>
        </v-col>
      </v-row>
      <v-row class="mt-5 px-0 mx-0" v-if="!isLoading">
        <v-col
          v-for="(item, index) in filteredList"
          :key="index"
          xs="12"
          sm="6"
          md="4"
          lg="3"
        >
          <v-card max-width="420" max-height="340">
            <v-img height="200" contain :src="item.img_base64"></v-img>
            <v-card-title>
              {{ item.title }}
              <v-spacer></v-spacer>
              <span class="blue-grey--text">
                {{ item.author_username }}
              </span>
            </v-card-title>
            <v-card-subtitle
              class="d-inline-block text-truncate posts-grid__card-subt"
            >
              {{ item.content }}
            </v-card-subtitle>
            <v-card-actions>
              <v-btn
                color="orange lighten-2"
                text
                @click="toPostDetail(item._id.$oid)"
              >
                Explore
              </v-btn>
              <v-spacer></v-spacer>
              <v-chip class="mx-2">
                <v-avatar left>
                  <v-icon icon color="success" small>mdi-thumb-up</v-icon>
                </v-avatar>
                {{ item.like }}
              </v-chip>
              <v-chip class="mx-2">
                <v-avatar left>
                  <v-icon color="error" small>mdi-thumb-down</v-icon>
                </v-avatar>
                {{ item.dislike }}
              </v-chip>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters, mapState } from "vuex";

export default {
  pageTitle: "My Profile",

  data() {
    return {
      token: localStorage.getItem("id_token"),
      postList: [],
      userDetails: {},
      keyword: "",
      isLoading: false,
      total_like: 0,
    };
  },
  async created() {
    await this.posts();
  },
  mounted() {
    this.getUserDetail();
  },
  methods: {
    toPostDetail(_post_id) {
      this.$router.push({
        name: "Post",
        params: { postID: _post_id },
      });
    },
    async posts() {
      this.axios
        .get("users/" + this.$route.params.userID + "/blog-posts")
        .then((response) => {
          this.postList = response.data.data;
          this.isLoading = false;
          return this.postList;
        })
        .then(() => {
          this.postList.map((post) => {
            if (post.like) {
              this.total_like += post.like;
            }
          });
        });
    },
    getUserDetail() {
      this.axios
        .get("users/" + this.$route.params.userID)
        .then((response) => {
          this.userDetails = response.data.data[0];
        })
        .catch((error) => {
          console.log(error);
        });
    },
    count() {
      this.postList.map((post) => {
        if (post.like) {
          this.total_like += post.like;
        }

      });
    },
  },

  computed: {
    ...mapState({
      errors: (state) => state.auth.errors,
    }),
    filteredList() {
      return this.postList.filter((post) => {
        return this.keyword
          .toLowerCase()
          .split(" ")
          .every((v) => post.title.toLowerCase().includes(v));
      });
    },
    ...mapGetters(["currentUser"]),
  },
};
</script>
