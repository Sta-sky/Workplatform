<template>
  <div
    class="userView"
    v-loading="listLoading"
    element-loading-text="数据加载中"
    element-loading-background="rgba(0, 0, 0, 0.6)"
  >
    <div class="mainTop">
      <el-row style="margin-bottom: 8px;" :gutter="20">
        <el-col :span="17">
          <span class="englishView">用户管理</span>
          <img src="@/assets/img/user_management.png" alt="" />
        </el-col>
        <el-col :span="3" style="height:42px;text-align:right">
          <el-button
            title="新增"
            type="primary"
            size="medium"
            v-if="$store.getters.roles === 'admin'"
            style="height:42px;padding:8px 20px;margin-left:10px;background-image: linear-gradient(to right, #56a5fe, #3e7bec);"
            icon="el-icon-circle-plus-outline"
            @click="addSinTask"
            round
            >新增</el-button
          >
        </el-col>
        <el-col :span="4">
          <el-input
            class="searchinput"
            placeholder="请输入搜索内容"
            @input="enterCheck"
            @keypress.enter.native="clickCheck"
            v-model="search"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="clickCheck"
            ></el-button>
          </el-input>
        </el-col>
      </el-row>
    </div>
    <div class="mainList">
      <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane
          label="用户列表"
          name="first"
          class="firstPane scrollStyle"
        >
          <el-table
            :data="userListData"
            v-if="noDataIs"
            border
            fit
            class="proTable scrollStyle"
            style="width: 100%;"
          >
            <el-table-column prop="name" label="用户姓名" show-overflow-tooltip>
            </el-table-column>
            <el-table-column
              prop="email"
              label="电子邮箱"
              show-overflow-tooltip
            >
            </el-table-column>
            <el-table-column
              prop="phone"
              label="联系电话"
              show-overflow-tooltip
            ></el-table-column>
            <el-table-column
              prop="task_count"
              label="任务数量"
            ></el-table-column>
            <el-table-column
              prop="user_permission"
              label="人员权限"
              width="150"
            >
              <template slot-scope="scope">
                <el-tag
                  style="text-align:center"
                  :type="scope.row.user_permission == 0 ? 'info' : 'danger'"
                  disable-transitions
                  >{{
                    scope.row.user_permission == 0 ? "普通用户" : "管理员"
                  }}</el-tag
                >
              </template>
            </el-table-column>
            <el-table-column
              label="操作"
              width="200"
              v-if="$store.getters.roles === 'admin'"
            >
              <template slot-scope="scope">
                <el-button
                  title="编辑"
                  class="sinProBtn editBtn"
                  @click="checkDetail(scope.row)"
                >
                  编辑
                </el-button>
                <el-button
                  title="删除"
                  class="sinProBtn delBtn"
                  @click="userapiDel(scope.row)"
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
        </el-tab-pane>
        <el-tab-pane
          label="信息收集账号列表"
          name="second"
          class="firstPane scrollStyle"
        >
          <el-table
            :data="accountListData"
            v-if="noDataIs"
            border
            fit
            class="proTable scrollStyle"
            style="width: 100%;"
          >
            <el-table-column
              prop="account"
              label="账户名"
              show-overflow-tooltip
            >
            </el-table-column>
            <el-table-column prop="key" label="KEY" show-overflow-tooltip>
            </el-table-column>
            <el-table-column
              prop="engine_type"
              label="分类"
              show-overflow-tooltip
            >
            </el-table-column>
            <el-table-column
              label="操作"
              width="200"
              v-if="$store.getters.roles === 'admin'"
            >
              <template slot-scope="scope">
                <el-button
                  title="编辑"
                  class="sinProBtn editBtn"
                  @click="checkDetail(scope.row)"
                >
                  编辑
                </el-button>
                <el-button
                  title="删除"
                  class="sinProBtn delBtn"
                  @click="userapiDel(scope.row)"
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
        </el-tab-pane>
      </el-tabs>
    </div>
    <!--用户编辑-->
    <el-drawer
      :visible.sync="modifyDrawer"
      size="80%"
      :withHeader="false"
      :close-on-press-escape="false"
    >
      <div
        style="height:100%;"
        v-loading="modifyLoading"
        element-loading-text="数据加载中"
        element-loading-background="rgba(0, 0, 0, 0.6)"
      >
        <div class="sinLeakDe">
          <el-row :gutter="100" style="height:95%;">
            <el-col :span="22" style="height:100%;">
              <div class="diaTitle">
                <span class="englishView">用户编辑</span>
                <img src="@/assets/img/modify_information.png" alt="" />
              </div>
              <div class="leftCon">
                <div class="modifyForm">
                  <el-form
                    :model="modifyForm"
                    :rules="rules1"
                    status-icon
                    ref="modifyForm"
                    label-width="100px"
                    v-if="activeName === 'second'"
                    class="demo-ruleForm"
                  >
                    <el-form-item label="账户名" prop="account">
                      <el-input
                        v-model="modifyForm.account"
                        required
                        maxlength="30"
                        style="width:50%"
                        clearable
                      ></el-input>
                    </el-form-item>
                    <el-form-item label="KEY" prop="key">
                      <el-input
                        v-model="modifyForm.key"
                        required
                        maxlength="50"
                        style="width:50%"
                        placeholder="请输入KEY"
                      ></el-input>
                    </el-form-item>
                    <el-form-item label="代理" prop="proxy">
                      <el-input
                        v-model="modifyForm.proxy"
                        required
                        maxlength="50"
                        style="width:50%"
                        placeholder="请输入代理"
                      ></el-input>
                    </el-form-item>
                    <el-form-item label="用户分类" prop="engine_type">
                      <el-select
                        style="width:50%;"
                        v-model="modifyForm.engine_type"
                        placeholder="请选择用户分类"
                      >
                        <el-option
                          v-for="item in userTypeList"
                          :key="item.name"
                          :label="item.name"
                          :value="item.name"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                  </el-form>
                  <el-form
                    :model="modifyForm1"
                    :rules="rules11"
                    status-icon
                    v-else
                    ref="modifyForm1"
                    label-width="100px"
                    class="demo-ruleForm"
                  >
                    <el-form-item
                      label="用户姓名"
                      prop="name"
                      v-show="activeName === 'first'"
                    >
                      <el-input
                        v-model="modifyForm1.name"
                        required
                        maxlength="28"
                        style="width:50%"
                        clearable
                      ></el-input>
                    </el-form-item>
                    <el-form-item
                      label="联系电话"
                      prop="phone"
                      v-show="activeName === 'first'"
                    >
                      <el-input
                        v-model="modifyForm1.phone"
                        required
                        style="width:50%"
                        placeholder="请输入联系电话"
                      ></el-input>
                    </el-form-item>
                    <el-form-item
                      label="电子邮箱"
                      prop="email"
                      v-show="activeName === 'first'"
                    >
                      <el-input
                        v-model="modifyForm1.email"
                        required
                        style="width:50%"
                        placeholder="请输入电子邮箱"
                      ></el-input>
                    </el-form-item>
                    <el-form-item
                      label="用户权限"
                      prop="user_permission"
                      v-show="activeName === 'first'"
                    >
                      <el-radio-group v-model="modifyForm1.user_permission">
                        <el-radio-button :label="0">普通用户</el-radio-button>
                        <el-radio-button :label="1">管理员 </el-radio-button>
                      </el-radio-group>
                    </el-form-item>
                  </el-form>
                </div>
              </div>
            </el-col>
          </el-row>
          <el-button
            @click="saveModify"
            :loading="saveLoading"
            type="primary"
            class="sureBtn"
            >保存修改</el-button
          >
        </div>
        <div @click="modifyDrawer = false" class="closeBtn">
          <i class="el-icon-arrow-right"></i>
        </div>
      </div>
    </el-drawer>
    <!-- 创建用户 -->
    <el-dialog
      :visible.sync="addVisible"
      class="addDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
      top="6%"
    >
      <div class="addMain">
        <div class="addTopbar">
          <span class="englishView"
            >新增{{ addActive === "user" ? "用户" : "账号" }}</span
          >
          <img src="@/assets/img/new_users.png" alt="" />
        </div>
        <div class="addDiv">
          <el-tabs v-model="addActive">
            <el-tab-pane label="用户" name="user" class="firstPane scrollStyle">
              <el-form
                :model="addform1"
                :rules="rules11"
                status-icon
                ref="addform1"
                label-width="100px"
                class="demo-ruleForm"
                style="height:85%"
              >
                <el-form-item label="用户姓名" prop="name">
                  <el-input
                    v-model="addform1.name"
                    required
                    maxlength="28"
                    style="width:50%"
                    placeholder="请输入用户姓名"
                    clearable
                  ></el-input>
                </el-form-item>
                <el-form-item label="联系电话" prop="phone">
                  <el-input
                    v-model="addform1.phone"
                    required
                    style="width:50%"
                    placeholder="请输入联系电话"
                  ></el-input>
                </el-form-item>
                <el-form-item label="电子邮箱" prop="email">
                  <el-input
                    v-model="addform1.email"
                    required
                    style="width:50%"
                    placeholder="请输入电子邮箱"
                  ></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                  <el-input
                    type="password"
                    style="width:50%"
                    v-model="addform1.password"
                    placeholder="请输入密码"
                    autocomplete="off"
                  ></el-input>
                </el-form-item>
                <el-form-item label="确认密码" prop="checkPass">
                  <el-input
                    type="password"
                    style="width:50%"
                    v-model="addform1.checkPass"
                    placeholder="请再次输入密码"
                    autocomplete="off"
                  ></el-input>
                </el-form-item>
                <el-form-item label="用户权限" prop="user_permission">
                  <el-radio-group v-model="addform1.user_permission">
                    <el-radio-button :label="0">普通用户</el-radio-button>
                    <el-radio-button :label="1"> 管理员 </el-radio-button>
                  </el-radio-group>
                </el-form-item>
              </el-form>
            </el-tab-pane>
            <el-tab-pane
              label="信息收集账号"
              name="apiuser"
              class="firstPane scrollStyle"
            >
              <el-form
                :model="addform"
                :rules="rules1"
                status-icon
                ref="addform"
                label-width="100px"
                class="demo-ruleForm"
                style="height:85%"
              >
                <el-form-item label="账户名" prop="account">
                  <el-input
                    v-model="addform.account"
                    required
                    maxlength="30"
                    style="width:50%"
                    placeholder="请输入账户名"
                    clearable
                  ></el-input>
                </el-form-item>
                <el-form-item label="KEY" prop="key">
                  <el-input
                    v-model="addform.key"
                    required
                    maxlength="50"
                    style="width:50%"
                    placeholder="请输入KEY"
                  ></el-input>
                </el-form-item>
                <el-form-item label="代理" prop="proxy">
                  <el-input
                    v-model="addform.proxy"
                    required
                    maxlength="50"
                    style="width:50%"
                    placeholder="请输入代理"
                  ></el-input>
                </el-form-item>
                <el-form-item label="用户分类" prop="engine_type">
                  <el-select
                    style="width:50%;"
                    v-model="addform.engine_type"
                    placeholder="请选择用户分类"
                  >
                    <el-option
                      v-for="item in userTypeList"
                      :key="item.name"
                      :label="item.name"
                      :value="item.name"
                    >
                    </el-option>
                  </el-select>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>
      <div slot="footer" class="addFooter">
        <el-button
          @click="addSubmit"
          type="primary"
          class="sureBtn"
          :loading="loadSureAdd"
          >创建{{ addActive === "user" ? "用户" : "账号" }}</el-button
        >
      </div>
    </el-dialog>
    <!--删除确认模态框-->
    <el-dialog
      :visible.sync="delVisible"
      width="30%"
      top="15%"
      class="delDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <span class="spans">{{
        dialogType === 0 ? "删除用户" : "删除账号"
      }}</span>
      <p class="contentPsty">
        {{ dialogType === 0 ? "确认删除该用户？" : "确认删除该账号?" }}
        <!-- <span style="font-weight:600;padding-left:15px;">{{
          delCon
        }}</span
        > -->
      </p>
      <div slot="footer">
        <el-button
          @click="sureDel"
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
  </div>
</template>
<script>
import { encrypt } from "@/utils/encrypt";
import {
  userDel,
  apiDel,
  // usertypeList,
  modifySave,
  modifyApiSave,
  userList,
  apiList,
  userAdd,
  apiAdd,
  taskAddArr
} from "@/api/user";
export default {
  name: "taskList",
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
    var validatePass = (rule, value, callback) => {
      if (!value) {
        return callback(new Error("密码不能为空"));
      } else {
        if (this.addform1.checkPass !== "") {
          this.$refs.addform1.validateField("checkPass");
        }
      }
      setTimeout(() => {
        var reg = /^(?![^A-Za-z]+$)(?![^0-9]+$)[^]{7,19}$/;
        var r = reg.test(value);
        if (!r) {
          return callback(new Error("密码不符合要求，请重新输入！"));
        } else {
          callback();
        }
      }, 1000);
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.addform1.password) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    return {
      addActive: "user",
      dialogType: 0,
      delId: "",
      delVisible: false,
      loadSureDel: false,
      userTypeList: [
        {
          id: 0,
          name: "shodan"
        },
        {
          id: 1,
          name: "zoomeye"
        },
        {
          id: 2,
          name: "censys"
        }
      ],
      modifyDrawer: false,
      modifyLoading: false,
      modifyForm: {
        account: "",
        key: "",
        engine_type: "",
        proxy: ""
      },
      modifyForm1: {
        name: "",
        phone: "",
        email: "",
        user_permission: 0
      },
      addform: {
        account: "",
        key: "",
        engine_type: "",
        proxy: ""
      },
      addform1: {
        name: "",
        phone: "",
        email: "",
        password: "",
        checkPass: "",
        user_permission: 0
      },
      activeName: "first",
      base_infos: {
        avatar: "",
        username: "",
        account: "",
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
      listLoading: false,
      userListData: [],
      accountListData: [],
      search: "",
      page: 1,
      page_size: 10,
      totalSize: 0,
      addVisible: false,
      loadSureAdd: false,
      form: {
        name: "",
        describe: "",
        time: ""
      },
      ruleForm: {
        email: "",
        phone: "",
        username: "",
        nickname: "",
        radio: 0
      },
      rules1: {
        account: [
          { required: true, message: "请输入账户姓名", trigger: "blur" }
        ],
        key: [{ required: true, message: "请输入KEY", trigger: "blur" }],
        proxy: [{ required: true, message: "请输入代理", trigger: "blur" }],
        engine_type: [
          { required: true, message: "请选择用户分类", trigger: "blur change" }
        ]
      },
      rules11: {
        email: [
          { required: true, message: "请输入邮箱地址", trigger: "blur" },
          {
            type: "email",
            message: "请输入正确的邮箱地址",
            trigger: ["blur", "change"]
          }
        ],
        phone: [{ validator: validateTel, trigger: "blur" }],
        name: [{ required: true, message: "请输入用户姓名", trigger: "blur" }],
        user_permission: [
          { required: true, message: "请选择用户分类", trigger: "blur change" }
        ],
        password: [{ validator: validatePass, trigger: "blur" }],
        checkPass: [{ validator: validatePass2, trigger: "blur" }]
      },
      userDetailDrawer: false,
      noDataIs: true,
      userBelong: [],
      defaultProps: {
        children: "children",
        label: "label"
      },
      modalArr: [],
      masterArr: [],
      detailGetLoading: false,
      saveLoading: false
    };
  },
  mounted() {
    this.getUserList("userinfo");
  },
  created() {
    // this.userTypesList();
  },
  methods: {
    // 获取用户类型列表
    userTypesList() {
      // usertypeList()
      //   .then(response => {
      //     if (response.data.success) {
      //       this.userTypeList = response.data.data;
      //     } else {
      //       this.$message.warning(response.data.info);
      //     }
      //   })
      //   .catch(error => {
      //     this.$message.error(error.message);
      //   });
    },
    // 详情切换
    handleClick() {
      this.page = 1;
      this.page_size = 10;
      this.search = "";
      this.modalChoose = "";
      var type = this.activeName === "first" ? "userinfo" : "keyinfo";
      this.getUserList(type);
    },
    // 获取用户/账户列表
    getUserList(val) {
      var sendD = {
        search_word: this.search,
        page: this.page,
        max_count: this.page_size
      };
      this.listLoading = true;
      if (val === "userinfo") {
        userList(sendD)
          .then(response => {
            this.listLoading = false;
            if (response.data.success) {
              this.userListData = response.data.data;
              this.totalSize = response.data.total;
              if (this.totalSize == 0) {
                this.noDataIs = false;
              } else {
                this.noDataIs = true;
              }
            } else {
              this.$message.warning(response.data.info);
            }
          })
          .catch(() => {
            this.listLoading = false;
            // this.$message.error(error.message);
          });
      } else {
        apiList(sendD)
          .then(response => {
            this.listLoading = false;
            if (response.data.success) {
              this.accountListData = response.data.data;
              this.totalSize = response.data.total;
              if (this.totalSize == 0) {
                this.noDataIs = false;
              } else {
                this.noDataIs = true;
              }
            } else {
              this.$message.warning(response.data.info);
            }
          })
          .catch(() => {
            this.listLoading = false;
            // this.$message.error(error.message);
          });
      }
    },
    // 查看详情
    checkDetail(val) {
      this.taskId = val.id;
      var form =
        this.activeName === "first" ? this.modifyForm1 : this.modifyForm;
      if (this.activeName === "first") {
        form.user_permission = val.user_permission;
        form.name = val.name;
        form.phone = val.phone;
        form.email = val.email;
      } else {
        form.account = val.account;
        form.key = val.key;
        form.engine_type = val.engine_type;
        form.proxy = val.proxy;
      }
      this.modifyDrawer = true;
    },
    // 创建用户
    addSubmit() {
      var form = this.addActive === "user" ? "addform1" : "addform";
      var formData = this.addActive === "user" ? this.addform1 : this.addform;
      this.$refs[form].validate(valid => {
        if (valid) {
          this.loadSureAdd = true;
          var psd = this.addActive === "user" ? formData.password : "";
          var encrypted = encrypt(psd);
          let sendD = {
            username: this.addActive === "user" ? formData.name : undefined,
            phone: this.addActive === "user" ? formData.phone : undefined,
            email: this.addActive === "user" ? formData.email : undefined,
            permission:
              this.addActive === "user" ? formData.user_permission : undefined,
            s_passwd: this.addActive === "user" ? encrypted : undefined,
            f_passwd: this.addActive === "user" ? encrypted : undefined,
            key: this.addActive === "apiuser" ? formData.key : undefined,
            account:
              this.addActive === "apiuser" ? formData.account : undefined,
            engine_type:
              this.addActive === "apiuser" ? formData.engine_type : undefined,
            proxy: this.addActive === "apiuser" ? formData.proxy : undefined
          };
          if (this.addActive === "user") {
            userAdd(sendD)
              .then(response => {
                this.loadSureAdd = false;
                if (response.data.success) {
                  this.addVisible = false;
                  this.getUserList("userinfo");
                  this.$message.success("用户创建成功");
                } else {
                  this.$message.warning(response.data.info);
                }
              })
              .catch(error => {
                this.loadSureAdd = false;
                this.addVisible = false;
                this.$message.error(error.message);
              });
          } else {
            apiAdd(sendD)
              .then(res => {
                this.loadSureAdd = false;
                if (res.data.success) {
                  this.addVisible = false;
                  this.$message.success("添加账户成功");
                  this.getUserList("keyinfo");
                } else {
                  this.$message.error(res.data.info);
                }
              })
              .catch(error => {
                this.loadSureAdd = false;
                this.addVisible = false;
                this.$message.error(error);
              });
          }
        } else {
          this.$message.error("请完善各项内容");
          return false;
        }
      });
    },
    // 保存修改
    saveModify() {
      //todo modifyForm
      var form = this.activeName === "first" ? "modifyForm1" : "modifyForm";
      var formData =
        this.activeName === "first" ? this.modifyForm1 : this.modifyForm;
      this.$refs[form].validate(valid => {
        if (valid) {
          this.saveLoading = true;
          var a = this.activeName === "first" ? true : false;
          var data = {
            user_id: this.taskId,
            username: a ? formData.name : undefined,
            phone: a ? formData.phone : undefined,
            email: a ? formData.email : undefined,
            permission: a ? formData.user_permission : undefined,
            engine_id: a ? undefined : this.taskId,
            account: a ? undefined : formData.account,
            key: a ? undefined : formData.engine_type,
            engine_type: a ? undefined : formData.engine_type,
            proxy: a ? undefined : formData.proxy
          };
          if (this.activeName === "first") {
            modifySave(data)
              .then(res => {
                this.saveLoading = false;
                this.modifyDrawer = false;
                if (res.data.success) {
                  this.$message.success("修改用户信息成功");
                  this.getUserList("userinfo");
                } else {
                  this.$message.error(res.data.info);
                }
              })
              .catch(error => {
                this.saveLoading = false;
                this.modifyDrawer = false;
                this.$message.error(error);
              });
          } else {
            modifyApiSave(data)
              .then(res => {
                this.saveLoading = false;
                this.modifyDrawer = false;
                if (res.data.success) {
                  this.$message.success("修改账户信息成功");
                  this.getUserList("keyinfo");
                } else {
                  this.$message.error(res.data.info);
                }
              })
              .catch(error => {
                this.saveLoading = false;
                this.modifyDrawer = false;
                this.$message.error(error);
              });
          }
        } else {
          this.$message.warning("请输入正确信息后保存！");
          return false;
        }
      });
    },
    // 用户 / 账户 删 除
    sureDel() {
      this.loadSureDel = true;
      var a = this.activeName === "first" ? true : false;
      if (a) {
        userDel({ user_id: this.delId })
          .then(res => {
            this.loadSureDel = false;
            if (res.data.success) {
              this.$message.success("删除用户成功");
              this.getUserList("userinfo");
            } else {
              this.$message.error(res.data.info);
            }
            this.delVisible = false;
          })
          .catch(error => {
            this.loadSureDel = false;
            this.delVisible = false;
            this.$message.error(error);
          });
      } else {
        apiDel({ engine_id: this.delId })
          .then(res => {
            this.loadSureDel = false;
            if (res.data.success) {
              this.$message.success("删除账户成功");
              this.getUserList("keyinfo");
            } else {
              this.$message.error(res.data.info);
            }
            this.delVisible = false;
          })
          .catch(error => {
            this.loadSureDel = false;
            this.delVisible = false;
            this.$message.error(error);
          });
      }
    },
    // 用户新增点击
    addSinTask() {
      var f = this.$refs["addform1"];
      if (f != undefined && f != null) {
        this.$refs["addform1"].resetFields();
      }
      var treeTar = this.$refs["addform"];
      if (treeTar != undefined && treeTar != null) {
        this.$refs["addform"].resetFields();
      }
      this.addVisible = true;
    },
    // 关键词搜索
    enterCheck(val) {
      if (val == "") {
        this.page = 1;
        this.page_size = 10;
        var type = this.activeName === "first" ? "userinfo" : "keyinfo";
        this.getUserList(type);
      }
    },
    clickCheck() {
      if (this.search != "") {
        this.page = 1;
        var type = this.activeName === "first" ? "userinfo" : "keyinfo";
        this.getUserList(type);
      }
    },
    // 修改信息
    userapiDel(val) {
      this.delId = val.id;
      this.delVisible = true;
    },
    // 分页
    handleSizeChange(val) {
      this.page_size = val;
      var data = this.activeName === "first" ? "userinfo" : "keyinfo";
      this.getUserList(data);
    },
    handleCurrentChange(val) {
      this.page = val;
      var data = this.activeName === "first" ? "userinfo" : "keyinfo";
      this.getUserList(data);
    },
    // 获取新增任务各数组
    getTaskAddArr() {
      taskAddArr()
        .then(response => {
          if (response.data.success) {
            let t = response.data.data;
            this.userBelong = t.userBelong;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    }
  }
};
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.userView {
  height: 100%;
  padding: 30px 30px 0px;
  background: #fff;
  position: relative;
  .addDialog {
    .addMain {
      height: 550px;
      width: 100%;
      .addTopbar {
        height: 50px;
        .englishView {
          height: 30px;
          line-height: 30px;
          float: left;
          font-size: 22px;
          font-weight: 100;
          margin-right: 20px;
        }
        img {
          margin-top: 3px;
        }
      }
      .addDiv {
        height: calc(100% - 30px);
        width: 100%;
      }
      .treeCol {
        padding: 0 10px 10px 40px;
        height: 100%;
        overflow-y: scroll;

        &::-webkit-scrollbar {
          width: 5px;
        }
      }
    }
  }
  .mainTop {
    margin-bottom: 30px;
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
    overflow-x: hidden;
    width: 100%;
    height: calc(100% - 72px);
    .editBtn {
      background-color: #434be0;
      color: #fff;
      &:hover {
        background-color: #545bde;
      }
    }
    .delBtn {
      background-color: #f65160;
      color: #fff;
      &:hover {
        background-color: #f3606e;
      }
    }
    .proTable {
      height: calc(100% - 68px);
      border-radius: 10px;
      &::-webkit-scrollbar {
        width: 6px;
      }
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
  .sinLeakDe {
    height: 100%;
    padding: 50px 70px;
    .rightTree {
      padding-top: 150px;
      height: 100%;
    }
    .diaTitle {
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
    .leftCon {
      height: 100%;
      & > div {
        padding-left: 10px;
      }
      .name {
        height: 34px;
        display: block;
        font-size: 30px;
        font-weight: bold;
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
      .userInfoTwo {
        margin-top: 40px;
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
      padding: 140px 30px 20px 0px;
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
  }
}
</style>
<style rel="stylesheet/scss" lang="scss">
.userView {
  .mainTop {
    .searchinput {
      z-index: 5;
      width: 15%;
      position: absolute;
      right: 20px;
      .el-input-group--append .el-input-group__append {
        background: #3b43db;
      }
    }
    .el-input-group--append .el-input-group__append {
      background: #3b43db;
    }
  }
  .el-dialog {
    border-radius: 2%;
  }
  .delDialog {
    .el-dialog {
      border-radius: 30px;
      .spans {
        font-size: 25px;
        text-align: center;
        display: block;
        // margin-bottom: 20px;
      }
      p {
        font-size: 18px;
        margin: 26px;
        font-weight: bold;
        text-align: center;
      }
      .btnCancle {
        color: #fff;
        background-image: linear-gradient(to right, #5861f0, #3b44db);
      }
    }
  }
  .mainList {
    .el-table thead th {
      padding-left: 20px;
      color: #000;
      font-weight: bold;
      background-color: #fff;
    }
    .el-table .el-table__row td {
      color: #999999;
      padding-left: 20px;
    }
    .el-table {
      overflow: auto;
      border-radius: 10px;
      .el-table thead th {
        background-color: #fff;
      }
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
      .detailBtn {
        background: #fff;
        color: black;
        border: 1px solid #6dd7f3;
      }
    }
    .el-tabs {
      height: calc(100% - 100px);
      .el-tabs__header {
        .el-tabs__nav {
          margin-left: 20px;
        }
        .el-tabs__active-bar {
          height: 2px;
          border-radius: 5px;
        }
        .el-tabs__item {
          font-size: 22px;
          box-shadow: none;
          height: 50px;
          line-height: 50px;
          color: #9c9da0;
        }
        .el-tabs__item:hover,
        .el-tabs__item.is-active {
          color: #409eff;
        }
      }
      .el-tabs__content {
        height: 100%;
        .el-tab-pane {
          height: 100%;
        }
        .otherPane {
          height: calc(100% - 88px);
        }
      }
    }
    .el-tag--danger {
      background-color: #ffffff;
      border-color: #f8bbb3;
      color: #ed5642;
    }
    .el-tag--warning {
      background-color: #fff;
      border-color: #fee39c;
      color: #f5ac0e;
    }
    .el-tag--primary {
      background-color: #fff;
      border-color: #c1d9fd;
    }
    .el-tag--info {
      background-color: #fff;
      border-color: #4dc98d;
      color: #4dc98d;
    }
  }
  .sinLeakDe {
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
      }
    }
    .sureBtn {
      position: absolute;
      bottom: 5%;
      left: 40%;
      width: 20%;
      border-radius: 36px;
      background-image: linear-gradient(to right, #56a5fe, #3e7bec);
    }
  }
  .addDialog {
    .addMain {
      .el-tabs {
        height: calc(100% - 100px);
        .el-tabs__header {
          margin: 0;
          .el-tabs__nav {
            margin-left: 20px;
          }
          .el-tabs__active-bar {
            height: 2px;
            border-radius: 5px;
          }
          .el-tabs__item {
            font-size: 22px;
            box-shadow: none;
            height: 50px;
            line-height: 50px;
            color: #9c9da0;
          }
          .el-tabs__item:hover,
          .el-tabs__item.is-active {
            color: #409eff;
          }
        }
        .el-tabs__content {
          height: 100%;
          .el-tab-pane {
            height: 100%;
          }
          .otherPane {
            height: calc(100% - 88px);
          }
        }
      }
      .el-form {
        height: 100%;
        width: 100%;
        .el-form-item {
          margin-bottom: 30px;
          .el-form-item__label {
            text-align: left;
            font-weight: 600;
            &::before {
              display: none;
            }
          }
        }
      }
    }
    .addFooter {
      text-align: center;
      .sureBtn {
        width: 30%;
        border-radius: 36px;
        background-image: linear-gradient(to right, #56a5fe, #3e7bec);
      }
    }
  }
  .el-radio-group {
    .el-radio-button:first-child {
      box-shadow: none;
      .el-radio-button__inner {
        border-right: 0;
        border-radius: 36px 0 0 36px;
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
        border-radius: 0 36px 36px 0;
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
</style>
