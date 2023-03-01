import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "@/core/services/store";
import ApiService from "@/core/services/api.service";

import { VERIFY_AUTH } from "@/core/services/store/auth.module";

import vuetify from "./plugins/vuetify";
import axios from "axios";
import VueAxios from "vue-axios";
Vue.use(VueAxios, axios);

// GOOD
router.beforeEach((to, from, next) => {
  // Ensure we checked auth before each page load.
  if (to.name == "404") {
    next();
  } else {
    // Ensure we checked auth before each page load.
    if (
      !store.state.auth.isAuthenticated &&
      // ❗️ Avoid an infinite redirect
      to.meta.requiresAuth
    ) {
      router.push("/Login");
    } else {
      Promise.all([store.dispatch(VERIFY_AUTH)]).then(next);
    }
  }

  // reset config to initial state

  // Scroll page to top on every route change
  setTimeout(() => {
    window.scrollTo(0, 0);
  }, 100);
});

(async () => {
  await fetch("./config.json")
    .then((res) => {
      console.log(res);
      if (res.status >= 200 && res.status < 300) {
        return res;
      } else {
        let err = new Error(res.statusText);
        err.response = res;
        alert("Failed to load config. Will try again. Error:  " + err);
        window.location.reload(true);
      }
    })
    .then((res) => res.json())
    .then((config) => {
      ApiService.init(config.API_BASE_URL);
      Vue.config.productionTip = config.productionTip;
    })
    .then(() => {
      new Vue({
        router,
        store,
        vuetify,
        render: (h) => h(App),
      }).$mount("#app");
    })
    .catch((err) => {
      alert("Failed to load config. Will try again. Error:  " + err);
      window.location.reload(true);
    });
})();



