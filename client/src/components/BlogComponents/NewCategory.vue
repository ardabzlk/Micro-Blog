<template>
  <v-container>
    <v-row class="align-center justify-center">
      <v-col cols="6">
        <v-text-field
          :rules="required"
          label="Category Name"
          required
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row class="align-center justify-center">
      <v-col cols="6">
        <v-btn color="success" class="mr-4" @click="newCategory">
          POST IT
        </v-btn>
        <v-btn color="error" class="mr-4" @click="reset"> clear </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

export default {
    name: "new-category",
    data: () => ({
        valid: true,
        required: [(v) => !!v || "This field is required"],
    }),
};
</script>
