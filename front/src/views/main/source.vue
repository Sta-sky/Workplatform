<template>
  <div
    class="sourceView"
    v-loading="listLoading"
    element-loading-text="数据加载中"
    element-loading-background="rgba(0, 0, 0, 0.6)"
  >
    <div class="mainTop">
      <span class="englishView">资源管理</span>
      <img src="@/assets/img/sourceManage.png" alt="" />
    </div>
    <div class="mainList">
      <div class="topPos">
        <el-button
          v-if="
            adminUser && (activeName === 'third' || activeName === 'fourth')
          "
          title="新增"
          type="primary"
          size="medium"
          style="height:42px;padding:8px 20px;margin-left:10px;background-image: linear-gradient(to right, #56a5fe, #3e7bec);"
          icon="el-icon-circle-plus-outline"
          @click="addSinLink"
          round
          >{{ btnCon }}</el-button
        >
        <el-input
          class="searchBoxPos"
          v-if="activeName != 'first'"
          placeholder="请输入搜索内容"
          @input="enterCheck"
          @keypress.enter.native="clickCheck"
          v-model="search"
          :style="{
            width: activeName === 'second' ? '50%' : adminUser ? '60%' : 'auto'
          }"
        >
          <el-button
            slot="append"
            icon="el-icon-search"
            @click="clickCheck"
          ></el-button>
        </el-input>
        <el-select
          @change="mcChange"
          v-model="modalChoose"
          v-if="activeName === 'second'"
          class="hostPos"
        >
          <el-option label="全部" value=""></el-option>
          <el-option label="本地" :value="0"></el-option>
          <el-option label="外网" :value="1"></el-option>
        </el-select>
      </div>
      <div class="pageShowStyle" v-if="activeName != 'first'">
        <el-pagination
          class="pageShowView"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="page"
          :page-sizes="[10, 25, 50, 100]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalSize"
        >
        </el-pagination>
      </div>
      <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane
          label="资源概览"
          name="first"
          class="firstPane scrollStyle"
        >
          <div class="firstMainView">
            <el-row :gutter="50" style="height:334px;margin-right:0;">
              <el-col :span="14" style="height:100%;">
                <h2 class="title">数据统计</h2>
                <div id="leftCircle"></div>
                <div id="rightCircle"></div>
              </el-col>
              <el-col :span="9" style="height:100%;">
                <h2 class="title">最新模板top5</h2>
                <el-table
                  :data="baseDetail.template_top5"
                  border
                  style="width: 100%;border-radius:10px;"
                  size="small"
                >
                  <el-table-column
                    prop="name"
                    label="名称"
                    show-overflow-tooltip
                  >
                  </el-table-column>
                  <el-table-column prop="cpu" label="CPU"> </el-table-column>
                  <el-table-column prop="memory" label="内存(M)">
                  </el-table-column>
                  <el-table-column prop="disk" label="磁盘(G)">
                  </el-table-column>
                  <el-table-column
                    prop="type"
                    label="类型"
                    width="100"
                    show-overflow-tooltip
                  >
                  </el-table-column>
                </el-table>
              </el-col>
            </el-row>
            <el-row :gutter="50" style="height:334px;margin-right:0;">
              <el-col :span="14" style="height:100%;">
                <h2 class="title">数量统计</h2>
                <el-row
                  :gutter="50"
                  v-if="baseDetail.hasOwnProperty('weapons_count')"
                >
                  <el-col :span="6">
                    <div class="sin" @click="checkActive('fourth')">
                      <count-to
                        :start-val="0"
                        :end-val="baseDetail.weapons_count"
                        :duration="2800"
                        class="numCon"
                      />
                      <p class="totalNum">武器库数量</p>
                    </div>
                  </el-col>
                  <el-col :span="6">
                    <div class="sin" @click="checkActive('third')">
                      <count-to
                        :start-val="0"
                        :end-val="baseDetail.links_count"
                        :duration="2800"
                        class="numCon"
                      />
                      <p class="totalNum">链路数量</p>
                    </div>
                  </el-col>
                  <el-col :span="6">
                    <div class="sin">
                      <count-to
                        :start-val="0"
                        :end-val="baseDetail.weapon_download_time"
                        :duration="2800"
                        class="numCon"
                      />
                      <p class="totalNum">下载次数</p>
                    </div>
                  </el-col>
                </el-row>
              </el-col>
              <el-col :span="9" style="height:100%;">
                <h2 class="title">最新武器top5</h2>
                <el-table
                  :data="baseDetail.weapon_top5"
                  border
                  style="width: 100%;border-radius:10px;"
                  size="small"
                >
                  <el-table-column
                    prop="name"
                    label="名称"
                    show-overflow-tooltip
                  >
                  </el-table-column>
                  <el-table-column prop="size" label="大小">
                    <template slot-scope="scope">
                      {{ $bytesToSize(scope.row.size) }}
                    </template>
                  </el-table-column>
                  <el-table-column
                    prop="category"
                    label="类型"
                    show-overflow-tooltip
                  >
                  </el-table-column>
                </el-table>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
        <el-tab-pane
          label="模板资源"
          name="second"
          class="otherPane scrollStyle"
        >
          <el-table :data="modalSourceArr" border class="filesTable">
            <el-table-column type="index" label="序号" width="50">
            </el-table-column>
            <el-table-column label="模板来源" show-overflow-tooltip>
              <template slot-scope="scope">
                <el-tag
                  :type="scope.row.source === 0 ? 'success' : 'danger'"
                  disable-transitions
                  >{{
                    scope.row.source === 0 ? "本地镜像" : "外网镜像"
                  }}</el-tag
                >
              </template>
            </el-table-column>
            <el-table-column prop="template_name" label="模板名称">
            </el-table-column>
            <el-table-column
              prop="description"
              label="模板描述"
              show-overflow-tooltip
            >
            </el-table-column>
            <el-table-column prop="vcpu_counts" label="CPU"> </el-table-column>
            <el-table-column prop="memory" label="内存(M)"> </el-table-column>
            <el-table-column prop="disk_size" label="磁盘(G)">
            </el-table-column>
            <el-table-column prop="vm_count" label="虚拟机数量">
            </el-table-column>
            <el-table-column prop="resource_type" label="资源类型">
            </el-table-column>
            <el-table-column prop="create_time" label="创建时间">
            </el-table-column>
            <el-table-column label="操作" width="100">
              <template slot-scope="scope">
                <el-button
                  title="详情"
                  class="sinProBtn"
                  type="primary"
                  @click="checkSinModal(scope.row)"
                >
                  详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane
          label="链路资源"
          name="third"
          class="otherPane scrollStyle"
        >
          <el-table :data="linkSourceArr" border class="filesTable">
            <el-table-column type="index" label="序号" width="50">
            </el-table-column>
            <el-table-column prop="uuid" label="序列号"> </el-table-column>
            <el-table-column
              prop="description"
              label="链路描述"
              show-overflow-tooltip
            >
            </el-table-column>
            <el-table-column prop="group" label="组名称"> </el-table-column>
            <el-table-column prop="create_time" label="创建时间">
            </el-table-column>
            <el-table-column prop="failuretime" label="失效时间">
            </el-table-column>
            <el-table-column label="操作" width="200" v-if="adminUser">
              <template slot-scope="scope">
                <el-button
                  title="编辑"
                  class="sinProBtn"
                  type="primary"
                  @click="editSinLink(scope.row)"
                >
                  编辑
                </el-button>
                <el-button
                  title="删除"
                  class="sinProBtn delBtn"
                  type="danger"
                  @click="delSinLink(scope.row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="武器资源" name="fourth" class="otherPane">
          <el-radio-group
            v-model="category"
            @change="weaponCchange"
            style="margin:0 0 20px 25px;"
          >
            <el-radio-button
              v-for="(item, i) in weaponTypeArr"
              :key="i"
              :label="item.id"
              >{{ item.name }}</el-radio-button
            >
          </el-radio-group>
          <el-table
            :data="weaponSourceArr"
            border
            class="weaponTable scrollStyle"
          >
            <el-table-column type="index" label="序号" width="50">
            </el-table-column>
            <el-table-column
              prop="weapon_name"
              label="武器名称"
              show-overflow-tooltip
            >
            </el-table-column>
            <el-table-column
              prop="description"
              label="武器描述"
              show-overflow-tooltip
            >
            </el-table-column>
            <el-table-column prop="size" label="资源大小" width="150">
              <template slot-scope="scope">
                {{ $bytesToSize(scope.row.size) }}
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100">
              <template slot-scope="scope">
                <el-tag
                  :type="scope.row.status === 0 ? 'success' : ''"
                  disable-transitions
                  >{{
                    scope.row.status === 0 ? "检测中..." : "监测完毕"
                  }}</el-tag
                >
              </template>
            </el-table-column>
            <el-table-column prop="create_time" label="创建时间" width="200">
            </el-table-column>
            <el-table-column label="操作" :width="adminUser ? 'auto' : 180">
              <template slot-scope="scope">
                <div v-if="scope.row.status === 1">
                  <div v-if="scope.row.isSure">
                    <el-button
                      title="详情"
                      class="sinProBtn"
                      type="primary"
                      @click="checkSinWeapon(scope.row, 'detail')"
                    >
                      详情
                    </el-button>
                    <el-button
                      title="下载"
                      class="sinProBtn whiteBtn"
                      type="primary"
                      @click="downLoadSinWeapon(scope.row)"
                    >
                      下载
                    </el-button>
                    <el-button
                      v-if="adminUser"
                      title="删除"
                      class="sinProBtn delBtn"
                      type="danger"
                      @click="delSinLink(scope.row)"
                    >
                      删除
                    </el-button>
                  </div>
                  <div v-else>
                    <div v-if="adminUser">
                      <el-button
                        title="查看文件"
                        class="sinProBtn"
                        type="success"
                        @click="checkSinWeapon(scope.row, 'file')"
                      >
                        查看文件
                      </el-button>
                      <el-button
                        title="确认保存"
                        class="sinProBtn"
                        type="primary"
                        @click="saveSinWeapon(scope.row)"
                      >
                        确认保存
                      </el-button>
                      <el-button
                        title="删除文件"
                        class="sinProBtn delBtn"
                        type="danger"
                        @click="delSinLink(scope.row)"
                      >
                        删除文件
                      </el-button>
                    </div>
                  </div>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </div>
    <!--模板详情模抽屉-->
    <el-drawer
      :visible.sync="detailDrawer"
      class="addTaskModal"
      size="80%"
      :withHeader="false"
      :close-on-press-escape="false"
    >
      <div
        style="height:100%;"
        v-loading="drawerDetailLoading"
        element-loading-text="数据加载中"
        element-loading-background="rgba(0, 0, 0, 0.6)"
      >
        <div class="addTaskBox" style="height:100%;">
          <div class="addModalTop" v-if="activeName === 'second'">
            <span class="englishView">模板详情</span>
            <img src="@/assets/img/modalDet.png" alt="" />
          </div>
          <div class="addModalTop" v-else>
            <span class="englishView">武器详情</span>
            <img src="@/assets/img/weaponDet.png" alt="" />
          </div>
          <p class="titleOfSourceDetail">
            {{ detailName }}
          </p>
          <el-input
            class="searchPos"
            v-if="activeName === 'second'"
            placeholder="请输入搜索内容"
            @input="enterDetailCheck"
            @keypress.enter.native="checkDetailResult"
            v-model="drawerSearch"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="checkDetailResult"
            ></el-button>
          </el-input>
          <div class="pageShowStyle" v-if="activeName != 'fourth'">
            <el-pagination
              class="pageShowView"
              @size-change="detailSizeChange"
              @current-change="detailCurrentChange"
              :current-page="drawerPage"
              :page-sizes="[10, 25, 50, 100]"
              :page-size="drawerPageSize"
              layout="total, sizes, prev, pager, next, jumper"
              :total="drawerTotalSize"
            >
            </el-pagination>
          </div>
          <div class="detailMainView scrollStyle">
            <el-table
              :data="sinModalDetailArr"
              border
              v-if="activeName === 'second'"
            >
              <el-table-column type="index" label="序号" width="50">
              </el-table-column>
              <el-table-column prop="detail_name" label="名称">
              </el-table-column>
              <el-table-column prop="ip" label="IP" show-overflow-tooltip>
              </el-table-column>
              <el-table-column label="状态">
                <template slot-scope="scope">
                  <el-tag
                    :type="
                      scope.row.status === 0
                        ? 'success'
                        : scope.row.status === 1
                        ? ''
                        : 'danger'
                    "
                    disable-transitions
                    >{{
                      scope.row.status === 0
                        ? "开启"
                        : scope.row.status === 1
                        ? "挂起"
                        : "关闭"
                    }}</el-tag
                  >
                </template>
              </el-table-column>
              <el-table-column prop="update_time" label="开启时间">
              </el-table-column>
            </el-table>
            <div class="weaponDetail" v-else>
              <el-form
                v-if="typeIsDet"
                :model="sinWeaponDetail"
                label-position="left"
                label-width="120px"
                style="padding-right:20px;"
                class="reviewFsty"
              >
                <el-form-item label="武器大小">
                  <p>{{ $bytesToSize(sinWeaponDetail.size) }}</p>
                </el-form-item>
                <el-form-item label="武器分类">
                  <p>{{ category_name }}</p>
                </el-form-item>
                <el-form-item label="创建时间">
                  <p>{{ sinWeaponDetail.create_time }}</p>
                </el-form-item>
                <el-form-item label="武器描述">
                  <p>{{ sinWeaponDetail.description }}</p>
                </el-form-item>
                <el-form-item label="使用说明">
                  <p>{{ sinWeaponDetail.info }}</p>
                </el-form-item>
              </el-form>
              <summary-to
                v-else
                ref="sum"
                :changeList="firstState"
                :taskid="taskId"
              />
            </div>
          </div>
          <div @click="detailDrawer = false" class="closeBtn">
            <i class="el-icon-arrow-right"></i>
          </div>
        </div>
      </div>
    </el-drawer>
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
          <span class="englishView">新建链路</span>
          <img src="@/assets/img/new_link.png" alt="" />
        </div>
        <div class="addTopbar" v-else>
          <span class="englishView">编辑链路</span>
          <img src="@/assets/img/edit_link.png" alt="" />
        </div>
        <el-form
          :model="linkForm"
          status-icon
          :rules="rulesLink"
          ref="linksforms"
          label-width="100px"
          class="weaponForm"
        >
          <el-form-item label="uuid" prop="uuid" class="fifty">
            <el-input v-model="linkForm.uuid"></el-input>
          </el-form-item>
          <el-form-item label="失效时间" prop="failuretime" class="fifty">
            <el-date-picker
              v-model="linkForm.failuretime"
              type="datetime"
              value-format="yyyy-MM-dd HH:mm:ss"
              style="width:100%;"
              placeholder="选择日期时间"
            >
            </el-date-picker>
          </el-form-item>
          <el-form-item label="链路描述" prop="description">
            <el-input
              type="textarea"
              :rows="5"
              v-model="linkForm.description"
            ></el-input>
          </el-form-item>
          <el-form-item label="选择组">
            <el-tree
              ref="tree"
              node-key="name"
              :data="treeData"
              :props="treeProps"
              class="treeSty"
              :check-on-click-node="true"
              :default-expand-all="true"
              show-checkbox
              :highlight-current="true"
              @check-change="nodeClick"
            ></el-tree>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer" class="addFooter">
        <el-button
          @click="addSureLink"
          type="primary"
          class="sureBtn"
          :loading="addLinkLoad"
          >{{ addNewLink ? "新建链路" : "编辑链路" }}</el-button
        >
      </div>
    </el-dialog>
    <!-- 新增武器 -->
    <el-dialog
      :visible.sync="addWeaponVisible"
      class="addDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
      top="6%"
    >
      <div class="addMain">
        <div class="addTopbar">
          <span class="englishView">新增武器</span>
          <img src="@/assets/img/new_weapon.png" alt="" />
        </div>
        <el-form
          :model="ruleForm"
          status-icon
          :rules="rules1"
          ref="forms"
          label-width="100px"
          class="weaponForm"
        >
          <el-form-item label="武器上传" prop="fileName" class="fifty">
            <el-input v-model="ruleForm.fileName">
              <el-upload
                slot="suffix"
                class="upload-demo"
                ref="upload"
                action="#"
                :show-file-list="false"
                :auto-upload="false"
                :on-change="changeFile"
              >
                <el-button
                  slot="trigger"
                  size="small"
                  type="primary"
                  icon="iconfont icon-shangchuan"
                ></el-button>
              </el-upload>
            </el-input>
          </el-form-item>
          <el-form-item label="武器名称" prop="name" class="fifty">
            <el-input v-model="ruleForm.name"></el-input>
          </el-form-item>
          <el-form-item label="武器分类" prop="weaponType">
            <el-row>
              <el-col :span="10">
                <el-select
                  style="width:100%;"
                  v-model="ruleForm.weaponType"
                  placeholder="请选择"
                >
                  <el-option
                    v-for="item in weaponTypeArr"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                  >
                  </el-option>
                </el-select>
              </el-col>
              <el-col :span="3" style="text-align:center;">
                或新增
              </el-col>
              <el-col :span="10">
                <el-input v-model="weaponTypeNmae"></el-input>
              </el-col>
            </el-row>
          </el-form-item>
          <el-form-item label="武器大小" class="fifty">
            <span v-if="ruleForm.fileName != ''">
              {{ ruleForm.size }}
            </span>
          </el-form-item>
          <el-form-item label="武器描述" prop="description">
            <el-input
              type="textarea"
              :rows="5"
              v-model="ruleForm.description"
            ></el-input>
          </el-form-item>
          <el-form-item label="使用说明" prop="useIns">
            <el-input
              type="textarea"
              :rows="5"
              v-model="ruleForm.useIns"
            ></el-input>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer" class="addFooter">
        <el-button
          @click="addSubmit"
          type="primary"
          class="sureBtn"
          :loading="loadSureAdd"
          >新增武器</el-button
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
        是否确认删除?
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
  </div>
</template>
<script>
import CountTo from "vue-count-to";
import SummaryTo from "@/views/main/summary.vue";
import {
  sourceReview,
  modalsReview,
  sinModalDetail,
  linksReview,
  linksAdd,
  linksUpdate,
  linksDel,
  weaponCategory,
  weaponReview,
  weaponAdd,
  weaponFileSave,
  weaponDel
} from "@/api/source";
import { organizationList } from "@/api/organization";
export default {
  name: "scourceManage",
  components: {
    CountTo,
    SummaryTo
  },
  data() {
    return {
      firstState: 0,
      taskId: null,
      listLoading: false,
      activeName: "first",
      page: 1,
      pageSize: 10,
      totalSize: 0,
      search: "",
      drawerPage: 1,
      drawerPageSize: 10,
      drawerTotalSize: 0,
      drawerSearch: "",
      modalChoose: "",
      baseDetail: {},
      modalSourceArr: [],
      sinModalDetailArr: [],
      linkSourceArr: [],
      weaponSourceArr: [],
      weaponTypeArr: [],
      drawerDetailLoading: false,
      modalId: null,
      detailDrawer: false,
      detailName: "",
      category: null,
      category_name: "",
      sinWeaponDetail: {},
      adminUser: null,
      addWeaponVisible: false,
      ruleForm: {
        file: "",
        fileName: "",
        name: "",
        size: "",
        weaponType: "",
        description: "",
        useIns: ""
      },
      rules1: {
        fileName: [{ required: true, message: "请上传武器", trigger: "blur" }],
        name: [{ required: true, message: "请输入武器名称", trigger: "blur" }],
        description: [
          { required: true, message: "请输入武器描述", trigger: "blur" }
        ],
        useIns: [
          { required: true, message: "请输入武器使用说明", trigger: "blur" }
        ]
      },
      linkForm: {
        id: "",
        uuid: "",
        group: "",
        failuretime: "",
        description: ""
      },
      rulesLink: {
        uuid: [{ required: true, message: "请输入uuid", trigger: "blur" }],
        group: [{ required: true, message: "请选择链路组", trigger: "blur" }],
        description: [
          { required: true, message: "请输入链路描述", trigger: "blur" }
        ],
        failuretime: [
          { required: true, message: "请选择失效时间", trigger: "blur" }
        ]
      },
      loadSureAdd: false,
      addVisible: false,
      file_id: null,
      addLinkLoad: false,
      addLinkVisible: false,
      linkId: null,
      btnCon: "新增链路",
      weaponTypeNmae: "",
      weapon_name: "",
      treeData: [],
      treeProps: {
        children: "children",
        label: "name"
      },
      delVisible: false,
      loadSureDel: false,
      addNewLink: true,
      typeIsDet: true
    };
  },
  mounted() {
    this.adminUser = this.$store.getters.roles === "admin" ? true : false;
    this.checkFirst();
  },
  created() {
    this.getWeaponsTypes();
    this.getOrgList();
  },
  methods: {
    // 详情切换
    handleClick() {
      this.page = 1;
      this.pageSize = 10;
      this.serach = "";
      this.modalChoose = "";
      if (this.activeName === "third") {
        this.btnCon = "新增链路";
      }
      if (this.activeName === "fourth") {
        this.btnCon = "新增武器";
        this.category = this.weaponTypeArr[0].id;
        this.category_name = this.weaponTypeArr[0].name;
      }
      this.changeView();
    },
    changeView() {
      this.listLoading = true;
      switch (this.activeName) {
        case "first":
          this.checkFirst();
          break;
        case "second":
          this.checkSecond();
          break;
        case "third":
          this.checkThird();
          break;
        case "fourth":
          this.checkFourth();
      }
    },
    // 资源概览获取
    checkFirst() {
      this.listLoading = true;
      sourceReview()
        .then(response => {
          this.listLoading = false;
          if (response.data.success) {
            this.baseDetail = response.data.data;
            this.leftChartView();
            this.rightChartView();
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.listLoading = false;
          this.$message.error(error.message);
        });
    },
    // 概览环形图渲染
    leftChartView() {
      let chart = this.$echarts.init(document.getElementById("leftCircle"));
      let color = ["#13dd5a", "#3b83ef"];
      let echartData = [
        {
          name: "本地资源",
          value: this.baseDetail.local_template_count
        },
        {
          name: "外部资源",
          value: this.baseDetail.foreign_template_count
        }
      ];

      let formatNumber = function(num) {
        let reg = /(?=(\B)(\d{3})+$)/g;
        return num.toString().replace(reg, ",");
      };
      let option = {
        color: color,
        title: [
          {
            text: "{val|" + formatNumber(this.baseDetail.templates_count) + "}",
            top: "center",
            left: "center",
            textStyle: {
              rich: {
                val: {
                  fontSize: 24,
                  fontWeight: "bold",
                  color: "#333333"
                }
              }
            }
          },
          {
            text: "模板来源",
            bottom: 10,
            left: "center",
            textStyle: {
              fontSize: 14,
              color: "#636469",
              fontWeight: 100
            }
          }
        ],
        series: [
          {
            type: "pie",
            radius: ["45%", "60%"],
            center: ["50%", "50%"],
            data: echartData,
            hoverAnimation: false,
            labelLine: {
              normal: {
                length: 20,
                length2: 120
              }
            },
            label: {
              normal: {
                formatter: params => {
                  return (
                    "{icon|●}{name|" +
                    params.name +
                    "}{value|" +
                    formatNumber(params.value) +
                    "}"
                  );
                },
                padding: [0, -130, 25, -130],
                rich: {
                  icon: {
                    fontSize: 16
                  },
                  name: {
                    fontSize: 14,
                    padding: [0, 10, 0, 4]
                  },
                  value: {
                    fontSize: 18,
                    fontWeight: "bold"
                  }
                }
              }
            }
          }
        ]
      };
      chart.setOption(option, true);
      window.addEventListener("resize", function() {
        chart.resize();
      });
    },
    rightChartView() {
      let chart = this.$echarts.init(document.getElementById("rightCircle"));
      let color = ["#f9b72a", "#f5593a"];
      let echartData = [
        {
          name: "已开启数量",
          value: this.baseDetail.vm_started_count
        },
        {
          name: "未开启数量",
          value: this.baseDetail.useless_vms_count
        }
      ];

      let formatNumber = function(num) {
        let reg = /(?=(\B)(\d{3})+$)/g;
        return num.toString().replace(reg, ",");
      };
      let option = {
        color: color,
        title: [
          {
            text: "{val|" + formatNumber(this.baseDetail.vms_count) + "}",
            top: "center",
            left: "center",
            textStyle: {
              rich: {
                val: {
                  fontSize: 24,
                  fontWeight: "bold",
                  color: "#333333"
                }
              }
            }
          },
          {
            text: "总计状态",
            bottom: 10,
            left: "center",
            textStyle: {
              fontSize: 14,
              color: "#636469",
              fontWeight: 100
            }
          }
        ],
        series: [
          {
            type: "pie",
            radius: ["45%", "60%"],
            center: ["50%", "50%"],
            data: echartData,
            hoverAnimation: false,
            labelLine: {
              normal: {
                length: 20,
                length2: 120
              }
            },
            label: {
              normal: {
                formatter: params => {
                  return (
                    "{icon|●}{name|" +
                    params.name +
                    "}{value|" +
                    formatNumber(params.value) +
                    "}"
                  );
                },
                padding: [0, -130, 25, -130],
                rich: {
                  icon: {
                    fontSize: 16
                  },
                  name: {
                    fontSize: 14,
                    padding: [0, 10, 0, 4]
                  },
                  value: {
                    fontSize: 18,
                    fontWeight: "bold"
                  }
                }
              }
            }
          }
        ]
      };
      chart.setOption(option, true);
      window.addEventListener("resize", function() {
        chart.resize();
      });
    },
    // 左下角数量点击跳转
    checkActive(tar) {
      this.activeName = tar;
      this.handleClick();
    },
    // 全部/内网/外网切换
    mcChange() {
      this.search = "";
      this.page = 1;
      this.pageSize = 10;
      this.checkSecond();
    },
    // 模板资源获取
    checkSecond() {
      var sendD = {
        search: this.search,
        page: this.page,
        page_size: this.pageSize,
        source: this.modalChoose
      };
      modalsReview(sendD)
        .then(response => {
          this.listLoading = false;
          if (response.data.success) {
            this.modalSourceArr = response.data.data;
            this.totalSize = response.data.total;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.listLoading = false;
          this.$message.error(error.message);
        });
    },
    // 查看模板详情
    checkSinModal(row) {
      this.modalId = row.id;
      this.detailName = row.template_name;
      this.detailDrawer = true;
      this.checkModalDetail();
    },
    checkModalDetail() {
      this.drawerDetailLoading = true;
      var sendD = {
        id: this.modalId,
        search: this.drawerSearch,
        page: this.drawerPage,
        page_size: this.drawerPageSize
      };
      sinModalDetail(sendD)
        .then(response => {
          this.drawerDetailLoading = false;
          if (response.data.success) {
            this.sinModalDetailArr = response.data.data;
            this.drawerTotalSize = response.data.total;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.drawerDetailLoading = false;
          this.$message.error(error.message);
        });
    },
    // 链路资源获取
    // 获取组织列表
    getOrgList() {
      this.listLoading = true;
      organizationList()
        .then(response => {
          this.listLoading = false;
          if (response.data.success) {
            this.treeData = response.data.data.data;
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
    nodeClick(val, check) {
      if (check) {
        this.linkForm.group = val.name;
      } else {
        this.linkForm.group = "";
      }
    },
    checkThird() {
      var sendD = {
        searchParam: this.search,
        page: this.page,
        pageSize: this.pageSize
      };
      linksReview(sendD)
        .then(response => {
          this.listLoading = false;
          if (response.data.success) {
            this.linkSourceArr = response.data.data;
            this.totalSize = response.data.total;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.listLoading = false;
          this.$message.error(error.message);
        });
    },
    // 新增单个链路
    addSinLink() {
      if (this.activeName === "third") {
        this.addLink();
      } else {
        this.addWeapon();
      }
    },
    addLink() {
      this.addNewLink = true;
      const f = this.$refs["linksforms"];
      if (f != undefined && f != null) {
        this.$refs["linksforms"].resetFields();
      }
      const tre = this.$refs["tree"];
      if (tre != undefined && tre != null) {
        this.$refs.tree.setChecked(this.linkForm.group, false);
      }
      this.linkForm = {
        id: "",
        uuid: "",
        group: "",
        failuretime: "",
        description: ""
      };
      this.addLinkVisible = true;
    },
    addSureLink() {
      this.$refs["linksforms"].validate(valid => {
        if (valid) {
          if (this.linkForm.group === "") {
            this.$message.error("请选择链路所属组织");
            return false;
          }
          this.addLinkLoad = true;
          let sendD = {
            uuid: this.linkForm.uuid,
            description: this.linkForm.description,
            failuretime: this.linkForm.failuretime,
            group: this.linkForm.group
          };
          if (this.addNewLink) {
            linksAdd(sendD)
              .then(response => {
                this.addLinkLoad = false;
                this.addLinkVisible = false;
                if (response.data.success) {
                  this.checkThird();
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
            linksUpdate(sendD)
              .then(response => {
                this.addLinkLoad = false;
                this.addLinkVisible = false;
                if (response.data.success) {
                  this.checkThird();
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
    // 编辑
    editSinLink(row) {
      this.addNewLink = false;
      this.linkForm = {
        id: row.id,
        uuid: row.uuid,
        group: row.group,
        failuretime: row.failuretime,
        description: row.description
      };
      this.addLinkVisible = true;
      this.$nextTick(() => {
        this.$refs.tree.setChecked(row.group, true);
      });
    },
    // 删除
    delSinLink(row) {
      this.linkId = row.id;
      this.delVisible = true;
    },
    sureDelLink() {
      this.loadSureDel = true;
      let sendD = {
        id: this.linkId
      };
      if (this.activeName === "third") {
        linksDel(sendD)
          .then(response => {
            this.loadSureDel = false;
            this.delVisible = false;
            if (response.data.success) {
              if (this.linkSourceArr.length === 1) {
                this.page = 1;
              }
              this.checkThird();
            } else {
              this.$message.warning(response.data.info);
            }
          })
          .catch(error => {
            this.loadSureDel = false;
            this.delVisible = false;
            this.$message.error(error.message);
          });
      } else {
        weaponDel(sendD)
          .then(response => {
            this.loadSureDel = false;
            this.delVisible = false;
            if (response.data.success) {
              if (this.linkSourceArr.length === 1) {
                this.page = 1;
              }
              this.checkFourth();
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
    },
    // 武器资源获取
    checkFourth() {
      var sendD = {
        search: this.search,
        page: this.page,
        page_size: this.pageSize,
        category_id: this.category
      };
      weaponReview(sendD)
        .then(response => {
          this.listLoading = false;
          if (response.data.success) {
            this.weaponSourceArr = response.data.data;
            this.totalSize = response.data.total;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.listLoading = false;
          this.$message.error(error.message);
        });
    },
    // 武器类别获取
    getWeaponsTypes() {
      weaponCategory()
        .then(response => {
          if (response.data.success) {
            this.weaponTypeArr = response.data.data;
            this.category = this.weaponTypeArr[0].id;
            this.category_name = this.weaponTypeArr[0].name;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    // 类别切换
    weaponCchange(val) {
      this.weaponTypeArr.forEach(el => {
        if (el.id === val) {
          this.category_name = el.name;
        }
      });
      this.listLoading = true;
      this.search = "";
      this.page = 1;
      this.pageSize = 10;
      this.checkFourth();
    },
    addWeapon() {
      var f = this.$refs["forms"];
      if (f != undefined && f != null) {
        f.resetFields();
      }
      this.weaponTypeNmae = "";
      this.addWeaponVisible = true;
    },
    // 上传武器
    changeFile(file) {
      this.ruleForm.fileName = file.name;
      this.ruleForm.file = file.raw;
      this.ruleForm.name = file.name;
      this.ruleForm.size = this.$bytesToSize(file.size);
    },
    // 新增武器
    addSubmit() {
      this.$refs["forms"].validate(valid => {
        if (valid) {
          if (this.weaponTypeNmae === "" && this.ruleForm.weaponType === "") {
            this.$message.error("请选择/输入武器类别");
            return false;
          }
          this.loadSureAdd = true;
          var weaponType = this.ruleForm.weaponType;
          if (this.weaponTypeNmae !== "") {
            weaponType = this.weaponTypeNmae;
          }
          const sendD = new FormData();
          sendD.append("file", this.ruleForm.file);
          sendD.append("name", this.ruleForm.name);
          sendD.append("category", weaponType);
          sendD.append("description", this.ruleForm.description);
          sendD.append("useIns", this.ruleForm.useIns);
          weaponAdd(sendD)
            .then(response => {
              this.loadSureAdd = false;
              this.addWeaponVisible = false;
              if (response.data.success) {
                this.checkFourth();
              } else {
                this.$message.warning(response.data.info);
              }
            })
            .catch(error => {
              this.loadSureAdd = false;
              this.addWeaponVisible = false;
              this.$message.error(error.message);
            });
        } else {
          this.$message.error("请完善各项内容");
          return false;
        }
      });
    },
    // 下载单个武器
    downLoadSinWeapon(row) {
      const a = document.createElement("a");
      a.href =
        "http://192.168.8.243:8100/api/resource/weapon/download/?id=" +
        row.id +
        "&token=" +
        this.$store.getters.token;
      a.download = row.weapon_name;
      document.querySelector("body").appendChild(a);
      a.click();
      document.querySelector("body").removeChild(a);
    },
    // 查看文件详情
    checkSinWeapon(row, type) {
      if (type === "detail") {
        this.typeIsDet = true;
        this.sinWeaponDetail = row;
      } else {
        this.typeIsDet = false;
        window.sessionStorage.setItem("typefile", "weapon");
        this.firstState++;
        this.taskId = row.cuckoo_task_id;
      }
      this.detailName = row.weapon_name;
      this.detailDrawer = true;
    },
    // 保存武器
    saveSinWeapon(row) {
      const sd = {
        id: row.id,
        cuckoo_task_id: row.cuckoo_task_id
      };
      weaponFileSave(sd)
        .then(response => {
          if (response.data.success) {
            this.checkFourth();
            // this.$set(row, "isTrue", 1);
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    // 关键词搜索
    enterCheck(val) {
      if (val == "") {
        this.page = 1;
        this.pageSize = 10;
        this.changeView();
      }
    },
    clickCheck() {
      if (this.search != "") {
        this.page = 1;
        this.changeView();
      }
    },
    // 分页
    handleSizeChange(val) {
      this.pageSize = val;
      this.changeView();
    },
    handleCurrentChange(val) {
      this.page = val;
      this.changeView();
    },
    // 详情抽屉关键词搜索
    enterDetailCheck(val) {
      if (val == "") {
        this.drawerPage = 1;
        this.drawerPageSize = 10;
        this.changeDetailView();
      }
    },
    checkDetailResult() {
      if (this.detailSearch != "") {
        this.drawerPage = 1;
        this.changeDetailView();
      }
    },
    // 分页
    detailSizeChange(val) {
      this.drawerPageSize = val;
      this.changeDetailView();
    },
    detailCurrentChange(val) {
      this.drawerPage = val;
      this.changeDetailView();
    },
    // 详情切换
    changeDetailView() {
      if (this.activeName === "second") {
        this.checkModalDetail();
      } else {
        this.checkLinkDetail();
      }
    }
  }
};
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.sourceView {
  height: 100%;
  padding: 30px 30px 20px;
  background: #fff;
  position: relative;
  .mainTop {
    margin-bottom: 10px;
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
    height: calc(100% - 41px);
    position: relative;
    .firstMainView {
      height: 100%;
      padding: 20px;
      .title {
        margin: 0 0 20px 0;
      }
      #leftCircle {
        width: 50%;
        height: 250px;
        float: left;
      }
      #rightCircle {
        width: 50%;
        height: 250px;
        float: left;
      }
      .sin {
        margin-top: 50px;
        padding: 40px;
        font-family: "strong";
        text-align: center;
        border-radius: 10px;
        cursor: pointer;
        .numCon {
          font-size: 40px;
          color: #1377ff;
          line-height: 60px;
        }
        .totalNum {
          color: #94969a;
        }
        &:hover {
          background: #f0f2f5;
        }
      }
    }
  }
}
</style>
<style rel="stylesheet/scss" lang="scss">
.sourceView {
  .mainList {
    .el-tabs {
      height: 100%;
      .el-tabs__header {
        .el-tabs__nav-wrap {
          padding-left: 25px;
          .el-tabs__active-bar {
            width: 40px !important;
            left: 24px;
            height: 5px;
            border-radius: 5px;
          }
          .el-tabs__item {
            font-size: 22px;
            box-shadow: none;
            height: 60px;
            line-height: 60px;
          }
        }
      }
      .el-tabs__content {
        height: calc(100% - 60px);
        .el-tab-pane {
          height: 100%;
        }
        .firstPane {
          .firstMainView {
            .el-table {
              .el-table__body {
                .el-table__row {
                  height: 34px;
                  line-height: 34px;
                  td {
                    padding: 0;
                  }
                }
              }
            }
          }
        }
        .otherPane {
          height: calc(100% - 60px);
          .weaponTable {
            height: calc(100% - 53px);
          }
        }
      }
    }
    .topPos {
      z-index: 5;
      position: absolute;
      right: 0px;
      top: 0;
      .hostPos {
        float: left;
        width: 45%;
        margin-right: 5%;
        .el-input__inner {
          height: 42px;
          line-height: 42px;
          border-radius: 42px;
        }
      }
      .searchBoxPos {
        float: right;
      }
    }
    .pageShowStyle {
      padding: 0;
      position: absolute;
      right: 80px;
      bottom: 0px;
      z-index: 5;
    }
  }
  .searchPos {
    z-index: 5;
    width: 10%;
    position: absolute;
    right: 80px;
    top: 120px;
  }
}
</style>
