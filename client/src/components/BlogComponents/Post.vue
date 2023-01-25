<template>
  <v-container class="post-detail">
    <v-row class="align-center justify-center">
      <v-col sm="8" class="text-left">
        <h1>{{ postDetail.title }}</h1>
      </v-col>
      <v-col sm="4" class="text-right">
        <v-chip class="ma-2" color="primary">
          {{ postDetail.category_name }}
        </v-chip>
        <v-chip class="ma-2" color="secondary">
          {{ postDetail.author_username }}
        </v-chip>
        <!-- 1 like -->
        <v-chip outlined class="mx-2" @click="votePost(1)">
          <v-avatar left>
            <v-icon icon color="success" small>mdi-thumb-up</v-icon>
          </v-avatar>
          {{ postDetail.like }}
        </v-chip>
        <!-- 2 dislike -->
        <v-chip outlined class="mx-2" @click="votePost(2)">
          <v-avatar left>
            <v-icon color="error" small>mdi-thumb-down</v-icon>
          </v-avatar>
          {{ postDetail.dislike }}
        </v-chip>
              <v-btn v-if="isUser" color="error" icon @click="deletePost(post_id)">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
      </v-col>
    </v-row>

    <v-row class="align-center justify-center">
      <v-col sm="12">
        <v-row>
          <v-col sm="8">
            <p>
              {{ postDetail.content }}
            </p>
          </v-col>
          <v-col sm="4" class="text-right">
            <v-img
              max-height="480"
              contain
              :src="postDetail.img_base64"
            ></v-img>
          

          </v-col>
        </v-row>
        <v-row v-for="(item, index) in comments" :key="index">
          <v-col sm="4" md="8" class="text-left">
            <v-row>
              <v-icon> mdi-account-circle </v-icon>
              <h5>
                {{ item.author_username }}
              </h5>
            </v-row>
            <v-row>
              <p>
                {{ item.comment_content }}
              </p>
            </v-row>
          </v-col>
          <v-col sm="12" md="12" class="text-right">
            <v-btn
              v-if="currentUser.uid.$oid === item.author_id.$oid"
              color="error"
              icon
              @click="deletePostComments(item._id.$oid)"
            >
              <v-icon>mdi-delete</v-icon></v-btn
            >
            <v-divider class="mb-2"></v-divider>
          </v-col>
        </v-row>
        <v-row>
          <v-col sm="6">
            <v-card class="elevation-0">
              <v-card-title primary-title>
                <div>
                  <h4 class="headline mb-0 primary--text">Add comment</h4>
                </div>
              </v-card-title>
              <v-card-text>
                <v-textarea v-model="newCommentContent"> </v-textarea>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn text color="primary" @click="postNewComment">send</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "post-component",
  data() {
    return {
      postDetail: {},
      comments: [],
      categories: [],
      isUser: false,
      isCommentUser: false,
      post_id: this.$route.params.postID,
      newCommentContent: "",
    };
  },
  mounted() {
    this.getBlogCategories();
    this.getPost();
    this.getPostComments();
  },
  computed: {
    ...mapGetters(["currentUser"]),
  },
  methods: {
    getPost() {
      this.axios.get("blog-posts/" + this.post_id).then((response) => {
        this.postDetail = response.data[0];
        if (this.currentUser.uid.$oid === this.postDetail.author_id.$oid) {
          this.isUser = true;
        }
        else {
          this.isUser = false;
        }
        this.display();
      });
    },
    getPostComments() {
      this.axios.get("comment/" + this.post_id).then((response) => {
        this.comments = response.data[0];
      });
    },
    deletePostComments(_id) {
      const bodyFormData = {
        id: _id,
      };
      this.axios({
        method: "delete",
        url: "comment/" + this.post_id,
        data: JSON.stringify(bodyFormData),
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      }).then(() => {
        this.getPostComments();
      });
    },
    getBlogCategories() {
      this.axios.get("blog-posts/categories").then((response) => {
        this.categories = response.data;
      });
    },
    display() {
      this.categories.map((element) => {
        if (element.category_id === this.postDetail.category_id) {
          this.postDetail.category_name = element.category_name;
        }
      });
    },
    postNewComment() {
      const bodyFormData = {
        post_id: this.post_id,
        author_id: this.currentUser.uid.$oid,
        comment_content: this.newCommentContent,
        author_username: this.currentUser.username,
      };
      this.axios({
        method: "post",
        url: "comment/" + this.post_id,
        data: JSON.stringify(bodyFormData),
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      })
        .then(() => {
          this.newCommentContent = "";
          this.getPostComments();
        })
        .catch((err) => {
          console.log(err);
        });
    },
    votePost(_vote_value) {
      const bodyFormData = {
        vote_value: _vote_value,
        post_id: this.post_id,
        author_id: this.currentUser.uid.$oid,
      };
      this.axios({
        method: "post",
        url: "vote",
        data: JSON.stringify(bodyFormData),
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      }).then((response) => {
        if (response.status == 200) {
          this.getPost();

        }
      });
    },
    deletePost(_id) {
      const bodyFormData = {
        id: _id,
      };
      this.axios({
        method: "delete",
        url: "blog-posts/" + _id,
        data: JSON.stringify(bodyFormData),
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          "Access-Control-Allow-Origin": "*"
        },
      }).then(() => {
        this.$router.push({ name: "Posts" });
      });
    },
  },
};
</script>

<style></style>
