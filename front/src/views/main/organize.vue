<template>
  <div
    class="orgmanage"
    v-loading="listLoading"
    element-loading-text="数据加载中"
    element-loading-background="rgba(0, 0, 0, 0.6)"
  >
    <div class="mainTop">
      <el-row style="margin-bottom: 8px;" :gutter="20">
        <el-col :span="14">
          <span class="englishView">组织管理</span>
          <img src="@/assets/img/organizational_management.png" alt="" />
        </el-col>
        <el-col :span="10" class="btns" v-show="showMain">
          <!-- <el-button class="importOrg" @click="importFile">导入</el-button> -->
          <el-button class="importOrg" @click="addOrg" v-if="adminUser"
            >新增</el-button
          >
          <!-- <el-button class="exportOrg" @click="importFile">导出</el-button> -->
        </el-col>
      </el-row>
    </div>
    <div class="mainList">
      <div class="teams" :class="showMain ? 'show' : 'noshow'" v-if="showMain">
        <el-tree
          ref="tree"
          node-key="id"
          :data="treeData"
          :props="treeProps"
          class="scrollStyle treeSty"
          :default-expand-all="true"
          :highlight-current="true"
          @node-click="nodeClick"
        ></el-tree>
        <div class="srcollCol scrollStyle">
          <div
            class="homeSecond"
            v-for="(item, index) in currentOrg"
            :key="index"
          >
            <div
              class="sinHScon"
              title="点击进入组员列表页面"
              @click="checkMemberList(item)"
            >
              <div class="shsTwo">
                <span>{{ item.name }}</span>
              </div>
              <div class="shsOne">
                <div class="sin">
                  <span class="colorDif">{{ item.score }}</span>
                  <p class="totalNum">组织得分</p>
                </div>
                <div class="sin">
                  <span class="colorDif">{{ item.task_count }}</span>
                  <p class="totalNum">任务数量</p>
                </div>
                <div class="sin">
                  <span class="colorDif">{{ item.user_count }}</span>
                  <p class="totalNum">组员数量</p>
                </div>
              </div>
              <div class="shsThree">
                <span>{{ item.create_time }}</span>
                <div class="btns" v-if="adminUser">
                  <el-button
                    type="primary"
                    icon="el-icon-edit"
                    circle
                    @click.native.stop="editOrg(item)"
                  ></el-button>
                  <!-- <el-button
                    type="danger"
                    icon="el-icon-delete"
                    circle
                  ></el-button> -->
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="members" :class="!showMain ? 'show' : 'noshow'" v-else>
        <div class="leaderTab">
          <i class="iconfont icon-fanhui1 tabIcon" @click="gebackOrg"></i>
          <span>组织列表 / </span>
          <span>组员列表</span>
        </div>
        <el-table
          :data="memberListData"
          v-if="noDataIs"
          border
          class="proTable scrollStyle"
          style="width: 100%;height:100%"
        >
          <el-table-column prop="name" label="组员姓名" show-overflow-tooltip>
          </el-table-column>
          <el-table-column prop="username" label="用户名" show-overflow-tooltip>
          </el-table-column>
          <el-table-column prop="email" label="电子邮箱" show-overflow-tooltip>
          </el-table-column>
          <el-table-column
            prop="phone"
            label="联系电话"
            show-overflow-tooltip
          ></el-table-column>
          <el-table-column
            prop="missionCount"
            label="任务数量"
          ></el-table-column>
          <el-table-column prop="totalScore" label="个人总分"></el-table-column>
          <el-table-column
            label="操作"
            :width="adminUser ? 200 : 100"
            fixed="right"
          >
            <template slot-scope="scope">
              <el-button
                title="详情"
                class="sinProBtn detailBtn"
                @click="checkDetail(scope.row)"
              >
                详情
              </el-button>
              <el-button
                v-if="adminUser"
                title="删除"
                class="sinProBtn delBtn"
                @click="delSinLeak(scope.row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="pageShowStyle" v-if="noDataIs">
          <el-pagination
            class="pageShowView"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="page"
            :page-sizes="[10, 25, 50, 100]"
            :page-size="page_size"
            layout="total, sizes, prev, pager, next, jumper"
            :total="totalSize"
          >
          </el-pagination>
        </div>
        <div class="noDataIs" v-if="!noDataIs">
          <img src="@/assets/img/noData.png" alt="" />
          <p>暂无数据</p>
        </div>
      </div>
    </div>
    <!--新增链路-->
    <el-dialog
      :visible.sync="addLinkVisible"
      class="addDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
      top="6%"
    >
      <div class="addMain">
        <div class="addTopbar" v-if="addNewLink">
          <span class="englishView">新建组织</span>
          <img src="@/assets/img/new_org.png" alt="" />
        </div>
        <div class="addTopbar" v-else>
          <span class="englishView">编辑组织</span>
          <img src="@/assets/img/edit_org.png" alt="" />
        </div>
        <el-form
          :model="linkForm"
          status-icon
          :rules="rulesLink"
          ref="linksforms"
          label-width="100px"
          class="weaponForm"
        >
          <el-form-item label="组织名称" prop="name" class="fifty">
            <el-input v-model="linkForm.name"></el-input>
          </el-form-item>
          <el-form-item label="选择人员" class="fifty">
            <el-select
              style="width:100%;"
              v-model="linkForm.user_list"
              multiple
              placeholder="请选择"
            >
              <el-option
                v-for="item in userList"
                :key="item.id"
                :label="item.username"
                :value="item.id"
              >
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer" class="addFooter">
        <el-button
          @click="addSureLink"
          type="primary"
          class="sureBtn"
          :loading="addLinkLoad"
          >{{ addNewLink ? "新增组织" : "编辑组织" }}</el-button
        >
      </div>
    </el-dialog>
    <!--删除确认模态框-->
    <el-dialog
      :visible.sync="delVisible"
      width="25%"
      top="15%"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <p class="contentPsty">
        是否确认移除此组员?
        <!-- <span style="font-weight:600;padding-left:15px;">{{
          delCon
        }}</span
        > -->
      </p>
      <div slot="footer">
        <el-button
          @click="sureDelLink"
          class="btnSure"
          type="warning"
          :loading="loadSureDel"
          >确 定</el-button
        >
        <el-button type="info" class="btnCancle" @click="delVisible = false"
          >放 弃</el-button
        >
      </div>
    </el-dialog>
    <!--任务详情模抽屉-->
    <el-drawer
      :visible.sync="taskDetailDrawer"
      class="missionDetailDrawer"
      size="80%"
      :withHeader="false"
      :close-on-press-escape="false"
    >
      <div
        style="height:100%;"
        v-loading="detailGetLoading"
        element-loading-text="数据加载中"
        element-loading-background="rgba(0, 0, 0, 0.6)"
      >
        <div class="allDetailBox">
          <div class="addModalTop">
            <span class="englishView">组员信息</span>
            <img src="@/assets/img/member_information.png" alt="" />
          </div>
          <div class="mainBox">
            <el-row :gutter="20" style="height:100%;">
              <el-col :span="12" style="height:100%;">
                <span>{{ taskDetail.name }}</span>
                <el-form
                  :model="ruleForm"
                  status-icon
                  :rules="rules"
                  ref="ruleForm"
                  label-width="100px"
                  class="demo-ruleForm"
                >
                  <el-form-item label="电子邮箱" prop="email">
                    <el-input
                      v-model="ruleForm.email"
                      autocomplete="off"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="联系电话" prop="phone">
                    <el-input
                      v-model="ruleForm.phone"
                      autocomplete="off"
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="任务数量" prop="missionCount">
                    <el-input
                      readonly
                      v-model.number="ruleForm.missionCount"
                    ></el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button
                      type="primary"
                      class="suerBtnSaveChange"
                      :loading="saveLoading"
                      @click="submitForm('ruleForm')"
                      >保存修改</el-button
                    >
                  </el-form-item>
                </el-form>
              </el-col>
              <el-col :span="12" style="height:100%;">
                <count-to
                  :start-val="0"
                  :end-val="taskDetail.totalScore"
                  :duration="2800"
                  style="color:#539cff;"
                  class="numCon"
                />
                <span style="color:#b9bbc4;font-size:17px;font-weight:normal"
                  >任务得分</span
                >
                <div class="timeLine scrollStyle">
                  <el-timeline :reverse="false">
                    <el-timeline-item
                      v-for="(activity, index) in activities"
                      :key="index"
                      :type="index === 0 ? 'success' : ''"
                      :icon="index === 0 ? 'el-icon-star-on' : ''"
                      :color="index === 0 ? '#539cff' : ''"
                      :size="index === 0 ? 'large' : 'normal'"
                      :timestamp="activity.timestamp"
                    >
                      <span class="spanOne">{{ activity.content }}</span>
                      <span class="spanTwo">+{{ activity.missionScore }}</span>
                    </el-timeline-item>
                  </el-timeline>
                </div>
              </el-col>
            </el-row>
          </div>
          <div @click="taskDetailDrawer = false" class="closeBtn">
            <i class="el-icon-arrow-right"></i>
          </div>
        </div>
      </div>
    </el-drawer>
  </div>
</template>
<script>
import CountTo from "vue-count-to";
import {
  memberDel,
  organizationList,
  orgAdd,
  orgEdit,
  memberList,
  getOrgsList,
  userList,
  // memberDetail,
  changeMember
} from "@/api/organization";
export default {
  name: "taskList",
  components: {
    CountTo
  },
  data() {
    var validateTel = (rule, value, callback) => {
      const reg = /^1[3|4|5|7|8][0-9]\d{8}$/;
      if (value === "") {
        callback(new Error("联系电话不能为空"));
      } else if (reg.test(value)) {
        callback();
      } else {
        callback(new Error("请输入正确的11位电话号码!"));
      }
    };
    return {
      treeData: [
        {
          name: "四川省",
          children: []
        }
      ],
      showMain: true,
      currentOrg: [],
      treeProps: {
        children: "children",
        label: "name"
      },
      curMember: {},
      memberListData: [],
      listLoading: false,
      search: "",
      page: 1,
      page_size: 10,
      totalSize: 0,
      delVisible: false,
      taskDetailDrawer: false,
      taskDetail: {},
      detailGetLoading: false,
      loadSureDel: false,
      delCon: "",
      leakId: [],
      noDataIs: true,
      activities: [],
      ruleForm: {
        email: "",
        phone: "",
        missionCount: ""
      },
      rules: {
        email: [
          { required: true, message: "请输入邮箱地址", trigger: "blur" },
          {
            type: "email",
            message: "请输入正确的邮箱地址",
            trigger: ["blur", "change"]
          }
        ],
        phone: [{ validator: validateTel, trigger: "blur" }]
      },
      saveLoading: false,
      org_id: null,
      addLinkLoad: false,
      addLinkVisible: false,
      linkForm: {
        id: "",
        name: "",
        user_list: []
      },
      rulesLink: {
        name: [{ required: true, message: "请输入组织名称", trigger: "blur" }]
      },
      userList: [],
      addNewLink: true,
      adminUser: null
    };
  },
  mounted() {
    this.adminUser = this.$store.getters.roles === "admin" ? true : false;
  },
  created() {
    this.getOrgList();
    this.getAddUsers();
  },
  methods: {
    getAddUsers() {
      const sd = {
        page: 1,
        page_size: 9999,
        search: ""
      };
      userList(sd)
        .then(response => {
          if (response.data.success) {
            this.userList = response.data.data;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    // 获取组织列表
    getOrgList() {
      this.listLoading = true;
      organizationList()
        .then(response => {
          this.listLoading = false;
          if (response.data.success) {
            this.treeData[0].children = response.data.data.data;
            if (response.data.data.data.length > 0) {
              var id = response.data.data.data[0].id;
              this.org_id = id;
              this.$nextTick(() => {
                this.nodeClick(id);
              });
            }
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.listLoading = false;
          this.$message.error(error.message);
        });
    },
    // 树节点点击事件
    nodeClick(val) {
      if (val.hasOwnProperty("children")) {
        this.$refs.tree.setCurrentKey(this.org_id);
        return;
      }
      var data = { id: val };
      if (val.hasOwnProperty("id")) {
        data = {
          id: val.id
        };
      }
      this.org_id = data.id;
      getOrgsList(data)
        .then(res => {
          if (res.data.success) {
            this.$refs.tree.setCurrentKey(this.org_id);
            this.currentOrg = res.data.data.data;
          } else {
            this.$message.warning(res.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    // 组织新增
    addOrg() {
      const f = this.$refs["linksforms"];
      if (f != undefined && f != null) {
        this.$refs["linksforms"].resetFields();
      }
      const tre = this.$refs["trees"];
      if (tre != undefined && tre != null) {
        this.$refs.trees.setChecked(this.linkForm.group, false);
      }
      this.linkForm = {
        id: "",
        name: "",
        user_list: ""
      };
      this.addNewLink = true;
      this.addLinkVisible = true;
    },
    addSureLink() {
      this.$refs["linksforms"].validate(valid => {
        if (valid) {
          if (this.linkForm.user_list.length === 0) {
            this.$message.error("请选择组织参与人员");
            return false;
          }
          this.addLinkLoad = true;
          let sendD = {
            name: this.linkForm.name,
            user_list: this.linkForm.user_list
          };
          if (this.addNewLink) {
            orgAdd(sendD)
              .then(response => {
                this.addLinkLoad = false;
                this.addLinkVisible = false;
                if (response.data.success) {
                  this.nodeClick(this.org_id);
                } else {
                  this.$message.warning(response.data.info);
                }
              })
              .catch(error => {
                this.addLinkLoad = false;
                this.addLinkVisible = false;
                this.$message.error(error.message);
              });
          } else {
            sendD.id = this.linkForm.id;
            orgEdit(sendD)
              .then(response => {
                this.addLinkLoad = false;
                this.addLinkVisible = false;
                if (response.data.success) {
                  this.nodeClick(this.org_id);
                } else {
                  this.$message.warning(response.data.info);
                }
              })
              .catch(error => {
                this.addLinkLoad = false;
                this.addLinkVisible = false;
                this.$message.error(error.message);
              });
          }
        } else {
          this.$message.error("请完善各项内容");
          return false;
        }
      });
    },
    // 组织编辑
    editOrg(row) {
      this.addNewLink = false;
      this.linkForm = {
        id: row.id,
        name: row.name,
        user_list: row.user_list
      };
      this.addLinkVisible = true;
      this.$nextTick(() => {
        this.$refs.tree.setChecked(row.group, true);
      });
    },
    // 切回组织列表
    gebackOrg() {
      this.showMain = true;
      this.nodeClick(this.org_id);
    },
    // 进入组员列表页面
    checkMemberList(val) {
      //todo
      this.showMain = false;
      this.curMember = {
        id: val.id,
        // searchParam: this.search,
        page: this.page,
        pageSize: this.page_size
      };
      this.getMemberList(this.curMember);
    },
    // 组员列表接口调用
    getMemberList(val) {
      this.listLoading = true;
      memberList(val)
        .then(res => {
          this.listLoading = false;
          if (res.data.success) {
            this.memberListData = res.data.data.data;
            this.totalSize = res.data.data.total;
            if (this.totalSize === 0) {
              this.noDataIs = false;
            } else {
              this.noDataIs = true;
            }
          } else {
            this.$message.warning(res.data.info);
          }
        })
        .catch(error => {
          this.listLoading = false;
          this.$message.error(error.message);
        });
    },
    // 查看组员详情
    checkDetail(val) {
      this.taskDetailDrawer = true;
      this.taskDetail = val;
      this.activities = val.missions;
      this.$set(this.ruleForm, "email", val.email);
      this.$set(this.ruleForm, "phone", val.phone);
      this.$set(this.ruleForm, "missionCount", val.missionCount);
      // this.detailGetLoading = true;
      // memberDetail(val)
      //   .then(res => {
      //     if (res.data.success) {
      //       this.detailGetLoading = false;
      //       this.taskDetail = res.data.data;
      //       this.activities = res.data.data.missions;
      //       this.$set(this.ruleForm, "email", res.data.data.email);
      //       this.$set(this.ruleForm, "phone", res.data.data.phone);
      //       this.$set(
      //         this.ruleForm,
      //         "missionCount",
      //         res.data.data.missionCount
      //       );
      //     } else {
      //       this.$message.warning(res.data.info);
      //     }
      //   })
      //   .catch(error => {
      //     this.detailGetLoading = false;
      //     this.$message.error(error.message);
      //   });
    },
    // 修改组员信息
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.saveLoading = true;
          var data = {
            id: this.taskDetail.id,
            email: this.ruleForm.email,
            phone: this.ruleForm.phone,
            missionCount: this.ruleForm.missionCount
          };
          changeMember(data)
            .then(res => {
              this.saveLoading = false;
              this.taskDetailDrawer = false;
              if (res.data.success) {
                this.$message.success("信息修改成功！");
                this.getMemberList(this.curMember);
              } else {
                this.$message.error(res.data.info);
              }
            })
            .catch(error => {
              this.saveLoading = false;
              this.$message.error(error.message);
            });
        } else {
          this.$message.warning("请输入正确信息后保存！");
          return false;
        }
      });
    },
    // 导入
    importFile() {
      var url =
        "http://192.168.8.243:8100/api/system/backup_down?id=" +
        this.org_id +
        "&token=" +
        this.$store.getters.token;
      var a = document.createElement("a");
      a.href = url;
      a.target = "_blank";
      var body = document.getElementsByTagName("body")[0];
      body.appendChild(a);
      a.click();
      body.removeChild(a);
    },
    // 分页
    handleSizeChange(val) {
      this.page_size = val;
      this.curMember.pageSize = val;
      this.getMemberList(this.curMember);
    },
    handleCurrentChange(val) {
      this.page = val;
      this.curMember.page = val;
      this.getMemberList(this.curMember);
    },
    // 删除任务
    delSinLeak(row) {
      this.leakId = row.id;
      // this.delCon = row.name;
      this.delVisible = true;
    },
    sureDelLink() {
      this.loadSureDel = true;
      var data = {
        group_id: this.curMember.id,
        user_id: this.leakId
      };
      memberDel(data)
        .then(response => {
          this.loadSureDel = false;
          this.delVisible = false;
          if (response.data.success) {
            this.getMemberList(this.curMember);
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.loadSureDel = false;
          this.delVisible = false;
          this.$message.error(error.message);
        });
    }
  }
};
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.orgmanage {
  height: 100%;
  padding: 28px 30px 20px;
  background: #fff;
  .mainTop {
    margin-bottom: 10px;
    .btns {
      text-align: right;
      .importOrg {
        background: #4786ff;
        color: #fdf1ed;
        &:hover {
          background: #82abf8;
          color: #f5f0ee;
        }
      }
      .exportOrg {
        margin: 0 20px;
        background: #2fd37c;
        color: #fdf1ed;
        &:hover {
          background: #4db57e;
          color: #f5f0ee;
        }
      }
    }
    .englishView {
      height: 30px;
      line-height: 30px;
      float: left;
      font-size: 28px;
      font-weight: 100;
      margin-right: 20px;
    }
    img {
      margin-top: 3px;
    }
  }
  .mainList {
    position: relative;
    width: 100%;
    height: calc(100% - 40px);
    .members {
      .leaderTab {
        width: 100%;
        height: 40px;
        line-height: 30px;
        display: inline-block;
        .tabIcon {
          font-size: 20px;
          display: block;
          float: left;
          cursor: pointer;
          color: #687079;
          margin: 0 15px 0 5px;
        }
        span {
          font-size: 15px;
        }
        span:nth-child(3) {
          font-weight: bold;
          color: #539cff;
        }
      }
    }
    .teams {
      position: absolute;
      height: 100%;
      width: 100%;
      .treeSty {
        height: 100%;
        float: left;
        margin-top: 15px;
        width: 120px;
      }
      .srcollCol {
        width: calc(100% - 120px);
        height: 100%;
        padding-left: 20px;
        float: left;
        &::-webkit-scrollbar {
          width: 6px;
        }
      }
      .homeSecond {
        height: 200px;
        width: 23%;
        min-width: 320px;
        display: inline-block;
        margin: 20px 15px 20px 13px;
        .sinHScon {
          height: 100%;
          padding: 10px;
          border-radius: 10px;
          background: #fff;
          -moz-box-shadow: 0px 0px 10px 2px #cbdefa;
          -webkit-box-shadow: 0px 0px 10px 2px #cbdefa;
          box-shadow: 0px 0px 10px 2px #cbdefa;
          cursor: pointer;
          transition: all 0.5s;
          &:hover {
            transform: scale(1.05, 1.05);
            -moz-box-shadow: 0px 0px 20px 5px #cbdefa;
            -webkit-box-shadow: 0px 0px 20px 5px #cbdefa;
            box-shadow: 0px 0px 20px 5px #cbdefa;
          }
          .shsTwo {
            img {
              vertical-align: middle;
            }
            span {
              display: inline-block;
              line-height: 60px;
              margin-left: 20px;
              font-size: 18px;
              color: #2a2c33;
              font-weight: bold;
            }
          }
          .shsThree {
            & > span {
              display: inline-block;
              line-height: 60px;
              margin-left: 20px;
              font-size: 15px;
              color: #383a41;
              font-family: "light";
            }
            .btns {
              width: calc(100% - 155px);
              float: right;
              text-align: right;
              line-height: 60px;
              padding-right: 20px;
            }
          }
          .shsOne {
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            .sin {
              text-align: center;
              .numCon,
              .colorDif {
                font-family: "strong";
                font-size: 30px;
                color: #2a2c33;
              }
              .colorDif {
                color: #539cff;
              }
              .totalNum {
                margin-top: 10px;
                font-size: 14px;
                color: #636469;
              }
              #roleCircle {
                width: 500px;
                height: 200px;
              }
            }
          }
        }
      }
    }
    .noshow {
      left: 0px;
      visibility: visible;
      opacity: 1;
      animation: hideAni 0.5s forwards;
    }
    @keyframes hideAni {
      to {
        opacity: 0;
        visibility: hidden;
        left: 100%;
      }
    }
    .show {
      opacity: 0;
      visibility: hidden;
      left: 100%;
      animation: showAni 0.5s forwards;
    }
    @keyframes showAni {
      to {
        left: 0px;
        visibility: visible;
        opacity: 1;
      }
    }
    .proTable {
      height: calc(100% - 68px);
    }
    .noDataIs {
      position: absolute;
      left: calc(50% - 64px);
      top: calc(50% - 184px);
      width: 128px;
      height: 148px;
      text-align: center;
      i {
        font-size: 100px;
        color: #3a88e7;
      }
    }
  }
  .missionDetailDrawer {
    .allDetailBox {
      .mainBox {
        width: 100%;
        height: calc(100% - 100px);
        margin-top: 60px;
        .timeLine {
          width: 100%;
          margin-top: 20px;
          padding: 0 10px;
          height: calc(100% - 80px);
          &::-webkit-scrollbar {
            width: 5px;
          }
          .spanOne {
            width: 150px;
            font-size: 18px;
            float: left;
            margin-right: 40px;
            color: #696e80;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
          }
          .spanTwo {
            font-size: 20px;
            display: inline-block;
            color: #539cff;
          }
        }
        span {
          font-size: 36px;
          font-weight: bold;
        }
      }
    }
  }
}
</style>
<style rel="stylesheet/scss" lang="scss">
.orgmanage {
  .mainTop {
    .btns {
      .el-button {
        width: 80px;
        height: 32px;
        text-align: center;
        line-height: 32px;
        border: 0;
        padding: 0;
        border-radius: 32px;
      }
    }
  }
  .mainList {
    .el-tree-node__content > .el-tree-node__expand-icon::before {
      content: "";
    }
    .el-tree-node > .el-tree-node__children {
      margin-top: 7px;
      .el-tree-node__label {
        width: 100%;
        display: block;
        text-align: center;
        font-size: 15px;
        font-weight: 100;
        text-overflow: ellipsis;
        white-space: none;
        white-space: nowrap;
        overflow: hidden;
        color: #636469;
      }
      .el-tree-node__content {
        padding-left: 0px !important;
        width: 110px;
      }
      .el-tree-node.is-current > .el-tree-node__content {
        padding-left: 0px !important;
        width: 110px;
        border-radius: 13px;
        background-color: #539cff;
        color: #fff;
        text-align: center;
        box-shadow: 2px 4px 7px #539cff;
        .el-tree-node__label {
          width: 110px;
          color: #fff;
          text-align: center;
        }
      }
    }
    .el-tree-node__content {
      margin-bottom: 20px;
      width: 110px;
      .el-tree-node__label {
        width: 100%;
        display: block;
        text-align: center;
        font-size: 24px;
        font-weight: 700;
        text-overflow: ellipsis;
        white-space: none;
        white-space: nowrap;
        overflow: hidden;
      }
    }
    .el-tree-node__content > .el-tree-node__expand-icon {
      padding: 0;
    }
    .el-table {
      overflow: auto;
      &:before {
        height: 0;
      }
      .el-progress-bar__inner {
        background-image: linear-gradient(to right, #56a5fe, #3e7bec);
      }
      .el-progress__text {
        font-family: "strong";
        color: #529bff;
      }
    }
    .buttons {
      .el-button {
        width: 120px;
        height: 32px;
        text-align: center;
        line-height: 32px;
        border: 0;
        padding: 0;
        border-radius: 32px;
      }
    }
  }
  .missionDetailDrawer {
    .allDetailBox {
      height: calc(100% - 20px);
      padding: 50px 70px;
      .addModalTop {
        margin-bottom: 40px;
        .englishView {
          height: 30px;
          line-height: 30px;
          float: left;
          font-size: 28px;
          font-weight: 100;
          margin-right: 20px;
        }
        img {
          margin-top: 3px;
        }
      }
      .timeLine {
        .el-timeline-item__timestamp {
          font-family: "strong";
        }
      }
      .el-button {
        width: 100%;
        height: 40px;
        text-align: center;
        line-height: 40px;
        border: 0;
        padding: 0;
        border-radius: 40px;
        margin-left: -40px;
        margin-top: 20px;
      }
      .el-form {
        height: 100%;
        width: 70%;
        margin: 50px 0;
        .el-form-item {
          margin-bottom: 30px;
          .el-form-item__label {
            text-align: left;
            &::before {
              display: none;
            }
          }
          .el-radio-group {
            .el-radio-button:first-child {
              .el-radio-button__inner {
                border-right: 0;
                border-radius: 36px 0 0 36px;
              }
            }
            .el-radio-button:nth-child(2) {
              .el-radio-button__inner {
                border-radius: 0 36px 36px 0;
              }
            }
          }
        }
        &.reviewFsty {
          .el-form-item {
            margin-bottom: 15px;
            .el-radio-group {
              .el-radio-button:first-child {
                box-shadow: none;
                .el-radio-button__inner {
                  border-right: 0;
                  &:hover {
                    color: #2fd37c;
                  }
                }
                &.is-active {
                  .el-radio-button__inner {
                    background: #2fd37c;
                    border-color: #2fd37c;
                    color: #fff;
                    &:hover {
                      color: #fff;
                    }
                  }
                }
              }
              .el-radio-button:nth-child(2) {
                box-shadow: none;
                .el-radio-button__inner {
                  &:hover {
                    color: #ef6b5d;
                  }
                }
                &.is-active {
                  .el-radio-button__inner {
                    background: #ef6b5d;
                    border-color: #ef6b5d;
                    color: #fff;
                    box-shadow: none;
                    &:hover {
                      color: #fff;
                    }
                  }
                }
              }
            }
          }
        }
        .leftModal {
          padding-right: 20px;
          height: 100%;
          &::-webkit-scrollbar {
            width: 5px;
          }
          .reviewMbox {
            background: transparent;
            padding: 0;
            border-radius: 0px;
            .joinUser {
              li {
                background: #f0f2f5;
                width: 48%;
              }
            }
          }
        }
        .reviewMbox {
          background: #dfe1e6;
          padding: 20px 20px 0;
          border-radius: 20px;
          .el-form-item {
            p {
              font-family: "strong";
              font-weight: 600;
            }
          }
          .joinUser {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            li {
              width: 24%;
              padding: 20px;
              border-radius: 20px;
              background: #fff;
              margin-bottom: 10px;
              .orgTitle {
                color: #333;
                font-size: 17px;
                font-weight: bold;
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
        .rightModal {
          height: 100%;
          &::-webkit-scrollbar {
            width: 5px;
          }
          .rmTop {
            ul {
              display: flex;
              justify-content: space-between;
              flex-wrap: wrap;
              li {
                width: 24%;
                text-align: center;
                div {
                  font-size: 38px;
                  font-family: "strong";
                  margin-bottom: 10px;
                }
                span {
                  color: #b9bbc4;
                }
              }
            }
          }
          .rmMiddle {
            padding-left: 30px;
            p {
              color: #46484e;
              margin: 60px 0 40px 0;
            }
            .el-progress {
              .el-progress-circle__path {
                stroke: #539cff !important;
                stroke-linecap: butt;
              }
              .el-progress__text {
                font-size: 30px !important;
                color: #1376fe;
                font-family: "stronger";
              }
            }
          }
          .rmBottom {
            margin-top: 30px;
            position: relative;
            .title {
              color: #fff;
              position: absolute;
              left: 120px;
              top: 110px;
              font-size: 26px;
              font-weight: bold;
            }
            .namePos {
              position: absolute;
              left: 120px;
              top: 150px;
              .username {
                margin: 30px 0;
                .spName {
                  display: inline-block;
                  width: 100px;
                  color: #d4f2d6;
                }
                .strongCon {
                  color: #fff;
                  font-family: "strong";
                }
              }
            }
          }
          .sinM {
            padding-right: 20px;
            .rmTop {
              margin-bottom: 30px;
              position: relative;
              .addNewModal,
              .delModal {
                position: absolute;
                color: #539cff;
                top: 5px;
                right: 0;
                font-size: 20px;
                cursor: pointer;
              }
              .delModal {
                color: #f55249;
              }
            }
            .sinModalBg {
              padding: 20px 20px 0;
              background: #f0f2f5;
              border-radius: 20px;
            }
          }
        }
      }
      .suerBtnSaveChange {
        margin-top: 60px;
        border-radius: 36px;
        background-image: linear-gradient(to right, #56a5fe, #3e7bec);
      }
    }
  }
}
</style>
