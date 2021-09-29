<template>
  <div class="layout">
    <!--头部用户信息-->
    <div class="topsidebar">
      <!--logo-->
      <div class="logo">
        <img src="@/assets/img/logo_title.png" />
      </div>
      <div class="right_mod" v-if="base_info.username !== ''">
        <!-- <img :src="$baseUrl + base_info.avatar" alt="" /> -->
        <!-- <el-dropdown
          trigger="click"
          placement="bottom-start"
          style="float:left;margin-right:30px;"
        >
          <span class="el-dropdown-single" style="margin-right:10px;color:#fff;"
            >{{ base_info.username }}
            <i
              class="el-icon-arrow-down el-icon--right"
              style="font-size: 12px;"
            ></i>
          </span>
           <el-dropdown-menu slot="dropdown">
            <el-dropdown-item @click.native.stop="checkBaseInfo"
              >个人中心</el-dropdown-item
            >
            <el-dropdown-item @click.native.stop="openCreateDrawer">
              <el-badge :value="base_info.createAmount">
                我的创建
              </el-badge></el-dropdown-item
            >
            <el-dropdown-item
              v-if="base_info.roles[0] === 'admin'"
              @click.native.stop="getTasksRev"
              ><el-badge :value="base_info.reviewAmount">
                任务审核
              </el-badge></el-dropdown-item
            >
            <el-dropdown-item
              v-if="base_info.roles[0] === 'admin'"
              @click.native.stop="taskRvScore"
            >
              任务评分</el-dropdown-item
            >
            <el-dropdown-item @click.native.stop="changeOwnPsd"
              >修改密码</el-dropdown-item
            >
            <el-dropdown-item class="logoutSty" @click.native.stop="exitLog"
              >退出登录</el-dropdown-item
            >
          </el-dropdown-menu> 
        </el-dropdown>-->
        <span style="margin-right:10px;color:#000;"
          >{{ base_info.username }}
        </span>
        <span title="退出" style="margin-right:30px;" @click.stop="exitLog">
          <i class="iconfont icon-tuichu"></i>
        </span>
      </div>
      <div class="side_left" v-if="isRouterAlive">
        <!--menu-->
        <div class="sidebar_menu firstSlide">
          <el-menu
            :unique-opened="true"
            router
            :default-active="$route.path"
            mode="horizontal"
            active-text-color="#ffffff"
          >
            <template v-for="(item, index) in $router.options.routes">
              <el-menu-item
                v-if="item.menuShow"
                :key="index"
                :index="item.children[0].path"
              >
                <!-- <i :class="item.iconCls"></i> -->
                {{ item.children[0].name }}
              </el-menu-item>
            </template>
          </el-menu>
        </div>
      </div>
    </div>
    <div class="mainCon">
      <section class="app-main scrollStyle">
        <transition name="fade-transform" mode="out-in">
          <router-view v-if="isRouterAlive" />
        </transition>
      </section>
    </div>
  </div>
</template>

<script>
import { passwordReg } from "@/assets/js/validate";
// import { encrypt } from "@/utils/encrypt";
import {
  // getUserInfo,
  saveInfo,
  changePsd,
  getOwnTasksList,
  getOwnLeaksList,
  getOwnSocialList,
  getOwnTequeList,
  getOwnTequeDetail,
  getOwnUsersList,
  getTaskReviewList,
  getTaskScoreList,
  getTaskScoreOrgList,
  sureChangeScore
} from "@/api/login";
import {
  taskDetails,
  taskDel,
  getTaskReview,
  sureTaskReview
} from "@/api/task";
export default {
  name: "layoutView",
  data() {
    var emailThree = (rule, value, callback) => {
      if (!passwordReg(value)) {
        callback(
          new Error("密码长度须在7到15位之间,以字母开头且只能为字母和数字组合")
        );
      } else {
        callback();
      }
    };
    return {
      base_info: {
        avatar: "",
        username: "",
        nickname: "",
        roles: [],
        email: "",
        phone: "",
        organize: [],
        task: {
          score: 0,
          mount: 0,
          details: []
        }
      },
      isRouterAlive: true,
      loadSureChange: false,
      changePsdDrawer: false,
      addEditForm: {
        oldPsd: "",
        newPsd: "",
        reNewPsd: ""
      },
      baseInfoDrawer: false,
      loadSureAdd: false,
      rulesTwo: {
        oldPsd: [{ required: true, message: "请输入原密码", trigger: "blur" }],
        newPsd: [{ required: true, validator: emailThree, trigger: "blur" }],
        reNewPsd: [{ required: true, validator: emailThree, trigger: "blur" }]
      },
      nameRead: true,
      emailRead: true,
      phoneRead: true,
      uploadHeadImgUrl: "",
      createTitle: 0,
      createDrawer: false,
      createTasksList: [],
      createLeaksList: [],
      createSocialList: [],
      createTequeList: [],
      createUsersList: [],
      createSearch: "",
      createTotalSize: 0,
      createPage: 1,
      createSize: 10,
      createLoading: false,
      taskReviewList: [],
      trSearch: "",
      trTotalSize: 0,
      trPage: 1,
      trSize: 10,
      taskReviewDrawer: false,
      taskReviewLoading: false,
      delVisible: false,
      loadSureDel: false,
      delCon: "",
      reviewForm: {
        id: "",
        name: "",
        description: "",
        time: "",
        organize: [],
        modal: "",
        modalDes: "",
        taskMaster: "",
        weapon: [],
        radio: 0,
        reason: ""
      },
      taskDetailDrawer: false,
      taskDetail: {},
      reviewDrawer: false,
      loadSureReview: false,
      taskScoreDrawer: false,
      taskScoreLoading: false,
      scoreList: [],
      checkTaskIs: true,
      taskName: "",
      taskId: null,
      csTaskTotalScore: 0,
      sinOrg: {
        id: null,
        pro: "",
        label: "",
        score: 0
      },
      sinTaskBelong: [],
      changeSvisible: false,
      scsBtnLoading: false,
      sliderMarks: {},
      skill: {}
    };
  },
  mounted() {
    this.uploadHeadImgUrl =
      "http://127.0.0.1:8100/api/users/uploadHeadImg?token=" +
      this.$store.getters.token;
  },
  created() {
    this.getBaseInfo();
    // this.reload();
  },
  methods: {
    reload() {
      this.isRouterAlive = false;
      this.$nextTick(() => (this.isRouterAlive = true));
    },
    getBaseInfo() {
      // getUserInfo(this.$store.token)
      //   .then(response => {
      //     if (response.data.success) {
      //       this.base_info = response.data.data;
      //       this.reload();
      //     } else {
      //       this.$message.warning(response.data.info);
      //     }
      //   })
      //   .catch(error => {
      //     this.$message.error(error.message);
      //   });
      this.base_info.username = this.$store.getters.base;
      this.reload();
    },
    // 选择头像
    changeFile(file) {
      var isJPGCon = file.name.split(".");
      isJPGCon = isJPGCon[isJPGCon.length - 1];
      var isJPG = false;
      var st = [
        "jpg",
        "jpeg",
        "png",
        "gif",
        "bmp",
        "pdf",
        "JPG",
        "JPEG",
        "PBG",
        "GIF",
        "BMP",
        "PDF"
      ];
      if (st.indexOf(isJPGCon) < 0) {
        this.$message.error("头像仅限图片格式");
      } else {
        isJPG = true;
      }
      const isLt2M = file.size / 1024 < 100;
      if (!isLt2M) {
        if (isJPG) {
          this.$message.error("图片大小不能超过 100KB!");
        }
      }
      return isJPG && isLt2M;
    },
    handleChange(res) {
      if (res.success) {
        this.base_info.avatar = res.avatar;
      } else {
        this.$message.error("修改失败，请稍后再试");
      }
    },
    // 编辑相关字段
    editName() {
      this.nameRead = false;
      this.$nextTick(() => this.$refs.nameValue.focus());
    },
    editEmail() {
      this.emailRead = false;
      this.$nextTick(() => this.$refs.emailValue.focus());
    },
    editPhone() {
      this.phoneRead = false;
      this.$nextTick(() => this.$refs.phoneValue.focus());
    },
    // 查看/修改用户基本信息
    checkBaseInfo() {
      this.baseInfoDrawer = true;
    },
    sureSaveInfo() {
      if (this.base_info.nickname === "") {
        this.$message.error("用户名不能为空");
        return false;
      }
      let sendD = {
        nickname: this.base_info.nickname,
        email: this.base_info.email,
        phone: this.base_info.phone
      };
      saveInfo(sendD)
        .then(response => {
          if (response.data.success) {
            this.baseInfoDrawer = false;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    // 查看我的创建
    // 点击我的创建
    openCreateDrawer() {
      this.createTitle = 0;
      this.createDrawer = true;
      this.checkFirst();
    },
    // 任务列表
    checkFirst() {
      let sendD = {
        searchParam: this.createSearch,
        page: this.createPage,
        pageSize: this.createSize
      };
      getOwnTasksList(sendD)
        .then(response => {
          this.createLoading = false;
          if (response.data.success) {
            this.createTasksList = response.data.data.data;
            this.createTotalSize = response.data.data.total;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.createLoading = false;
          this.$message.error(error.message);
        });
    },
    // 漏洞库
    checkSecond() {
      let sendD = {
        searchParam: this.createSearch,
        page: this.createPage,
        pageSize: this.createSize
      };
      getOwnLeaksList(sendD)
        .then(response => {
          this.createLoading = false;
          if (response.data.success) {
            this.createLeaksList = response.data.data.data;
            this.createTotalSize = response.data.data.total;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.createLoading = false;
          this.$message.error(error.message);
        });
    },
    // 社工库列表
    checkThird() {
      let sendD = {
        searchParam: this.createSearch,
        page: this.createPage,
        pageSize: this.createSize
      };
      getOwnSocialList(sendD)
        .then(response => {
          this.createLoading = false;
          if (response.data.success) {
            this.createSocialList = response.data.data.data;
            this.createTotalSize = response.data.data.total;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.createLoading = false;
          this.$message.error(error.message);
        });
    },
    // 技战法列表
    checkFourth() {
      let sendD = {
        search: this.createSearch,
        page: this.createPage,
        pageSize: this.createSize
      };
      getOwnTequeList(sendD)
        .then(response => {
          this.createLoading = false;
          if (response.data.success) {
            this.createTequeList = response.data.data;
            this.createTotalSize = response.data.total;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.createLoading = false;
          this.$message.error(error.message);
        });
    },
    // 用户列表
    checkFifth() {
      let sendD = {
        search: this.createSearch,
        page: this.createPage,
        pageSize: this.createSize
      };
      getOwnUsersList(sendD)
        .then(response => {
          this.createLoading = false;
          if (response.data.success) {
            this.createUsersList = response.data.data;
            this.createTotalSize = response.data.total;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.createLoading = false;
          this.$message.error(error.message);
        });
    },
    topChange() {
      this.createSearch = "";
      this.createPage = 1;
      this.createSize = 10;
      this.handleClick();
    },
    handleClick() {
      this.createLoading = true;
      switch (this.createTitle) {
        case 0:
          this.checkFirst();
          break;
        case 1:
          this.checkSecond();
          break;
        case 2:
          this.checkThird();
          break;
        case 3:
          this.checkFourth();
          break;
        case 4:
          this.checkFifth();
      }
    },
    // 关键词搜索
    enterCreateCheck(val) {
      if (val == "") {
        this.createPage = 1;
        this.createSize = 10;
        this.handleClick();
      }
    },
    checkCreateResult() {
      if (this.createSearch != "") {
        this.createPage = 1;
        this.handleClick();
      }
    },
    // 分页
    createSizeChange(val) {
      this.createSize = val;
      this.handleClick();
    },
    createCurrentChange(val) {
      this.createPage = val;
      this.handleClick();
    },

    // 任务审核
    getTasksRev() {
      this.createTitle = 0;
      this.taskReviewDrawer = true;
      this.taskReviewLoading = true;
      let sendD = {
        searchParam: this.trSearch,
        page: this.trPage,
        pageSize: this.trSize
      };
      getTaskReviewList(sendD)
        .then(response => {
          this.taskReviewLoading = false;
          if (response.data.success) {
            this.taskReviewList = response.data.data.data;
            this.trTotalSize = response.data.data.total;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.taskReviewLoading = false;
          this.$message.error(error.message);
        });
    },
    // 关键词搜索
    enterTrCheck(val) {
      if (val == "") {
        this.trPage = 1;
        this.trSize = 10;
        this.getTasksRev();
      }
    },
    checkTrResult() {
      if (this.trSearch != "") {
        this.trPage = 1;
        this.getTasksRev();
      }
    },
    // 分页
    trSizeChange(val) {
      this.trSize = val;
      this.getTasksRev();
    },
    trCurrentChange(val) {
      this.trPage = val;
      this.getTasksRev();
    },

    // 详情获取
    checkDetail(id) {
      this.taskId = id;
      this.taskDetailDrawer = true;
      this.detailGetLoading = true;
      this.checkDetails();
    },
    // 详情信息获取
    checkDetails() {
      if (this.createTitle === 0) {
        taskDetails(this.taskId)
          .then(response => {
            this.detailGetLoading = false;
            if (response.data.success) {
              this.taskDetail = response.data.data;
            } else {
              this.$message.warning(response.data.info);
            }
          })
          .catch(error => {
            this.detailGetLoading = false;
            this.$message.error(error.message);
          });
      }
      if (this.createTitle === 3) {
        getOwnTequeDetail(this.taskId)
          .then(response => {
            this.detailGetLoading = false;
            if (response.data.success) {
              this.skill = response.data.data;
            } else {
              this.$message.warning(response.data.info);
            }
          })
          .catch(error => {
            this.detailGetLoading = false;
            this.$message.error(error.message);
          });
      }
    },
    // 删除任务
    delSinLeak(row) {
      this.taskId = row.id;
      this.delCon = row.name;
      this.delVisible = true;
    },
    sureDelLink() {
      this.loadSureDel = true;
      let sendD = {
        id: this.taskId
      };
      taskDel(sendD)
        .then(response => {
          this.loadSureDel = false;
          this.delVisible = false;
          if (response.data.success) {
            if (this.createTasksList.length === 1) {
              this.page = 1;
            }
            this.checkFirst();
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.loadSureDel = false;
          this.delVisible = false;
          this.$message.error(error.message);
        });
    },
    // 任务审核信息获取
    reviewSinTask(row) {
      this.reviewDrawer = true;
      getTaskReview(row.id)
        .then(response => {
          if (response.data.success) {
            this.reviewForm = response.data.data;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    // 任务审核按钮点击
    sureReviewTask() {
      if (this.reviewForm.radio === 1 && this.reviewForm.reason === "") {
        this.$message.error("请输入拒绝理由");
        return false;
      }
      this.loadSureReview = true;
      var sendD = {
        id: this.reviewForm.id,
        radio: this.reviewForm.radio,
        reason: this.reviewForm.reason
      };
      sureTaskReview(sendD)
        .then(response => {
          this.loadSureReview = false;
          this.reviewDrawer = false;
          if (response.data.success) {
            this.getTasksRev();
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.loadSureReview = false;
          this.reviewDrawer = false;
          this.$message.error(error.message);
        });
    },
    // 任务评分
    taskRvScore() {
      this.checkTaskIs = true;
      this.taskScoreLoading = true;
      this.taskScoreDrawer = true;
      getTaskScoreList()
        .then(response => {
          this.taskScoreLoading = false;
          if (response.data.success) {
            this.scoreList = response.data.data;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.taskScoreLoading = false;
          this.$message.error(error.message);
        });
    },
    // 查看单个任务&分配分数
    checkSinTask(item) {
      this.checkTaskIs = false;
      this.taskName = item.name;
      this.taskId = item.id;
      this.csTaskTotalScore = item.totalScore;
      let sin = Math.round(this.csTaskTotalScore / 5);
      this.sliderMarks = {
        0: {
          style: {
            color: "#2a2c33"
          },
          label: this.$createElement("strong", 0)
        },
        [sin * 1]: {
          style: {
            color: "#999"
          },
          label: sin * 1
        },
        [sin * 2]: {
          style: {
            color: "#999"
          },
          label: sin * 2
        },
        [sin * 3]: {
          style: {
            color: "#999"
          },
          label: sin * 3
        },
        [sin * 4]: {
          style: {
            color: "#999"
          },
          label: sin * 4
        },
        [this.csTaskTotalScore]: {
          style: {
            color: "#2a2c33"
          },
          label: this.$createElement("strong", this.csTaskTotalScore)
        }
      };
      this.getOrgList(item.id);
    },
    // 获取单个任务组织列表
    getOrgList(id) {
      getTaskScoreOrgList(id)
        .then(response => {
          if (response.data.success) {
            this.sinTaskBelong = response.data.data;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    // 点击修改
    changeOrgScore(sin) {
      this.sinOrg = sin;
      this.changeSvisible = true;
    },
    // 点击确认按钮
    sureChangeS() {
      this.scsBtnLoading = true;
      var sendD = {
        org_id: this.sinOrg.id,
        task_id: this.taskId,
        type: this.sinOrg.type,
        score: this.sinOrg.score
      };
      sureChangeScore(sendD)
        .then(response => {
          this.changeSvisible = false;
          this.scsBtnLoading = false;
          if (response.data.success) {
            this.getOrgList(this.taskId);
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.changeSvisible = false;
          this.scsBtnLoading = false;
          this.$message.error(error.message);
        });
    },
    // 修改密码
    changeOwnPsd() {
      if (this.$refs["addEditForm"] !== undefined) {
        this.$refs["addEditForm"].resetFields();
      }
      this.addEditForm = {
        oldPsd: "",
        newPsd: "",
        reNewPsd: ""
      };
      this.changePsdDrawer = true;
    },
    sureChangePsd() {
      this.$refs["addEditForm"].validate(valid => {
        if (valid) {
          let t = this.addEditForm;
          if (t.reNewPsd !== t.newPsd) {
            this.$message.error("两次密码输入不一致,请重新输入");
            return false;
          }
          this.loadSureChange = true;
          // var oldPsd = encrypt(t.oldPsd),
          // newPsd = encrypt(t.newPsd);
          var sendD = {
            oldPsd: t.oldPsd,
            newPsd: t.newPsd
          };
          changePsd(sendD)
            .then(response => {
              if (response.data.success) {
                this.$router.push("/login");
              } else {
                this.$message.warning(response.data.info);
              }
            })
            .catch(error => {
              this.$message.error(error.message);
            });
        } else {
          this.$message.error("请完善各项内容");
        }
      });
    },
    // 退出
    exitLog() {
      this.$store.dispatch("LogOut").then(() => {
        this.$router.push("/login");
      });
    }
  }
};
</script>

<style rel="stylesheet/scss" lang="scss">
.layout {
  position: relative;
  width: 100%;
  height: 100%;
  background: #ebeef4;
  .topsidebar {
    background: #ebeef4;
    box-shadow: 0 0 20px rgba($color: #f2f5f7, $alpha: 0.2);
    height: 70px;
    line-height: 70px;
    i {
      font-size: 20px;
    }
    .logo {
      height: 70px;
      line-height: 70px;
      padding-left: 20px;
      text-align: center;
      overflow: hidden;
      float: left;
      img {
        vertical-align: middle;
      }
    }
    .collapse_btn {
      height: 70px;
      margin-left: 15px;
      cursor: pointer;
      float: left;
      i {
        color: #1a155d;
      }
    }
    .side_left {
      padding-top: 15px;
      float: right;
      transition: width 0.28s;
      margin-right: 20px;
      .sidebar_menu {
        height: 40px;
      }
      .firstSlide {
        .el-menu {
          height: 100%;
          background: transparent;
          border: 0;
          .el-menu-item {
            width: 100px;
            margin-right: 20px;
            text-align: center;
            height: 40px;
            line-height: 40px;
            border-radius: 20px;
            color: #757677;
            padding: 0;
            border: 0;
          }
          .el-menu-item:hover {
            color: #36475e;
          }
          .el-menu-item:focus {
            color: #36475e;
          }
          .el-menu-item.is-active {
            background: linear-gradient(to right, #5861f0, #3b44db);
            background: -webkit-linear-gradient(to right, #5861f0, #3b44db);
            background: -moz-linear-gradient(to right, #5861f0, #3b44db);
            -moz-box-shadow: 0px 5px 10px 2px rgba($color: #4e58e7, $alpha: 0.5);
            -webkit-box-shadow: 0px 5px 10px 2px
              rgba($color: #4e58e7, $alpha: 0.5);
            box-shadow: 0px 5px 10px 2px rgba($color: #4e58e7, $alpha: 0.5);
          }
        }
      }
    }
    .right_mod {
      float: right;
      height: 70px;
      color: #c70d0d;
      .el-dropdown {
        .el-dropdown-single {
          outline: none;
        }
      }
      img {
        width: 40px;
        height: 40px;
        border-radius: 40px;
        float: left;
        margin: 15px 10px 0 0;
        border: 2px solid #fff;
      }
      span {
        float: left;
        margin-right: 30px;
        cursor: pointer;
        i {
          display: inline-block;
          vertical-align: middle;
        }
        img {
          width: 30px;
          height: 30px;
          border-radius: 50%;
          margin-top: 17px;
          display: inline-block;
        }
      }
    }
  }
  .mainCon {
    height: calc(100% - 70px);
    width: 100%;
    padding: 20px;
    .app-main {
      width: 100%;
      height: 100%;
      box-shadow: 0px 0px 15px #e0e4ea;
      border-radius: 20px;
    }
  }
  .sinLeakDe {
    height: 100%;
    padding: 50px 70px;
    .leftCon {
      height: 100%;
      & > div {
        padding-left: 10px;
      }
      .userInfoOne {
        margin-bottom: 70px;
        overflow: hidden;
        height: 70px;
        line-height: 70px;
        img {
          cursor: pointer;
          width: 60px;
          height: 60px;
          border-radius: 60px;
          margin-right: 20px;
          float: left;
          -moz-box-shadow: 0px 5px 15px 5px #c4d7f1;
          -webkit-box-shadow: 0px 5px 15px 5px #c4d7f1;
          box-shadow: 0px 5px 15px 5px #c4d7f1;
          &:hover {
            & + .hideShelter {
              display: block;
            }
          }
        }
        .hideShelter {
          cursor: pointer;
          position: absolute;
          z-index: 3;
          width: 60px;
          height: 60px;
          border-radius: 60px;
          background: rgba(0, 0, 0, 0.6);
          color: #fff;
          text-align: center;
          line-height: 60px;
          display: none;
          &:hover {
            display: block;
          }
        }
      }
      .nameInput {
        width: 300px;
        .el-input__inner {
          padding-left: 0;
          color: #2a2c33;
          font-size: 26px;
          font-family: "strong";
          border: 0;
        }
        .el-input__suffix {
          line-height: 64px;
          cursor: pointer;
          .el-input__suffix-inner {
            i {
              color: #539cff;
            }
          }
        }
      }
      .emailInput,
      .phoneInput {
        width: 300px;
        .el-input__inner {
          font-size: 18px;
        }
        .el-input__suffix {
          line-height: 44px;
        }
      }
      .userInfoTwo,
      .userInfoThree {
        margin-bottom: 40px;
        p {
          color: #7f8085;
          line-height: 30px;
        }
      }
      .userInfoFour {
        margin-bottom: 30px;
        .title {
          display: inline-block;
          color: #7f8085;
          margin-right: 30px;
        }
      }
      .userInfoFive {
        height: calc(100% - 460px);
        overflow: hidden;
        .title {
          float: left;
          color: #7f8085;
          margin-right: 30px;
        }
        .fiveRightCon {
          height: 100%;
          width: calc(100% - 90px);
          float: left;
          &::-webkit-scrollbar {
            width: 5px;
          }
          ul {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            li {
              width: 48%;
              padding: 20px;
              border-radius: 20px;
              background: #f0f2f5;
              margin-bottom: 10px;
              .orgTitle {
                color: #333;
                font-size: 17px;
                font-weight: bold;
                margin-bottom: 30px;
              }
              .sinTag {
                padding: 5px 10px;
                color: #fff;
                background: #539cff;
                border-radius: 36px;
              }
            }
          }
        }
      }
      .btnChange {
        width: 300px;
        margin-left: 80px;
        margin-top: 20px;
        border-radius: 40px;
        background-image: linear-gradient(to right, #56a5fe, #3e7bec);
      }
    }
    .rightTop {
      padding: 120px 30px 20px 0px;
      overflow: hidden;
      .mountView {
        float: left;
        margin-right: 50px;
        .colorDif {
          color: #539cff;
          font-size: 36px;
          font-family: "strong";
        }
        p {
          color: #7f8085;
        }
      }
    }
    .rightMain {
      height: calc(100% - 200px);
      .timeContent {
        padding-left: 1px;
        height: calc(100% - 70px);
        .el-timeline-item {
          padding-bottom: 50px;
          .timeTitle {
            color: #696e80;
            .ttl {
              display: inline-block;
              width: 150px;
              font-size: 17px;
              font-weight: bold;
              overflow: hidden;
              white-space: nowrap;
              text-overflow: ellipsis;
            }
            .ttr {
              display: inline-block;
              margin-left: 60px;
              color: #539cff;
              font-family: "strong";
              font-size: 18px;
            }
          }
          .el-timeline-item__timestamp {
            color: #636469;
            font-family: "light";
          }
        }
      }
      &::-webkit-scrollbar {
        width: 5px;
      }
    }
    .dTop {
      font-size: 34px;
      margin-bottom: 40px;
    }
    .el-radio-group {
      .el-radio-button {
        &:focus {
          box-shadow: none !important;
          outline: none !important;
        }
      }
    }
    .searchBoxPos {
      z-index: 5;
      width: 10%;
      position: absolute;
      right: 80px;
      top: 130px;
    }
    .pageShowStyle {
      position: absolute;
      right: 80px;
      bottom: 0;
      z-index: 5;
    }
    .proTable {
      height: calc(100% - 160px);
    }
    .personalScore {
      height: calc(100% - 80px);
      // display: flex;
      // justify-content: space-between;
      // flex-wrap: wrap;
      .sinScore {
        float: left;
        width: 23%;
        height: 200px;
        padding: 20px;
        border-radius: 10px;
        margin-right: 2%;
        cursor: pointer;
        -moz-box-shadow: 0px 7px 5px 3px #ebedf0;
        -webkit-box-shadow: 0px 7px 5px 3px #ebedf0;
        box-shadow: 0px 7px 5px 3px #ebedf0;
        &:hover {
          -moz-box-shadow: 0px 5px 10px 5px #d0e4ff;
          -webkit-box-shadow: 0px 5px 10px 5px #d0e4ff;
          box-shadow: 0px 5px 10px 5px #d0e4ff;
        }
        .title {
          font-weight: bold;
          font-size: 20px;
          color: #2a2c33;
        }
        .des {
          height: 60px;
          margin: 25px 0;
          color: #9c9da0;
          overflow: hidden;
          text-overflow: ellipsis;
          display: -webkit-box;
          -webkit-line-clamp: 3;
          -webkit-box-orient: vertical;
        }
        .time {
          color: #9c9da0;
          span {
            padding-left: 30px;
            font-family: "strong";
            color: #2a2c33;
          }
        }
      }
    }
    .taskUserSty {
      height: calc(100% - 80px);
      .taskUserAllSty {
        margin-bottom: 20px;
        overflow: hidden;
        .iconfont {
          font-size: 20px;
          display: block;
          float: left;
          cursor: pointer;
          color: #687079;
          margin: 0 15px 0 5px;
        }
        .el-breadcrumb {
          padding-top: 5px;
          .el-breadcrumb__item:nth-child(2) {
            .el-breadcrumb__inner {
              font-weight: bold;
              color: #539cff;
            }
          }
        }
      }
    }
  }
  .cPsdBox {
    height: 100%;
    padding: 50px 70px;
    .dTop {
      font-size: 34px;
      margin-bottom: 60px;
      span {
        color: #f66;
        font-size: 14px;
      }
    }
    .cpsdBtn {
      width: 400px;
      margin-left: 80px;
      margin-top: 20px;
      border-radius: 40px;
      background-image: linear-gradient(to right, #56a5fe, #3e7bec);
    }
    .el-form {
      .el-form-item {
        margin-bottom: 60px;
        .el-form-item__label {
          color: #636469;
          &:before {
            display: none;
          }
        }
      }
    }
  }
}
</style>
