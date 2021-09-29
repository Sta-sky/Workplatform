<template>
  <div
    class="knowView"
    v-loading="listLoading"
    element-loading-text="数据加载中"
    element-loading-background="rgba(0, 0, 0, 0.6)"
  >
    <div class="mainTop">
      <el-row style="margin-bottom: 8px;" :gutter="20">
        <el-col :span="20">
          <span class="englishView">知识库</span>
          <img src="@/assets/img/knowledge_base.png" alt="" />
        </el-col>
        <el-col :span="4">
          <el-input
            class="searchinput"
            placeholder="输入搜索内容"
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
      <div class="mainCenter">
        <el-row :gutter="20" style="height:100%">
          <el-col :span="3" style="height:100%">
            <el-tree
              ref="tree"
              node-key="id"
              :data="treeData"
              :props="treeProps"
              :expand-on-click-node="false"
              style="margin-top:22px;height:100%"
              class="scrollStyle treeSty"
              :default-expand-all="true"
              :highlight-current="true"
              @node-click="nodeClick"
            >
              <span class="custom-tree-node" slot-scope="{ node }">
                <span style="color:#000;font-weight:bold"
                  >{{ node.label }}
                </span>
              </span>
            </el-tree>
          </el-col>
          <el-col class="colMain" :span="21">
            <span class="taskName">{{ currentName }}</span>
            <div class="table">
              <el-table
                :data="tableData"
                v-if="!noDataIs"
                border
                class="taskTable scrollStyle"
                style="width: 100%;"
              >
                <el-table-column
                  prop="note_name"
                  label="名称"
                  show-overflow-tooltip
                >
                </el-table-column>
                <el-table-column
                  prop="classify"
                  label="分类"
                  show-overflow-tooltip
                >
                  <template slot-scope="scope">{{
                    scope.row.classify === 1 ? "MARKDOWN" : "富文本"
                  }}</template>
                </el-table-column>
                <el-table-column
                  prop="label"
                  label="标签"
                  show-overflow-tooltip
                >
                </el-table-column>
                <el-table-column
                  prop="create_user"
                  label="创建人"
                  show-overflow-tooltip
                >
                </el-table-column>
                <el-table-column
                  prop="create_time"
                  label="创建时间"
                  show-overflow-tooltip
                >
                </el-table-column>
                <el-table-column label="操作" width="200">
                  <template slot-scope="scope">
                    <el-button
                      title="查看"
                      class="sinProBtn detailBtn"
                      @click="taskDetail(scope.row)"
                    >
                      查看
                    </el-button>
                    <el-button
                      title="删除"
                      v-if="$store.getters.roles === 'admin'"
                      class="sinProBtn delBtn"
                      @click="taskDel(scope.row)"
                    >
                      删除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
              <div class="pageShowStyle" v-if="!noDataIs">
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
              <div class="noDataIs" v-if="noDataIs">
                <img src="@/assets/img/noData.png" alt="" />
                <p>暂无数据</p>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
    <!--笔记详情模抽屉-->
    <el-drawer
      :visible.sync="taskDeteilDrawer"
      class="taskDetailDrawer"
      size="80%"
      :withHeader="false"
      :close-on-press-escape="false"
    >
      <div
        style="height:100%;"
        v-loading="detailLoading"
        element-loading-text="数据加载中"
        element-loading-background="rgba(0, 0, 0, 0.6)"
      >
        <div class="allDetailBox">
          <div class="addModalTop">
            <span class="englishView">笔记详情</span>
            <img src="@/assets/img/note_details.png" alt="" />
          </div>
          <div class="mainBox" v-show="!editNote">
            <div class="title">
              <span class="noteTitle"
                >{{ currentName + "  /  "
                }}<a style="font-size:30px;color:#000">{{
                  curRowData.note_name
                }}</a></span
              >
              <span class="share">创建者：{{ curRowData.create_user }}</span>
              <span class="classify">{{
                curRowData.classify === 1 ? "MARKDOWN" : "富文本"
              }}</span>
              <span class="label">{{ curRowData.label }}</span>
              <span class="createTime">{{ curRowData.create_time }}</span>
              <el-button
                class="btn"
                type="success"
                :loading="editLoading"
                v-if="$store.getters.roles === 'admin'"
                @click="noteEdit"
                >编辑笔记&nbsp;&nbsp;<i class="el-icon-edit"></i
              ></el-button>
              <!-- <el-button
                class="btn1"
                style="right:390px"
                type="danger"
                @click="cancelEdit"
                >取消编辑&nbsp;&nbsp;<i class="el-icon-delete"></i
              ></el-button> -->
              <el-button
                class="btn1"
                v-if="$store.getters.roles === 'admin'"
                type="danger"
                @click="taskDel(curRowData)"
                >删除笔记&nbsp;&nbsp;<i class="el-icon-delete"></i
              ></el-button>
            </div>
            <el-row
              :gutter="40"
              style="height:calc(100% - 120px);margin-top:50px;margin-left:0"
            >
              <el-col
                :span="16"
                style="padding:0;height:100%;border-radius:10px;background-color:#fff;margin-right:40px"
              >
                <div
                  class="content scrollStyle"
                  v-if="curRowData.type === 0"
                  v-html="curRowData.content"
                ></div>
                <div class="content scrollStyle" style="padding:0" v-else>
                  <mavon-editor
                    class="mavon detailEditor"
                    :boxShadow="true"
                    previewBackground="#fff"
                    :editable="false"
                    :navigation="false"
                    :subfield="false"
                    :autofocus="true"
                    defaultOpen="preview"
                    :toolbarsFlag="false"
                    v-model="curRowData.content"
                    ref="md1"
                  >
                  </mavon-editor>
                </div>
              </el-col>
              <el-col
                :span="7"
                style="height:100%;border-radius:10px;background-color:#fff"
              >
                <div class="taskdetails"><span>任务快照</span></div>
                <el-timeline class="timeContent scrollStyle">
                  <el-timeline-item
                    v-for="(item, i) in curRowData.details"
                    :key="i"
                    :timestamp="item.back_time"
                  >
                    <p class="timeTitle">
                      <span class="ttl">{{ item.back_user }}</span>
                      <span
                        class="ttr"
                        v-if="$store.getters.roles === 'admin'"
                        @click="versionView(item)"
                        >版本回退</span
                      >
                    </p>
                  </el-timeline-item>
                </el-timeline>
              </el-col>
            </el-row>
          </div>
          <div class="mainBox" v-show="editNote">
            <div class="title">
              <span class="noteTitle"
                >{{ currentName + "  /  " + curRowData.note_name + "  /  "
                }}<a style="font-size:30px;color:#000">编辑笔记</a></span
              >
              <el-button
                class="btn"
                type="success"
                :loading="saveeditLoading"
                @click="saveEdit"
                >保存编辑&nbsp;&nbsp;<i class="el-icon-edit"></i
              ></el-button>
              <el-button class="btn1" type="danger" @click="cancelEdit"
                >取消编辑&nbsp;&nbsp;<i class="el-icon-delete"></i
              ></el-button>
            </div>
            <el-row
              :gutter="40"
              style="height:calc(100% - 70px);margin:0;padding:0 30px"
            >
              <el-form
                :model="editForm"
                style="height:100%;padding-right:20px"
                :rules="editRules"
                class="scrollStyle editor"
                ref="editForm"
              >
                <el-row>
                  <el-col :span="12">
                    <el-form-item prop="note_name" label="笔记名称">
                      <el-input
                        v-model="editForm.note_name"
                        style="width:50%"
                      ></el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item prop="label" label="笔记标签">
                      <el-select
                        v-model="editForm.label_id"
                        placeholder="选择用户类型"
                        style="width:50%"
                      >
                        <el-option
                          v-for="item in userTypeList"
                          :key="item.id"
                          :label="item.name"
                          :value="item.id"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="12">
                    <el-form-item prop="classify" label="笔记内容">
                      <el-radio-group v-model="editForm.classify">
                        <el-radio-button :label="1">MARKDOWN</el-radio-button>
                        <el-radio-button :label="2"
                          >&nbsp;&nbsp;&nbsp;富&nbsp;&nbsp;&nbsp;&nbsp;文&nbsp;&nbsp;&nbsp;&nbsp;本&nbsp;&nbsp;&nbsp;</el-radio-button
                        >
                      </el-radio-group>
                    </el-form-item>
                    <!-- <el-form-item prop="belong_to_dir" label="笔记归属">
                      <el-select
                        v-model="editForm.belong_to_dir"
                        placeholder="请选择笔记归属"
                        style="width:50%"
                      >
                        <el-option
                          v-for="item in noteBelongList"
                          :key="item.name"
                          :label="item.name"
                          :value="item.name"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item> -->
                  </el-col>
                  <el-col :span="12">
                    <el-form-item prop="note_premission" label="可见权限">
                      <el-select
                        v-model="editForm.note_premission"
                        placeholder="请选择可见权限"
                        style="width:50%"
                      >
                        <el-option
                          v-for="item in notePermissionList"
                          :key="item.id"
                          :label="item.name"
                          :value="item.id"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-form-item prop="content" style="height:550px">
                  <tinymce
                    v-show="editForm.classify == 2"
                    ref="bzlc"
                    :height="550"
                    :id="'noteCreate'"
                    :tinyVal="editForm.content"
                  ></tinymce>
                  <!-- @imgDel="imgDel" -->
                  <mavon-editor
                    v-if="editForm.classify == 1"
                    class="mavon"
                    style="height:550px"
                    @imgAdd="imgAdd"
                    :boxShadow="true"
                    previewBackground="#f0f2f5"
                    :editable="true"
                    :navigation="true"
                    :subfield="true"
                    :autofocus="true"
                    defaultOpen="preview"
                    v-model="editForm.content"
                    ref="md"
                  >
                  </mavon-editor>
                </el-form-item>
              </el-form>
            </el-row>
          </div>
          <div @click="taskDeteilDrawer = false" class="closeBtn">
            <i class="el-icon-arrow-right"></i>
          </div>
        </div>
      </div>
    </el-drawer>
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
        dialogType === 0 ? "删除笔记" : "版本回退"
      }}</span>
      <p class="contentPsty">
        {{
          dialogType === 0
            ? "删除后可在任务快照恢复任务，确认删除笔记？"
            : "回退操作不可恢复，确认回退版本?"
        }}
        <!-- <span style="font-weight:600;padding-left:15px;">{{
          delCon
        }}</span
        > -->
      </p>
      <div slot="footer">
        <el-button
          @click="sureEdit"
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
    <!-- 回退预览 -->
    <el-dialog
      :visible.sync="versionBackVisible"
      class="addDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      width="30%"
      top="6%"
    >
      <div class="addMain">
        <div class="addTopbar" style="height: 40px;">
          <span class="englishView">回退预览</span>
          <img src="@/assets/img/img_VersionPreview.png" alt="" />
        </div>
        <div class="content scrollStyle" style="padding:0" v-if="versionCont">
          <mavon-editor
            class="mavon detailEditor"
            style="max-height:500px"
            :boxShadow="true"
            previewBackground="#fff"
            :editable="false"
            :navigation="false"
            :subfield="false"
            :autofocus="true"
            defaultOpen="preview"
            :toolbarsFlag="false"
            v-model="versionCont.content"
            ref="md2"
          >
          </mavon-editor>
        </div>
      </div>
      <div slot="footer" class="addFooter" style="padding-top:20px">
        <el-button
          @click="versionBack(versionRow)"
          class="btnSure"
          type="warning"
          >回 退</el-button
        >
        <el-button
          type="info"
          class="btnCancle"
          @click="versionBackVisible = false"
          >放 弃</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>
<script>
import {
  editState,
  noteedit,
  treeList,
  getTaskDetail,
  delNote,
  noteBack,
  usertypeList
  // getEnumList,
} from "@/api/knowledge";
// import { uploadImg, delImg } from "@/api/task";
import { uploadImg } from "@/api/task";
import tinymce from "./tinymce-editor";
export default {
  name: "knowledgeIndex",
  components: {
    tinymce
  },
  data() {
    return {
      listLoading: false,
      saveeditLoading: false,
      detailLoading: false,
      taskDeteilDrawer: false,
      curRowData: {},
      noDataIs: true,
      treeData: [],
      tableData: [],
      delVisible: false,
      loadSureDel: false,
      currentName: "",
      dialogType: 0,
      dialogData: {},
      // 回退预览
      versionBackVisible: false,
      versionCont: null,
      versionRow: null,
      treeProps: {
        children: "children",
        label: "title"
      },
      editRules: {
        note_name: [
          { required: true, message: "请输入笔记名称", trigger: "blur" }
        ],
        label: [
          { required: true, message: "选择用户类型", trigger: "blur change" }
        ],
        classify: [
          { required: true, message: "请选择笔记内容", trigger: "blur change" }
        ],
        // belong_to_dir: [
        //   { required: true, message: "请选择笔记归属", trigger: "blur change" }
        // ],
        note_premission: [
          { required: true, message: "请选择可见权限", trigger: "blur change" }
        ]
      },
      taskId: "",
      search: "",
      page: 1,
      page_size: 10,
      totalSize: 0,
      editNote: false,
      editForm: {
        note_name: "",
        label: "",
        label_id: "",
        belong_to_dir: "",
        note_premission: "",
        classify: 1,
        content: ""
      },
      notePermissionList: [
        {
          id: 0,
          name: "仅自己可见"
        },
        {
          id: 1,
          name: "任务参与人员可见"
        },
        {
          id: 2,
          name: "所有人可见"
        }
      ],
      noteBelongList: [],
      userTypeList: [],
      editLoading: false,
      interVal: null,
      adminUser: null
    };
  },
  watch: {
    taskDeteilDrawer(newVal, oldVal) {
      if (!newVal && oldVal) {
        this.cancelEdit();
      }
    }
  },
  mounted() {
    this.adminUser = this.$store.getters.roles === "admin" ? true : false;
    console.log(this.$route.query);
    this.getTreeList();
  },
  created() {
    window.addEventListener("visibilitychange", this.refresh);
  },
  methods: {
    refresh() {
      if (this.editNote) {
        this.cancelEdit();
      }
    },
    // 获取任务树
    getTreeList() {
      var data = {
        get_task: 1,
        keyword: ""
      };
      treeList(data)
        .then(res => {
          if (res.data.success) {
            this.treeData = res.data.data;
            if (res.data.data.length > 0) {
              let id = null;
              if (JSON.stringify(this.$route.query) !== "{}") {
                id = this.$route.query.taskId;
                this.currentName = this.$route.query.taskName;
                this.taskId = id;
              } else {
                id = res.data.data[0].id;
                this.currentName = res.data.data[0].title;
                this.taskId = id;
              }
              this.$nextTick(() => {
                this.$refs.tree.setCurrentKey(id);
                this.nodeClick(id);
              });
            }
          } else {
            this.$message.error("添加失败");
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
      usertypeList()
        .then(response => {
          if (response.data.success) {
            this.userTypeList = response.data.data;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    // 任务树节点点击事件
    nodeClick(val) {
      // if (val.hasOwnProperty("children")) {
      //   this.$refs.tree.setCurrentKey(this.taskId);
      // }
      if (JSON.stringify(this.$route.query) !== "{}") {
        this.search = this.$route.query.allSearch;
      } else {
        this.search = "";
      }
      var data = {
        get_task: 0,
        keyword: this.search,
        page: 1,
        max_count: 10,
        task_id: val
      };
      if (val.hasOwnProperty("id")) {
        this.currentName = val.title;
        data.task_id = val.id;
        // if (!val.hasOwnProperty("children")) {
        //   return false;
        // } else {
        //   this.currentName = val.name;
        // }
      }
      this.getTableList(data);
      this.taskId = data.task_id;
    },
    // 获取笔记列表
    getTableList(data) {
      this.listLoading = true;
      treeList(data)
        .then(res => {
          this.listLoading = false;
          if (res.data.success) {
            this.tableData = res.data.data;
            this.totalSize = res.data.total;
            this.noDataIs = res.data.data.length > 0 ? false : true;
          } else {
            this.$message.warning(res.data.info);
          }
        })
        .catch(() => {
          this.listLoading = false;
          // this.$message.error(error.message);
        });
    },
    // 列表详情
    taskDetail(row) {
      this.taskDeteilDrawer = true;
      this.detailLoading = true;
      this.curRowData = row;
      this.editNote = false;
      var data = { note_id: row.id };
      getTaskDetail(data)
        .then(res => {
          this.detailLoading = false;
          if (res.data.success) {
            this.$set(this.curRowData, "content", res.data.data.content);
            this.$set(this.curRowData, "details", res.data.data.back_info);
            this.editForm = res.data.data;
          } else {
            this.$message.warning(res.data.info);
          }
        })
        .catch(error => {
          this.detailLoading = false;
          this.$message.error(error.message);
        });
    },
    // content_type切换
    getEditForm() {
      var data = { note_id: this.curRowData.id };
      getTaskDetail(data)
        .then(res => {
          if (res.data.success) {
            this.editForm = res.data.data;
          } else {
            this.$message.warning(res.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    // 取消编辑
    cancelEdit() {
      this.editNote = false;
      var data = {
        task_id: this.taskId,
        note_id: this.curRowData.id,
        flag: 0
      };
      editState(data)
        .then(res => {
          console.log(res);
          // if (res.data.code === 200) {
          //   this.editNote = true;
          //   this.getEditForm();
          //   clearInterval(this.interVal);
          //   this.interVal = setInterval(() => {
          //     // 编辑5分钟后自动保存
          //     if (this.editNote) {
          //       this.saveEdit();
          //     }
          //   }, 300000);
          // } else {
          //   this.editLoading = false;
          //   this.$message.warning(res.data.info);
          // }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    // 编辑笔记
    noteEdit() {
      var data = {
        task_id: this.taskId,
        note_id: this.curRowData.id,
        flag: 1
      };
      this.editLoading = true;
      this.$set(this.editForm, "content", "");
      editState(data)
        .then(res => {
          this.editLoading = false;
          if (res.data.code === 200) {
            this.editNote = true;
            this.getEditForm();
            clearInterval(this.interVal);
            this.interVal = setInterval(() => {
              // 编辑5分钟后自动保存
              if (this.editNote) {
                this.saveEdit();
              }
            }, 300000);
          } else {
            this.editLoading = false;
            this.$message.warning(res.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    // 保存编辑
    saveEdit() {
      this.$refs["editForm"].validate(valid => {
        if (valid) {
          this.saveeditLoading = true;
          var data = {
            note_id: this.curRowData.id,
            content:
              this.editForm.classify === 1
                ? this.editForm.content
                : this.$refs.bzlc.release(),
            note_name: this.editForm.note_name,
            label: this.editForm.label_id,
            belong_to_dir: "",
            // belong_to_dir: this.editForm.belong_to_dir,
            note_premission: this.editForm.note_premission,
            classify: this.editForm.classify
          };
          noteedit(data)
            .then(res => {
              this.saveeditLoading = false;
              this.editNote = false;
              this.taskDeteilDrawer = false;
              if (res.data.success) {
                this.$message.success("修改笔记成功");
                this.getTreeList();
              } else {
                this.$message.error(res.data.info);
              }
            })
            .catch(error => {
              this.saveeditLoading = false;
              this.editNote = false;
              this.taskDeteilDrawer = false;
              this.$message.error(error);
            });
        } else {
          this.$message.warning("请完善信息后保存");
        }
      });
    },
    versionView(val) {
      this.versionRow = val;
      this.versionBackVisible = true;
      var data = {
        note_id: this.curRowData.id,
        back_time: this.versionRow.back_time,
        flag: 1
      };
      noteBack(data)
        .then(res => {
          if (res.data.success) {
            this.versionCont = res.data.data;
          } else {
            this.$message.warning(res.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    imgAdd(pos, $file) {
      // 第一步.将图片上传到服务器.
      let formdata = new FormData();
      formdata.append("images", $file);
      uploadImg(formdata).then(res => {
        if (res.data.success) {
          let json = "http://127.0.0.1:10000" + res.data.img_addr; //取出上传成功后的url
          if (this.editNote) {
            this.$refs.md.$imglst2Url([[pos, json]]);
          } else {
            this.$refs.md1.$imglst2Url([[pos, json]]);
          }
        } else {
          this.$message("上传失败");
        }
      });
    },
    // imgDel(pos) {
    //   let arr = pos[0].split("/images/");
    //   delImg({ img: arr[1] }, this.$store.getters.token)
    //     .then(() => {
    //       this.$message.success("删除成功");
    //     })
    //     .catch(res => {
    //       console.log(res);
    //     });
    // },
    // 版本回退
    versionBack(val) {
      this.dialogType = 1;
      this.dialogData = val;
      this.delVisible = true;
    },
    // 笔记删除
    taskDel(row) {
      this.curRowData = row;
      this.dialogType = 0;
      this.dialogData = row;
      this.delVisible = true;
    },
    // 弹出框确认点击
    sureEdit() {
      this.loadSureDel = true;
      if (this.dialogType === 0) {
        // 删除笔记
        delNote(this.dialogData.id)
          .then(res => {
            this.loadSureDel = false;
            if (res.data.success) {
              this.$message.success("删除成功");
              this.handleSizeChange(10);
            } else {
              this.$message.warning(res.data.info);
            }
            this.taskDeteilDrawer = false;
            this.delVisible = false;
          })
          .catch(error => {
            this.loadSureDel = false;
            this.delVisible = false;
            this.$message.error(error.message);
          });
      } else {
        // 版本回退
        var data = {
          note_id: this.curRowData.id,
          back_time: this.dialogData.back_time,
          flag: 2
        };
        noteBack(data)
          .then(res => {
            this.loadSureDel = false;
            this.versionBackVisible = false;
            if (res.data.success) {
              this.$message.success("回退成功");
              this.handleSizeChange(10);
            } else {
              this.$message.warning(res.data.info);
            }
            this.taskDeteilDrawer = false;
            this.delVisible = false;
          })
          .catch(error => {
            this.loadSureDel = false;
            this.versionBackVisible = false;
            this.delVisible = false;
            this.$message.error(error.message);
          });
      }
    },
    // 搜索
    handleClick() {
      var data = {
        get_task: 0,
        keyword: "",
        page: this.page,
        max_count: this.page_size,
        task_id: this.taskId
      };
      this.search = "";
      this.getTableList(data);
    },
    // 关键词搜索
    enterCheck(val) {
      if (val == "") {
        this.handleClick();
      }
    },
    clickCheck(val) {
      var data = {
        get_task: 0,
        keyword: this.search,
        page: this.page,
        max_count: this.page_size,
        task_id: this.taskId
      };
      if (val !== "") {
        this.page = 1;
        this.getTableList(data);
      }
    },
    // 分页
    handleSizeChange(val) {
      this.page_size = val;
      var data = {
        get_task: 0,
        keyword: this.search,
        page: this.page,
        max_count: this.page_size,
        task_id: this.taskId
      };
      this.getTableList(data);
    },
    handleCurrentChange(val) {
      this.page = val;
      var data = {
        get_task: 0,
        keyword: this.search,
        page: val,
        max_count: this.page_size,
        task_id: this.taskId
      };
      this.getTableList(data);
    },
    beforeunloadFn() {
      // todo
    }
  },
  beforeDestroy() {
    clearInterval(this.interVal);
    if (this.editNote) {
      this.cancelEdit();
    }
  },
  destroyed() {
    window.addEventListener("visibilitychange", this.refresh());
  }
};
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.knowView {
  height: 100%;
  padding: 30px 30px 20px;
  border-radius: 20px;
  background: #fff;
  .mainTop {
    height: 100%;
    .mainCenter {
      margin-top: 20px;
      height: calc(100% - 60px);
      position: relative;
      .colMain {
        height: 100%;
        border-radius: 20px;
        background-color: #f5f6fa;
        padding: 20px 40px !important;
        .taskName {
          font-size: 20px;
          margin-bottom: 20px;
          color: #000;
          float: left;
        }
        .table {
          height: 100%;
          .taskTable {
            height: calc(100% - 70px);
            border-radius: 10px;
            .detailBtn {
              background-color: #434be0;
              color: #fff;
              &:hover {
                background-color: #1b26e8;
                color: #fff;
              }
            }
            &::-webkit-scrollbar {
              width: 6px;
            }
          }
          .noDataIs {
            position: absolute;
            left: calc(50% - 64px);
            top: calc(70% - 184px);
            width: 128px;
            height: 148px;
            text-align: center;
            i {
              font-size: 100px;
              color: #3a88e7;
            }
          }
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
  .taskDetailDrawer {
    .allDetailBox {
      .mainBox {
        position: relative;
        width: 100%;
        padding: 20px;
        height: calc(100% - 90px);
        background-color: #eef0f7;
        border-radius: 20px;
        .title {
          height: 8%;
          line-height: 28px;
          width: 100%;
          .btn {
            position: absolute;
            right: 236px;
            width: 10%;
            top: 0;
            background-color: #3d46dc;
            box-shadow: 1px 4px 16px #3d46dc;
            &:hover {
              background-color: #535be0;
            }
          }
          .btn1 {
            position: absolute;
            right: 50px;
            width: 10%;
            top: 0;
            box-shadow: 1px 4px 16px #f95c6d;
          }
          span {
            display: inline-block;
            margin-right: 10px;
          }
          .noteTitle {
            font-size: 16px;
            color: #cacbcd;
            font-weight: 100;
            display: block;
            margin-bottom: 20px;
          }
          .share {
            height: 28px;
            border-radius: 28px;
            padding: 0 20px;
            font-size: 15px;
            border: 1px solid #8dc3f5;
            color: #2891f0;
          }
          .classify {
            height: 28px;
            border-radius: 28px;
            padding: 0 20px;
            border: 1px solid #8de4e1;
            font-size: 15px;
            color: #28d2c9;
          }
          .label {
            height: 28px;
            border-radius: 28px;
            padding: 0 20px;
            font-size: 15px;
            border: 1px solid #89e0b5;
            color: #62d79b;
          }
          .createTime {
            height: 28px;
            border-radius: 28px;
            font-size: 15px;
            padding: 0 20px;
            border: 1px solid #8de4e1;
            color: #28d2c9;
          }
        }
        .editor {
          height: 100%;
          padding-right: 20px;
          &::-webkit-scrollbar {
            width: 6px;
          }
        }
        .content {
          height: 100%;
          padding: 20px;
          font-size: 22px;
        }
        .taskdetails {
          margin-bottom: 40px;
          width: 100%;
          float: left;
          padding: 20px 0 0 0px;
          span {
            color: #000;
            font-size: 25px;
            font-weight: 100;
          }
        }
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
.knowView {
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
      background-color: #555fee;
    }
    .mainCenter {
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
      .el-tree-node__content > .el-tree-node__expand-icon::before {
        content: "";
      }
      .el-tree--highlight-current
        .el-tree-node.is-current
        > .el-tree-node__content {
        border-radius: 13px;
        background-color: #edeef2;
        color: #000;
        padding-left: 10px !important;
      }
      .el-tree-node > .el-tree-node__children {
        margin-top: 7px;
        .el-tree-node.is-current > .el-tree-node__content {
          border-radius: 13px;
          background-color: #edeef2;
          color: #000;
        }
      }
      .el-tree-node__content {
        margin-bottom: 20px;
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
    }
  }
  .el-dialog {
    border-radius: 30px;
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
  .taskDetailDrawer {
    .allDetailBox {
      height: 100%;
      padding: 50px 70px 20px 70px;
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
      .mainBox {
        .timeContent {
          padding-left: 20px;
          margin-top: 40px;
          height: calc(100% - 90px);
          .el-timeline-item {
            padding-bottom: 50px;
            .timeTitle {
              color: #696e80;
              .ttl {
                display: inline-block;
                width: 200px;
                font-size: 17px;
                font-weight: bold;
                overflow: hidden;
                white-space: nowrap;
                text-overflow: ellipsis;
              }
              .ttr {
                display: inline-block;
                margin-top: 10px;
                float: right;
                margin-right: 20px;
                line-height: 0px;
                padding: 10px;
                cursor: pointer;
                border-radius: 28px;
                border: 1px solid #434be0;
                color: #434be0;
                font-family: "light";
                font-size: 12px;
              }
            }
            .el-timeline-item__timestamp {
              color: #636469;
              font-family: "light";
            }
          }
          &::-webkit-scrollbar {
            width: 5px;
          }
        }
        .editor {
          .el-form-item__label,
          .el-input__inner {
            color: #222222;
            font-weight: bold;
          }
          // .v-note-wrapper .v-note-panel .v-note-navigation-wrapper {
          //   left: 0 !important;
          //   position: absolute;
          //   width: 20%;
          //   .v-note-navigation-title .v-note-navigation-close {
          //     display: none;
          //   }
          // }
          .auto-textarea-wrapper .auto-textarea-input {
            background-color: #f0f2f5;
          }
          // .v-note-edit {
          //   position: absolute;
          //   left: 20%;
          //   width: 40%;
          //   height: 100%;
          //   .content-input-wrapper {
          //     min-height: 100%;
          //     background-color: #f0f2f5 !important;
          //   }
          // }
          // .v-note-wrapper .v-note-panel .v-note-show .v-show-content,
          // .v-note-wrapper .v-note-panel .v-note-show .v-show-content-html {
          //   position: absolute;
          //   right: 0;
          //   background-color: #f0f2f5;
          //   width: 40%;
          //   padding: 8px 45px 15px 25px;
          // }
        }
        .content {
          .detailEditor {
            height: 100%;
            border-radius: 50px;
            // .v-note-edit {
            //   display: none;
            // }
            // .v-note-wrapper .v-note-panel .v-note-show {
            //   flex: 1;
            // }
            // .v-note-show {
            //   flex: 1;
            //   width: 100%;
            //   border-radius: 10px;
            //   padding: 15px;
            // }
          }
        }
        &::-webkit-scrollbar {
          width: 5px;
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
      .suerBtnSaveChange {
        margin-top: 60px;
        border-radius: 36px;
        background-image: linear-gradient(to right, #56a5fe, #3e7bec);
      }
    }
  }
}
</style>
