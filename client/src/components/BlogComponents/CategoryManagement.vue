<template>
  <v-container>
    <v-row class="align-center justify-center">
      <v-col cols="6">
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-text-field
            :rules="(required, blank)"
            label="Category Name"
            v-model="categoryName"
            required
          ></v-text-field>
        </v-form>
      </v-col>
    </v-row>
    <v-row class="align-center justify-center">
      <v-col cols="6">
        <v-btn
          color="success"
          class="mr-4"
          :disabled="!valid"
          @click="newCategory"
        >
          POST IT
        </v-btn>
        <v-btn color="error" class="mr-4" @click="reset"> clear </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-data-table
          :headers="categoryHeaders"
          :items="categories"
          :items-per-page="5"
          class="elevation-1"
        >
          <template v-slot:[`item.delete`]="{ item }">
            <v-icon small @click="deleteCategory(item.category_id)">
              mdi-delete
            </v-icon>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "category-management",
  data: () => ({
    valid: false,
    required: [(v) => !!v || "This field is required"],
    blank: [(v) => (v && !!v.trim()) || "Value cannot be blank"],
    categoryName: "",
    categories: [],
    categoryHeaders: [
      {
        text: "Category Name",
        value: "category_name",
      },
      {
        text: "Category ID",
        value: "category_id",
      },
      {
        text: "",
        value: "delete",
      },
    ],
  }),
  methods: {
    newCategory() {
      if (this.categoryName != "" && this.$refs.form.validate()) {
        const bodyFormData = {
          category_name: this.categoryName,
        };
        axios({
          method: "post",
          baseURL: "http://127.0.0.1:8000/blog-posts/categories",
          data: JSON.stringify(bodyFormData),
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        })
          .then((res) => {
            if (res.status == 200) {
              this.getCategories();
            }
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },
    getCategories() {
      axios({
        method: "get",
        baseURL: "http://127.0.0.1:8000/blog-posts/categories",
      })
        .then((res) => {
          this.categories = res.data.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    deleteCategory(_param_category_id) {
      const bodyFormData = {
        category_id: _param_category_id,
      };
      try {
        axios({
          method: "DELETE",
          baseURL: "http://127.0.0.1:8000/blog-posts/categories",
          data: JSON.stringify(bodyFormData),
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        }).then((res) => {
          if (res.status == 200) {
            this.getCategories();
          }
        });
      } catch (error) {
        console.log(error);
      }
    },
    reset() {
      this.$refs.form.resetValidation();
      this.$refs.form.reset();
    },
  },
  mounted() {
    this.getCategories();
  },
};
</script>
