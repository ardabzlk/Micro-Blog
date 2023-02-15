<template>
  <v-container>
    <v-row>
      <v-col>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-row>
            <v-col sm="4" xs="4">
              <v-text-field
                v-model="postDetail.title"
                :rules="required"
                label="Title"
                required
              ></v-text-field>
            </v-col>

            <v-col sm="4" xs="4">
              <v-select
                v-model="postDetail.category"
                :items="categoryItems"
                item-text="category_name"
                item-value="category_id"
                :rules="[(v) => !!v || 'Item is required']"
                label="Item"
                required
              ></v-select>
            </v-col>
            <v-col sm="4" xs="4">
              <v-file-input
                label="File input"
                filled
                accept="image/png, image/jpg, image/jpeg"
                prepend-icon="mdi-camera"
                @change="setFile"
              ></v-file-input>
            </v-col>
          </v-row>

          <v-textarea
            v-model="postDetail.content"
            :rules="required"
            label="Content"
            required
          ></v-textarea>
          <v-row class="text-right">
            <v-col>
              <v-btn
                :disabled="!valid"
                color="success"
                class="mr-4"
                @click="newBlogPost"
              >
                POST IT
              </v-btn>

              <v-btn color="error" class="mr-4" @click="reset"> clear </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import { mapGetters } from "vuex";
import axios from "axios";
export default {
  name: "new-post",
  data: () => ({
    valid: true,
    required: [(v) => !!v || "This field is required"],
    categoryItems: [],
    postDetail: { title: "", content: "", category: null },
    id_token: "Bearer " + localStorage.getItem("id_token"),
    image: {},
    upFile: null,
  }),
  mounted() {
    this.getPostCategories();
  },
  methods: {
    newBlogPost() {
      const bodyFormData = {
        user_id: this.currentUser.uid.$oid,
        title: this.postDetail.title,
        content: this.postDetail.content,
        category_id: this.postDetail.category,
        username: this.currentUser.username,
        img_base64: this.upFile,
      };
      axios({
        method: "post",
        baseURL: "http://127.0.0.1:8000/blog-posts",
        data: JSON.stringify(bodyFormData),
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      })
        .then(() => {
          this.$router.push({ name: "Posts" });
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getPostCategories() {
      let data = {
        headers: {
          Authorization: this.id_token,
        },
      };
      this.axios
        .get("http://127.0.0.1:8000/blog-posts/categories", data)
        .then((response) => {
          this.categoryItems = response.data.data;

        });
    },

    validate() {
      this.$refs.form.validate();
    },
    reset() {
      this.$refs.form.reset();
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    },

    setFile(e) {
      try {
        const file = e;
        this.extensionHandler = file.type.split("/")[0];
        if (
          (typeof FileReader === "function" && e.type == "image/jpeg") ||
          e.type == "image/png" ||
          e.type == "image/jpg"
        ) {
          const reader = new FileReader();
          reader.readAsDataURL(file);
          reader.onload = (event) => {
            let img = new Image();
            img.onload = () => {
              this.image.width = img.width;
              this.image.height = img.height;
            };
            this.upFile = event.target.result;
            img.src = event.target.result;
          };

          this.fileName = file.name;
        } else {
          this.newPhotoTextField = [];
          this.photoFormValid = false;
          this.fileName = "";
          this.upFile = null;
          this.file = "";
          this.image = {
            height: "",
            width: "",
          };
        }
      } catch (e) {
        this.file = "";
        this.newPhotoTextField = [];
        this.photoFormValid = false;
        this.file = "";
        this.fileName = "";
        this.upFile = null;
        this.image = {
          height: "",
          width: "",
        };
      }
    },
  },
  computed: {
    ...mapGetters(["currentUser"]),
  },
};
</script>
