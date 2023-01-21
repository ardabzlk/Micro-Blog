<template>
  <div class="test">
    <v-row class="align-center justify-center">
      <v-col cols="8">
        <v-card class="mt-12">
          <v-card-title>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="userList"
            @click:row="goToProfile"
            :search="search"
            :items-per-page="5"
            class="elevation-1 cursor-pointer"
          ></v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  data: () => ({
     search: '',
    headers: [
      {
        text: "Name",
        align: "start",
        sortable: false,
        value: "name",
      },
      { text: "Surname", value: "surname" },
    ],
    userList: [],
  }),

  mounted() {
    this.getUserList();
  },
  methods: {
    goToProfile(item) {
      this.$router.push({ name: "Profile", params: { userID: item._id.$oid } });
      console.log(item);
    },
    getUserList() {
      let data = {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("id_token"),
        },
      };
      this.axios.get("http://127.0.0.1:8000/users", data).then((response) => {
        this.userList = response.data;
      });
    },
  },
};
</script>
