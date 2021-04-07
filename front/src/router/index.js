import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);
import layoutView from "@/views/layoutPage/layoutView";
export const constantRouterMap = [
  {
    path: "/redirect",
    hidden: true,
    children: [
      {
        path: "/redirect/:path*",
        component: () => import("@/views/redirect/index")
      }
    ]
  },
  {
    path: "/login",
    component: () => import("@/views/login/login"),
    hidden: true
  },
  {
    path: "",
    component: () => import("@/views/login/login")
  },
  {
    path: "/404",
    component: () => import("@/views/errorPage/404"),
    hidden: true
  },
  {
    path: "/401",
    component: () => import("@/views/errorPage/401"),
    hidden: true
  },
  {
    path: "/main/task",
    component: layoutView,
    menuShow: true,
    children: [
      {
        path: "/main/task",
        name: "任务管理",
        component: () => import("@/views/main/task"),
        meta: {
          requireAuth: true
        }
      }
    ]
  },
  {
    path: "/main/knowledge",
    component: layoutView,
    menuShow: true,
    children: [
      {
        path: "/main/knowledge",
        name: "知识库管理",
        component: () => import("@/views/main/knowledge"),
        meta: {
          requireAuth: true
        }
      }
    ]
  },
  {
    path: "/main/todo",
    component: layoutView,
    menuShow: true,
    children: [
      {
        path: "/main/todo",
        name: "待工作",
        component: () => import("@/views/main/todo"),
        meta: {
          requireAuth: true
        }
      }
    ]
  },
  {
    path: "/main/setting",
    component: layoutView,
    menuShow: true,
    children: [
      {
        path: "/main/setting",
        name: "系统管理",
        component: () => import("@/views/main/setting"),
        meta: {
          requireAuth: true
        }
      }
    ]
  },
  {
    path: "/main/user",
    component: layoutView,
    menuShow: true,
    children: [
      {
        path: "/main/user",
        name: "用户管理",
        component: () => import("@/views/main/users"),
        meta: {
          requireAuth: true
        }
      }
    ]
  }
];
export default new Router({
  mode: "hash", // require service support
  scrollBehavior: () => ({ y: 0 }),
  // scrollBehavior: () => {
  //   history.pushState(null, null, document.URL);
  // },
  routes: constantRouterMap
});
export const asyncRouterMap = [
  //   {
  //     path: '/pdf/download',
  //     component: () => import('@/views/pdf/download'),
  //     hidden: true
  //   },
  { path: "*", redirect: "/404", hidden: true }
];
