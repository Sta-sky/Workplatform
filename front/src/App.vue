<template>
  <div id="app" v-cloak>
    <router-view />
  </div>
</template>

<script>
// import "./assets/fonts/iconfont.css";
export default { name: "App" };
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
[v-cloak] {
  display: none;
}
</style>
