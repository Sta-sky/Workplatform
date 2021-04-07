const path = require("path");
function resolve(dir) {
  return path.join(__dirname, dir);
}
module.exports = {
  publicPath: process.env.NODE_ENV === "production" ? "./" : "/",
  outputDir: "dist",
  assetsDir: "static",
  indexPath: "index.html",
  filenameHashing: true,
  pages: undefined,
  lintOnSave: true,
  runtimeCompiler: false,
  transpileDependencies: [],
  productionSourceMap: false,
  crossorigin: undefined,
  integrity: false,
  devServer: {
    host: "0.0.0.0",
    port: 8080,
    proxy: {
      "/": {
        target: "http://127.0.0.1:8080/",
        changeOrigin: true,
        pathRewrite: {
          "^/": ""
        },
        ws: false
      }
    }
  },
  configureWebpack: {
    resolve: {
      alias: {
        "@": resolve("src")
      }
    }
  },
  chainWebpack(config) {
    config.plugins.delete("preload");
    config.plugins.delete("prefetch");
  }
};
