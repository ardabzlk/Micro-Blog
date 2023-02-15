import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    redirect: "Home",
    component: () => import("@/layout/Layout.vue"),
    meta: {
      requiresAuth: true,
    },
    children: [
      {
        path: "/home",
        name: "Home",
        component: () => import("@/views/Home.vue"),
        meta: {
          requiresAuth: true,
        },
      },
      {
        path: "/user",
        name: "User",
        component: () => import("@/views/User.vue"),
        meta: {
          requiresAuth: true,
        },
      },
      {
        path: "/profile/:userID",
        name: "Profile",
        component: () => import("@/views/ProfileViews/ProfileView.vue"),
        meta: {
          requiresAuth: true,
        },
      },
      {
        path: "/posts",
        name: "Posts",
        component: () => import("@/views/BlogViews/PostsView.vue"),
        meta: {
          requiresAuth: true,
        },
      },
      {
        path: "/Posts/:postID",
        name: "Post",
        component: () => import("@/views/BlogViews/PostView.vue"),
        meta: {
          requiresAuth: true,
        },
      },
      {
        path: "/new_post",
        name: "New_Post",
        component: () => import("@/views/BlogViews/NewPostView.vue"),
        meta: {
          requiresAuth: true,
        },
      },
      {
        path: "/new-category",
        name: "New-Category",
        component: () => import("@/views/BlogViews/NewCategoryView.vue"),
        meta: {
          requiresAuth: true,
        },
      },
    ],
  },
  {
    path: "/",
    component: () => import("@/layout/ExternalLayout.vue"),
    meta: {
      requiresAuth: false,
    },
    children: [
      {
        path: "/login",
        name: "Login",
        component: () => import("@/views/AuthViews/LoginView.vue"),
        meta: {
          requiresAuth: false,
        },
      },
      {
        path: "/register",
        name: "Register",
        component: () => import("@/views/AuthViews/RegisterView.vue"),
        meta: {
          requiresAuth: false,
        },
      },
    ],
  },

  {
    path: "*",
    redirect: "/login",
  },
];

const router = new VueRouter({
  routes,
});

const onError = (e) => {
  // avoid NavigationDuplicated
  if (e.name !== "NavigationDuplicated") throw e;
};
const _push = router.__proto__.push;
// then override it
router.__proto__.push = function push(...args) {
  try {
    const op = _push.call(this, ...args);
    if (op instanceof Promise) op.catch(onError);
    return op;
  } catch (e) {
    onError(e);
  }
};

export default router;
