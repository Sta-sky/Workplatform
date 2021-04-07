<template>
  <div style="height:100%;" class="scrollStyle main">
    <div class="posBox">
      <div class="loginWrap">
        <div class="bgLeft"></div>
        <div class="bgRight">
          <div class="rightMain">
            <el-form
              ref="login_form"
              :rules="loginRules"
              :model="login_form"
              class="login_form"
            >
              <el-form-item
                class="login_form_item"
                prop="account"
                :class="focusOne ? 'focusOne' : ''"
              >
                <el-input
                  @focus="focusName"
                  @blur="blurName"
                  v-model.trim="login_form.account"
                  clearable
                  placeholder="账户"
                ></el-input>
                <i
                  v-show="login_form.account === ''"
                  class="el-icon-s-custom iconclass"
                ></i>
              </el-form-item>
              <el-form-item
                class="login_form_item"
                prop="password"
                :class="focusTwo ? 'focusTwo' : ''"
              >
                <el-input
                  placeholder="密码"
                  show-password
                  @focus="focusPsd"
                  @blur="blurPsd"
                  @keypress.enter.native="handleLogin"
                  v-model="login_form.password"
                />
                <i
                  v-show="login_form.password === ''"
                  class="el-icon-lock iconclass"
                ></i>
              </el-form-item>
              <el-form-item>
                <el-button
                  type="primary"
                  @click="handleLogin"
                  :loading="loading"
                  class="login_btn"
                >
                  <span class="lbSpan">LOGIN</span>
                  <i class="iconfont icon-qianjin lbi"></i>
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </div>
      <div class="starBox">
        <div class="light light1"></div>
        <div class="light light2"></div>
        <div class="light light3"></div>
        <div class="light light4"></div>
        <div class="light light5"></div>
        <div class="light light6"></div>
        <div class="light light7"></div>
        <div class="light light8"></div>
        <div class="light light9"></div>
        <div class="light light11"></div>
        <div class="light light12"></div>
        <div class="light light13"></div>
        <div class="light light14"></div>
        <div class="light light15"></div>
        <div class="light light16"></div>
        <div class="light light17"></div>
        <div class="light light18"></div>
        <div class="light light19"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { encrypt } from "@/utils/encrypt";
export default {
  data() {
    return {
      login_form: {
        account: "",
        password: ""
      },
      loginRules: {
        account: [{ required: true, message: "请输入账号", trigger: "blur" }],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }]
      },
      loading: false,
      firstCview: true,
      randomFour: "",
      focusOne: false,
      focusTwo: false,
      userLabel: " ",
      psdLabel: " ",
      userShow: "USER NAME",
      psdShow: "PASSWORD"
    };
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect;
      },
      immediate: true
    }
  },
  created() {},
  methods: {
    focusName() {
      this.userLabel = "USER NAME";
      this.userShow = "";
      this.focusOne = true;
    },
    focusPsd() {
      this.psdLabel = "PASSWORD";
      this.psdShow = "";
      this.focusTwo = true;
    },
    blurName() {
      // this.userLabel = "";
      this.focusOne = false;
    },
    blurPsd() {
      // this.psdLabel = "";
      this.focusTwo = false;
    },
    handleLogin() {
      if (this.login_form.account === "" || this.login_form.password === "") {
        this.$notify({
          title: "警告",
          message: "请输入账号/密码",
          type: "warning",
          duration: 3000
        });
        return;
      }
      var psd = this.login_form.password;
      var encrypted = encrypt(psd);
      var sendData = {
        username: this.login_form.account,
        passwd: encrypted
      };
      this.$refs.login_form.validate(valid => {
        if (valid) {
          this.loading = true;
          this.$store
            .dispatch("LoginByUsername", sendData)
            .then(() => {
              this.loading = false;
              this.$router.push({ path: "/main/task" });
            })
            .catch(error => {
              if (error !== undefined && error !== null) {
                this.$message.error(error.message);
              }
              this.loading = false;
            });
        } else {
          return false;
        }
      });
    }
  }
};
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.main {
  width: 100%;
  height: 100%;
  background: url(../../assets/img/login_bak.png);
  background-size: 100% 100%;
  .posBox {
    width: 100%;
    height: 100%;
    position: relative;
    .loginWrap {
      width: 1200px;
      position: absolute;
      right: 18%;
      top: 12%;
      z-index: 3;
      height: 740px;
      display: inline-flex;
      .bgLeft {
        width: 640px;
        height: 104%;
        background: url(../../assets/img/loginbak_left.png) no-repeat;
        background-size: 100%;
      }
      .bgRight {
        width: 560px;
        height: 100%;
        padding: 81px 0 74px 0px;
        .rightMain {
          width: 80%;
          height: 100%;
          background: url(../../assets/img/loginbak_right.png) no-repeat;
          background-size: 100% 100%;
          padding: 76px;
          .login_form {
            margin-top: 40%;
            width: 100%;
            height: 100%;
            font-size: 18px;
            .login_form_item {
              margin-bottom: 60px;
              .code_box_none {
                letter-spacing: 1px;
                color: #458ff7;
                cursor: pointer;
                width: 120px;
                position: absolute;
                right: -5px;
                top: -5px;
              }
              .iconclass {
                position: absolute;
                bottom: 9px;
                right: 8px;
                font-size: 18px;
                color: #5788fa;
              }
              .code_box {
                cursor: pointer;
                width: 100px;
                height: 40px;
                position: absolute;
                right: -5px;
                top: -5px;
              }
            }
            .login_btn {
              width: 100%;
              height: 40px;
              margin-top: 10%;
              background-color: #195eff;
              border-color: #195eff;
              border-radius: 20px;
              position: relative;
              box-shadow: 0px 6px 34px #195eff;
              .lbSpan {
                display: inline-block;
                font-family: "strong";
                font-size: 16px;
                letter-spacing: 1px;
              }
              .lbi {
                position: absolute;
                right: 20%;
              }
            }
          }
        }
      }
      .login_box {
        .login_right_logo {
          .imgOne {
            width: 70px;
            height: 82px;
            margin-bottom: 7%;
          }
          .imgTwo {
            width: 380px;
            height: 34px;
            margin-bottom: 20%;
          }
        }
      }
    }
    .starBox {
      width: 100%;
      height: 100%;
      overflow: hidden;
      position: relative;
    }
    .light {
      width: 100px;
      height: 260px;
      position: absolute;
      background: url(../../assets/img/img_lineUP_login.png);
      background-size: 100% 100%;
    }
    .light1 {
      left: 1%;
      top: 10%;
      animation: 4s lightUp linear infinite;
    }
    .light2 {
      left: 5%;
      top: 20%;
      animation: 5s lightUp1 linear infinite;
    }
    .light3 {
      left: 10%;
      top: 22%;
      animation: 4s lightUp2 linear infinite;
    }
    .light4 {
      left: 15%;
      top: 28%;
      animation: 6s lightUp3 linear infinite;
    }
    .light5 {
      left: 20%;
      top: 5%;
      animation: 4.5s lightUp4 linear infinite;
    }
    .light6 {
      left: 25%;
      top: 26%;
      animation: 5.5s lightUp5 linear infinite;
    }
    .light7 {
      left: 30%;
      top: 24%;
      animation: 6.5s lightUp6 linear infinite;
    }
    .light8 {
      left: 35%;
      top: 22%;
      animation: 3s lightUp7 linear infinite;
    }
    .light9 {
      left: 40%;
      top: 25%;
      animation: 3.5s lightUp8 linear infinite;
    }
    .light11 {
      left: 45%;
      top: 10%;
      animation: 4s lightUp linear infinite;
    }
    .light12 {
      left: 50%;
      top: 20%;
      animation: 5s lightUp1 linear infinite;
    }
    .light13 {
      left: 55%;
      top: 22%;
      animation: 4s lightUp2 linear infinite;
    }
    .light14 {
      left: 60%;
      top: 28%;
      animation: 6s lightUp3 linear infinite;
    }
    .light15 {
      left: 65%;
      top: 5%;
      animation: 4.5s lightUp4 linear infinite;
    }
    .light16 {
      left: 70%;
      top: 26%;
      animation: 5.5s lightUp5 linear infinite;
    }
    .light17 {
      left: 75%;
      top: 24%;
      animation: 6.5s lightUp6 linear infinite;
    }
    .light18 {
      left: 75%;
      top: 22%;
      animation: 3s lightUp7 linear infinite;
    }
    .light19 {
      left: 85%;
      top: 25%;
      animation: 3.5s lightUp8 linear infinite;
    }
    @keyframes lightUp {
      0% {
        opacity: 0;
        top: 100%;
      }
      20% {
        opacity: 0.5;
        top: 75%;
      }
      50% {
        opacity: 1;
        top: 50%;
      }
      70% {
        opacity: 0.5;
        top: 25%;
      }
      100% {
        opacity: 0;
        top: 0%;
      }
    }
    @keyframes lightUp1 {
      0% {
        opacity: 0;
        top: 100%;
      }
      20% {
        opacity: 0.5;
        top: 75%;
      }
      50% {
        opacity: 1;
        top: 50%;
      }
      70% {
        opacity: 0.5;
        top: 25%;
      }
      100% {
        opacity: 0;
        top: 0%;
      }
    }
    @keyframes lightUp2 {
      0% {
        opacity: 0;
        top: 100%;
      }
      20% {
        opacity: 0.5;
        top: 75%;
      }
      50% {
        opacity: 1;
        top: 50%;
      }
      70% {
        opacity: 0.5;
        top: 25%;
      }
      100% {
        opacity: 0;
        top: 0%;
      }
    }
    @keyframes lightUp3 {
      0% {
        opacity: 0;
        top: 100%;
      }
      20% {
        opacity: 0.5;
        top: 75%;
      }
      50% {
        opacity: 1;
        top: 50%;
      }
      70% {
        opacity: 0.5;
        top: 28%;
      }
      100% {
        opacity: 0;
        top: 0%;
      }
    }
    @keyframes lightUp4 {
      0% {
        opacity: 0;
        top: 100%;
      }
      20% {
        opacity: 0.5;
        top: 75%;
      }
      50% {
        opacity: 1;
        top: 50%;
      }
      70% {
        opacity: 0.5;
        top: 25%;
      }
      100% {
        opacity: 0;
        top: 0%;
      }
    }
    @keyframes lightUp5 {
      0% {
        opacity: 0;
        top: 100%;
      }
      20% {
        opacity: 0.5;
        top: 75%;
      }
      50% {
        opacity: 1;
        top: 50%;
      }
      70% {
        opacity: 0.5;
        top: 25%;
      }
      100% {
        opacity: 0;
        top: 0%;
      }
    }
    @keyframes lightUp6 {
      0% {
        opacity: 0;
        top: 100%;
      }
      20% {
        opacity: 0.5;
        top: 75%;
      }
      50% {
        opacity: 1;
        top: 50%;
      }
      70% {
        opacity: 0.5;
        top: 25%;
      }
      100% {
        opacity: 0;
        top: 0%;
      }
    }
    @keyframes lightUp7 {
      0% {
        opacity: 0;
        top: 100%;
      }
      20% {
        opacity: 0.5;
        top: 75%;
      }
      50% {
        opacity: 1;
        top: 50%;
      }
      70% {
        opacity: 0.5;
        top: 25%;
      }
      100% {
        opacity: 0;
        top: 0%;
      }
    }
    @keyframes lightUp8 {
      0% {
        opacity: 0;
        top: 100%;
      }
      20% {
        opacity: 0.5;
        top: 75%;
      }
      50% {
        opacity: 1;
        top: 50%;
      }
      70% {
        opacity: 0.5;
        top: 25%;
      }
      100% {
        opacity: 0;
        top: 0%;
      }
    }
    .turn {
      width: 60px;
      height: 60px;
      position: absolute;
      background-size: 100% 100%;
    }
    .turnOne {
      left: 8%;
      top: 30%;
      background: url(../../assets/img/icon4_login.png);
      animation: animX 6s cubic-bezier(0.36, 0, 0.64, 1) -4.5s infinite alternate,
        animY 6s cubic-bezier(0.36, 0, 0.64, 1) 0s infinite alternate;
    }
    /* 动画 */
    @keyframes animX {
      0% {
        left: 8%;
      }
      100% {
        left: 40%;
      }
    }
    @keyframes animY {
      0% {
        top: 30%;
      }
      100% {
        top: 44%;
      }
    }
    .turnTwo {
      left: 40%;
      top: 30%;
      background: url(../../assets/img/icon3_login.png);
      animation: animX2 6s cubic-bezier(0.36, 0, 0.64, 1) -4.5s infinite alternate,
        animY2 6s cubic-bezier(0.36, 0, 0.64, 1) 0s infinite alternate;
    }
    /* 动画 */
    @keyframes animX2 {
      0% {
        left: 40%;
      }
      100% {
        left: 8%;
      }
    }
    @keyframes animY2 {
      0% {
        top: 44%;
      }
      100% {
        top: 30%;
      }
    }
    .turnThree {
      left: 18%;
      top: 30%;
      background: url(../../assets/img/icon2_login.png);
      animation: animX3 9s cubic-bezier(0.36, 0, 0.64, 1) -4.5s infinite alternate,
        animY3 9s cubic-bezier(0.36, 0, 0.64, 1) 0s infinite alternate;
    }
    /* 动画 */
    @keyframes animX3 {
      0% {
        left: 44%;
      }
      100% {
        left: 2%;
      }
    }
    @keyframes animY3 {
      0% {
        top: 50%;
      }
      100% {
        top: 30%;
        opacity: 0;
      }
    }
    .turnFour {
      top: 58%;
      background: url(../../assets/img/icon5_login.png);
      animation: animX4 12s cubic-bezier(0.36, 0, 0.64, 1) -4.5s infinite alternate,
        animY4 12s cubic-bezier(0.36, 0, 0.64, 1) 0s infinite alternate;
    }
    /* 动画 */
    @keyframes animX4 {
      0% {
        left: -14%;
      }
      100% {
        left: 52%;
      }
    }
    @keyframes animY4 {
      0% {
        top: 26%;
        opacity: 0;
      }
      100% {
        top: 52%;
      }
    }
    .turnFive {
      left: 88%;
      top: 44%;
      background: url(../../assets/img/icon1_login.png);
      animation: animX5 15s cubic-bezier(0.36, 0, 0.64, 1) -4.5s infinite alternate,
        animY5 15s cubic-bezier(0.36, 0, 0.64, 1) 0s infinite alternate;
    }
    /* 动画 */
    @keyframes animX5 {
      0% {
        left: 56%;
      }
      100% {
        left: -16%;
      }
    }
    @keyframes animY5 {
      0% {
        top: 70%;
      }
      100% {
        top: 12%;
        opacity: 0;
      }
    }
    .turnSix {
      left: 8%;
      bottom: 38%;
      background: url(../../assets/img/icon6_login.png);
      animation: animX6 9s cubic-bezier(0.36, 0, 0.64, 1) -4.5s infinite alternate,
        animY6 9s cubic-bezier(0.36, 0, 0.64, 1) 0s infinite alternate;
    }
    /* 动画 */
    @keyframes animX6 {
      0% {
        left: 0%;
      }
      100% {
        left: 50%;
      }
    }
    @keyframes animY6 {
      0% {
        bottom: 54%;
        opacity: 0;
      }
      100% {
        bottom: 22%;
      }
    }
  }
}
</style>
<style rel="stylesheet/scss" lang="scss">
.login_form {
  .login_form_item {
    .el-input__inner {
      padding: 0;
      color: #434be0;
      font-size: 18px;
      border: none;
      border-radius: 0;
      background: #fff;
      border-bottom: 1px solid #ebedf2;
    }
    .el-input__suffix {
      .el-input__suffix-inner {
        border-color: none;
        .el-icon-circle-close:before {
          content: "\e79d" !important;
        }
        .el-icon-view:before {
          font-size: 18px;
          content: "\e6e5" !important;
        }
      }
      .el-input__clear {
        color: #5788fa !important;
        &:hover {
          color: #1959f0 !important;
        }
      }
    }
  }
  .el-form-item.is-error {
    .el-form-item__label {
      color: #f56c6c;
    }
    .el-input__inner {
      border-color: #f56c6c;
    }
  }
  .focusOne {
    .el-form-item__label {
      color: #1959f0;
    }
    .el-input__inner {
      border-color: #1959f0;
    }
  }
  .focusTwo {
    .el-form-item__label {
      color: #1959f0;
    }
    .el-input__inner {
      border-color: #1959f0;
    }
  }
}
</style>
