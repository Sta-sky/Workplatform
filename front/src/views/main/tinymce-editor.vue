<template>
  <div class="tinymceDiv">
    <textarea :id="id"></textarea>
  </div>
</template>
<script>
import tinymce from "tinymce/tinymce";
//这下面是tinymce的插件
import "tinymce/themes/silver/theme";
import "tinymce/plugins/image"; // 插入上传图片插件
import "tinymce/plugins/media"; // 插入视频插件
import "tinymce/plugins/table"; // 插入表格插件
import "tinymce/plugins/lists"; // 列表插件
import "tinymce/plugins/wordcount"; // 字数统计插件
import "tinymce/plugins/code"; //显示源代码插件
import "tinymce/plugins/advlist"; // 这几条引入是因为我的导入不了，不知道为啥
import "tinymce/plugins/link";
import "tinymce/plugins/textcolor";
import "tinymce/plugins/paste";
import "tinymce/plugins/colorpicker";
import "tinymce/plugins/contextmenu";

//这里写你自己存放语言包的路径
import "@/assets/js/zh_CN.js";
export default {
  name: "",
  props: {
    id: String,
    tinyVal: String, //内容绑定
    height: Number,
    value: String
  },
  data() {
    return {
      init: {
        selector: "#" + this.id,
        language: "zh_CN",
        // skin_url: "/static/tinymce/skins/ui/oxide",
        base_url: "/static/tinymce",
        //插件-实现插入图片等功能
        plugins: "link code table wordcount media image media",
        //工具栏-根据自己需要增减功能
        toolbar:
          "bold italic underline strikethrough | fontsizeselect | forecolor backcolor | alignleft aligncenter alignright alignjustify | bullist numlist | outdent indent blockquote | undo redo | link unlink image code | removeformat | uploadimg",
        branding: false,
        menubar: false, //顶部菜单栏显示
        min_height: this.height, //高度
        statusbar: false,
        images_upload_handler: (blobInfo, success, failure) => {
          this.handleImgUpload(blobInfo, success, failure);
        },
        file_picker_callback: (callback, value, meta) => {
          this.handelVideo(callback, value, meta);
        }
      },
      resVideo: "http://www.baidu.com" //返回的视频url
    };
  },
  methods: {
    handelVideo(callback, value, meta) {
      console.log(value, meta, "file");
      if (meta.filetype == "media") {
        let input = document.createElement("input"); //创建一个隐藏的input
        input.setAttribute("type", "file");
        let that = this;
        input.onchange = function() {
          let file = this.files[0]; //选取第一个文件
          console.log(file, "file");
          // that.uploadImg(that.qiniuToken, file, "video"); // 上传视频拿到url
          // if (that.uploaded) {
          callback(that.resVideo, { title: file.name }); //将url显示在弹框输入框中
          // } else {
          // setTimeout(() => {
          //   callback(that.resVideo, { title: file.name });
          // }, 2000);
          // }
        };
        //触发点击
        input.click();
      }
    },
    handleImgUpload(blobInfo, success) {
      let formdata = new FormData();
      formdata.set("upload_file", blobInfo.blob());
      var src = "data:image/png;base64," + blobInfo.base64();
      // let new_headers = { headers: this.headers };
      // let upload_url = process.env.BASE_API + "/website/uploadfile";
      // axios.post(upload_url, formdata, new_headers).then(res => {
      //   // console.log(res.data.data)
      // tinymce.get(this.id).insertContent(
      //   `<img src = ${src}></img>`
      // );
      success(src);
      // }).catch(res => {
      //   failure('error')
      // })
    },
    release() {
      //content 是文本内容带标签
      let content = tinymce.get(this.id).getContent();
      // getContent( { 'format' : 'text'} );//这是获取里面的文本文件，不带标签
      return content;
    },
    /**外部调用该方法，可以修改绑定数据*/
    setData(data) {
      console.log(data);
      tinymce.activeEditor.setContent(data);
      // tinymce.editors[0].setContent("需要设置的编辑器内容")
    } //数据回填
  },
  mounted() {
    //配置的初始化
    tinymce.init(this.init);
  },
  beforeDestroy() {
    //销毁
    tinymce.get(this.id).destroy();
  },
  watch: {
    // tinyVal: {
    //   immediate: true,
    //   // deep: true,
    //   handler(newVal) {
    //     tinymce.get(this.id).setContent(newVal); //动态设置内容
    //   }
    // }
    tinyVal(val) {
      tinymce.get(this.id).setContent(val); //动态设置内容
    }
  }
};
</script>
<style>
.tox-tinymce-aux {
  z-index: 5000 !important;
}
.tinymceDiv {
  width: 100%;
  height: 100%;
}
</style>
