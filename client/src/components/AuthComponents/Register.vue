<template>
  <v-container fill-height fluid>
    <v-row class="align-center justify-center">
      <v-col xl="4" lg="6" sm="8" cols="12">
        <v-card class="elevation-0" height="120%">
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-text-field
              v-model="registerInfo.name"
              :rules="nameRules"
              label="Name"
              required
            ></v-text-field>

            <v-text-field
              v-model="registerInfo.surname"
              :rules="nameRules"
              label="Surname"
              required
            ></v-text-field>
            <v-text-field
              v-model="registerInfo.username"
              :rules="nameRules"
              label="Username"
              required
            ></v-text-field>
            <v-text-field
              v-model="registerInfo.email"
              :rules="emailRules"
              label="E-mail"
              required
            ></v-text-field>
            <v-text-field
              v-model="registerInfo.password"
              label="Password"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword ? 'text' : 'password'"
              @click:append="showPassword = !showPassword"
             
              required
            ></v-text-field>

          </v-form>
          <v-card-actions>
            <v-btn
              :disabled="!valid"
              color="success"
              class="mr-4"
              @click="postUser"
              :loading="loading"
            >
              Submit
            </v-btn>
            <v-spacer></v-spacer>
            <p class="primary--text">
              Already have an account?
              <a class="success--text" @click="$router.push('login')">Login</a>
            </p>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import { REGISTER, LOGOUT } from "@/core/services/store/auth.module";

export default {
  name: "register-component",
  data() {
    return {
      valid: true,
      loading: false,
            showPassword: false,

      registerInfo: {
        name: "",
        surname: "",
        username: "",
        email: "",
        password: "",
        rPassword: "",
      },
      userList: [],

      NonEmpty: [(v) => !!v || "This field required"],
      nameRules: [(v) => !!v || "Name is required"],
      emailRules: [
        (v) => !!v || "E-mail is required",
        (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
      ],
    };
  },
  methods: {
    async postUser() {
      this.loading = true;
      const name = this.registerInfo.name;
      const surname = this.registerInfo.surname;
      const username = this.registerInfo.username;
      const email = this.registerInfo.email;
      const password = this.registerInfo.password;
      this.$store
        .dispatch(REGISTER, {
          name,
          surname,
          username,
          email,
          password,
        })
        .then(async (response) => {
          await new Promise((resolve) => setTimeout(resolve, 1000));
          this.loading = false;
          if (response.data.msg !== "Success") {
            this.$store.dispatch(LOGOUT);
          } else {
            this.$router.push("/home");
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    login(credientals) {
      this.loading = true;
      const bodyFormData = {
        email: credientals.email,
        password: credientals.password,
      };
      this.axios({
        method: "post",
        baseURL: "http://127.0.0.1:8000/login",
        data: JSON.stringify(bodyFormData),
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      })
        .then((response) => {
          if (response.status == 200) {
            localStorage.setItem("JWT", response.data.token);
            localStorage.setItem("isAuthenticated", true);
            localStorage.setItem("email", credientals.email);
          }
        })
        .catch(() => {
          this.loading = false;
        });
    },
  },
};
</script>
