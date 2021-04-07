import axios from "axios";
import { Message, Notification } from "element-ui";
import store from "@/store";
import { getToken } from "@/utils/auth";

axios.defaults.withCredentials = true;
axios.defaults.headers["X-Requested-With"] = "XMLHttpRequest";
axios.defaults.headers.post["Content-Type"] =
  "application/x-www-form-urlencoded;charset=UTF-8";
// var pathName = window.location.pathname.substring(1);
// var webName =
//   pathName == "" ? "" : pathName.substring(0, pathName.indexOf("/"));
// var s = "";
// if (webName == "") {
//   s = window.location.protocol + "//" + window.location.host;
// } else {
//   s = window.location.protocol + "//" + window.location.host + "/" + webName;
// }
// create an axios instance
const service = axios.create({
  // baseURL:
  //   "http://192.168.8.236:7300/mock/5ff809bb0ded6600220c9789/LaneGeanPlat", // api 的 base_url
  // baseURL: s + "/api", // api 的 base_url
  baseURL: "http://127.0.0.1:9000/api", // api 的 base_url
  timeout: 60000 // request timeout
});
// request interceptor
service.interceptors.request.use(
  config => {
    if (config.url != "/users/login") {
      var token = getToken();
      config.headers["token"] = token;
      config.headers["Authorization"] = token;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// response interceptor
service.interceptors.response.use(
  response => response,
  error => {
    Message.closeAll();
    Notification.closeAll();
    if (error.response.status === 429) {
      error.message = "接口提交次数太多，请稍后再试！";
    }
    if (
      error.response.status === 50008 ||
      error.response.status === 50012 ||
      error.response.status === 50014
    ) {
      store.dispatch("LogOut").then(() => {
        Message({
          message: "当前登录已失效,请重新登录",
          type: "warning",
          duration: 5000
        });
        location.reload();
      });
    }
    return Promise.reject(error);
  }
);

export default service;
