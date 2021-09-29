import Vue from "vue";
import App from "./App";
import router from "./router";
import store from "./store";
import Cookies from "js-cookie";
import ElementUI from "element-ui";
import echarts from "echarts";
import i18n from "./lang"; // Internationalization
import "element-ui/lib/theme-chalk/index.css";
import "@/styles/common.scss";
import "babel-polyfill";
import "./permission";
import Router from "vue-router";
import * as filters from "./filters"; // global filters
import mavonEditor from "mavon-editor";
import "mavon-editor/dist/css/index.css";
import { bytesToSize } from "@/assets/js/validate";

// var pathName = window.location.pathname.substring(1);
// var webName = pathName == '' ? '' : pathName.substring(0, pathName.indexOf('/'));
// var s = '';
// if (webName == '') {
//   s = window.location.protocol + '//' + window.location.host;
// } else {
//   s = window.location.protocol + '//' + window.location.host + '/' + webName;
// }
// Vue.prototype.$baseUrl = s + "/avatar/";
// Vue.prototype.$websocketattr = "ws://" + window.location.hostname + ":15674/ws";
Vue.prototype.$websocketattr = "ws://127.0.0.1:8633/ws";
Vue.prototype.$baseUrl = "http://127.0.0.1:9109/avatar/";
Vue.prototype.$bytesToSize = bytesToSize;
Vue.use(mavonEditor);
const originalPush = Router.prototype.push;
Router.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err);
};
// register global utility filters.
Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key]);
});
Vue.config.productionTip = false;
Vue.prototype.$echarts = echarts;
Vue.use(ElementUI, {
  size: Cookies.get("size") || "medium", // set element-ui default size
  i18n: (key, value) => i18n.t(key, value)
});
// window.addEventListener("popstate", function() {
//   history.pushState(null, null, document.URL);
// });
new Vue({
  el: "#app",
  router,
  store,
  i18n,
  render: h => h(App)
});
