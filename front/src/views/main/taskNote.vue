<template>
  <el-row :gutter="20" style="height:100%;">
    <el-col :span="5" class="directoryTree">
      <el-tree
        class="filesTree"
        ref="structure"
        node-key="id"
        :load="noteTreeLoadNode"
        :props="noteTreeProps"
        icon-class="el-icon-arrow-right"
        lazy
        @node-click="handleNodeClick"
        :highlight-current="true"
      >
        <span slot-scope="{ node }">
          <span>
            <i class="iconfont icon-wenjianjia"></i>{{ node.label }}
          </span>
        </span>
      </el-tree>
    </el-col>
    <el-col :span="19" class="fileTableBox" v-loading="detailGetLoading">
      <div class="dnoteList" v-if="notesListShow && !noteSearchState">
        <div class="task_filter">
          <span class="title">{{ node_name }}</span>
          <div class="pull_right">
            <el-button size="small" class="lookAtLog" @click="noteLogLook" round
              >查看日志 <i class="el-icon-circle-plus-outline"></i>
            </el-button>
            <el-button
              size="small"
              class="addDirectory"
              @click="addDirectory('add')"
              round
              >新增目录 <i class="el-icon-circle-plus-outline"></i>
            </el-button>
            <el-button
              size="small"
              class="addDirectory"
              v-if="node_name !== '根目录'"
              @click="addDirectory('edit')"
              round
              >编辑目录 <i class="el-icon-circle-plus-outline"></i>
            </el-button>
            <el-button
              size="small"
              class="addNote"
              v-if="node_name !== '根目录'"
              @click="addNote"
              round
              >新增笔记 <i class="el-icon-circle-plus-outline"></i>
            </el-button>
            <el-button
              size="small"
              class="addNote"
              v-if="node_name !== '根目录'"
              @click="noteUploadVisible = true"
              round
              >导入笔记 <i class="el-icon-circle-plus-outline"></i>
            </el-button>
            <el-button
              size="small"
              class="delNote"
              v-if="node_name !== '根目录'"
              @click="delDirectory"
              round
              >删除目录 <i class="el-icon-circle-plus-outline"></i>
            </el-button>
          </div>
        </div>
        <div
          class="scrollStyle"
          v-if="detailNoData"
          style="height: calc(100% - 90px);"
        >
          <div
            class="sinNote"
            v-for="(item, i) in taskNotesArr"
            :key="i"
            @click="checkSinNote(item)"
          >
            <p class="title">
              <img src="@/assets/img/wendang.png" alt="" />
              <el-tooltip
                class="item"
                effect="dark"
                :content="item.note_name"
                placement="top"
              >
                <span class="name">{{ item.note_name | beautySub(8) }}</span>
              </el-tooltip>
            </p>
            <p class="graph">{{ item.content }}</p>
            <div class="btm">
              <el-tooltip
                class="item"
                effect="dark"
                v-if="item.parentLabel"
                :content="item.parentLabel"
                placement="top"
              >
                <div class="tag_one" v-if="item.parentLabel">
                  {{ item.parentLabel | beautySub(3) }}
                </div>
              </el-tooltip>
              <div class="tag_two">
                {{ item.classify === 1 ? "markdown" : "富文本" }}
              </div>
              <el-tooltip
                class="item"
                effect="dark"
                :content="item.label"
                placement="top"
              >
                <div class="tag_three">{{ item.label | beautySub(4) }}</div>
              </el-tooltip>
            </div>
          </div>
        </div>
        <div class="detailNoDataIs" v-if="!detailNoData">
          <img src="@/assets/img/noData.png" alt="" />
          <p>暂无数据</p>
        </div>
        <div class="pageStyle" v-if="detailNoData">
          <el-pagination
            class="pageShowView"
            @size-change="detailSizeChange"
            @current-change="detailCurrentChange"
            :current-page="detailPage"
            :page-sizes="[10, 25, 50, 100]"
            :page-size="detailSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="detailTotalSize"
          >
          </el-pagination>
        </div>
      </div>
      <div class="dnoteDetail" v-if="!notesListShow">
        <div class="mainBox" v-if="!editNote">
          <div class="title">
            <div class="one_level">
              <span class="noteTitle"
                >{{ currentName + "  /  "
                }}<a style="font-size:30px;color:#000">{{
                  curRowData.note_name
                }}</a></span
              >
              <div class="pull_right">
                <el-button
                  size="small"
                  class="exportBtn"
                  @click="noteOutsideVisible = true"
                  round
                  >导出笔记 <i class="iconfont icon-daochu"></i>
                </el-button>
                <el-button
                  size="small"
                  class="editBtn"
                  :loading="editLoading"
                  @click="noteEdit(1)"
                  round
                  >编辑笔记 <i class="el-icon-edit"></i>
                </el-button>
                <el-button
                  size="small"
                  class="delBtn"
                  @click="taskDel(curRowData)"
                  round
                  >删除笔记 <i class="el-icon-delete"></i>
                </el-button>
              </div>
            </div>
            <div class="two_level">
              <span class="share">创建者：{{ curRowData.user }}</span>
              <span class="power">{{
                curRowData.note_premission === 0
                  ? "仅自己可见"
                  : curRowData.note_premission === 1
                  ? "任务内部成员可见"
                  : "公开"
              }}</span>
              <el-tooltip
                class="item"
                effect="dark"
                v-if="curRowData.belong_to_dir !== undefined"
                :content="curRowData.belong_to_dir"
                placement="top"
              >
                <span
                  class="directory"
                  v-if="curRowData.belong_to_dir !== undefined"
                  >{{ curRowData.belong_to_dir | beautySub(8) }}</span
                >
              </el-tooltip>
              <span class="classify">{{
                curRowData.classify === 1 ? "markdown" : "富文本"
              }}</span>
              <span class="label">{{ curRowData.label }}</span>
              <span class="createTime">{{ curRowData.create_time }}</span>
            </div>
          </div>
          <el-row
            :gutter="40"
            style="height:calc(100% - 120px);margin-top:50px;margin-left:0"
          >
            <el-col
              :span="15"
              style="padding:0;height:100%;border-radius:10px;background-color:#fff;margin-right:20px"
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
              :span="8"
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
                    <el-tooltip
                      class="item"
                      effect="dark"
                      :content="item.back_user"
                      placement="top"
                    >
                      <span class="ttl">{{ item.back_user }}</span>
                    </el-tooltip>
                    <span class="ttr" @click="versionView(item)">版本回退</span>
                  </p>
                </el-timeline-item>
              </el-timeline>
            </el-col>
          </el-row>
        </div>
        <!-- <div class="mainBox" v-else>
          <div class="title">
            <div class="one_level">
              <span class="noteTitle"
                >{{ currentName + "  /  " + curRowData.note_name + "  /  "
                }}<a style="font-size:30px;color:#000">编辑笔记</a></span
              >
              <div class="pull_right">
                <el-button
                  size="small"
                  class="editBtn"
                  :loading="saveeditLoading"
                  @click="saveEdit"
                  round
                  >保存编辑 <i class="el-icon-edit"></i>
                </el-button>
                <el-button
                  size="small"
                  class="delBtn"
                  @click="noteEdit(0)"
                  round
                  >取消编辑 <i class="el-icon-delete"></i>
                </el-button>
              </div>
            </div>
          </div>
          <el-row
            :gutter="40"
            style="height:calc(100% - 30px);margin:0;padding:0 30px"
          >
            <el-form
              :model="editForm"
              style="height:100%"
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
                      v-model="editForm.label"
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
                    <el-tooltip
                      class="item"
                      effect="dark"
                      content="管理标签"
                      placement="top"
                    >
                      <el-button
                        style="background:#434be0;border-color: #434be0;color:#fff;padding: 10px 12px;margin-left:10px;"
                        icon="el-icon-s-tools"
                        @click="manageTags"
                      ></el-button>
                    </el-tooltip>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item prop="classify" label="笔记内容">
                    <el-radio-group
                      text-color="#ffffff"
                      fill="#3b44db"
                      v-model="editForm.classify"
                    >
                      <el-radio-button :label="1">MARKDOWN</el-radio-button>
                      <el-radio-button :label="2"
                        >&nbsp;&nbsp;&nbsp;富&nbsp;&nbsp;&nbsp;&nbsp;文&nbsp;&nbsp;&nbsp;&nbsp;本&nbsp;&nbsp;&nbsp;</el-radio-button
                      >
                    </el-radio-group>
                  </el-form-item>
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
              <el-form-item prop="content" style="height:410px">
                <tinymce
                  v-show="editForm.classify == 2"
                  ref="bzlc"
                  :height="410"
                  :id="'noteEdit'"
                  :tinyVal="editForm.content"
                ></tinymce>
                <mavon-editor
                  v-show="editForm.classify == 1"
                  class="mavon"
                  style="height:410px"
                  :boxShadow="true"
                  previewBackground="#f0f2f5"
                  :editable="true"
                  :navigation="true"
                  :subfield="true"
                  :autofocus="true"
                  defaultOpen="preview"
                  :toolbarsFlag="false"
                  v-model="editForm.content"
                  ref="md"
                >
                </mavon-editor>
              </el-form-item>
            </el-form>
          </el-row>
        </div> -->
      </div>
      <div class="searchDetail" v-if="noteSearchState">
        <ul class="searchCard scrollStyle">
          <li
            v-for="item in noteSearchList"
            :key="item.id"
            class="searchItem"
            @click="checkSinNote(item)"
          >
            <el-col :span="12">
              <div>
                <strong>笔记名称: </strong>
                <span v-html="item.note_name"></span>
              </div>
            </el-col>
            <el-col :span="12">
              <div><strong>笔记归属: </strong>{{ item.file_dir }}</div>
            </el-col>
            <el-col :span="24">
              <div>
                <strong>笔记内容: </strong>
                <span v-html="item.content"></span>
              </div>
            </el-col>
            <el-col :span="24" class="level">
              <span class="power">{{
                item.note_premission === 0
                  ? "仅自己可见"
                  : item.note_premission === 1
                  ? "任务内部成员可见"
                  : "公开"
              }}</span>
              <span class="classify">{{
                item.classify === 1 ? "markdown" : "富文本"
              }}</span>
              <span class="label">{{ item.label }}</span>
            </el-col>
            <el-button title="详情" class="detailBtn" icon="el-icon-right">
              详情
            </el-button>
          </li>
          <div class="pagePortStyle">
            <el-pagination
              @size-change="searchSizeChange"
              @current-change="searchCurrentChange"
              :current-page="search_page"
              :page-sizes="[10, 25, 50, 100]"
              :page-size="search_page_size"
              layout="total, sizes, prev, pager, next, jumper"
              :total="searchTotalSize"
            >
            </el-pagination>
          </div>
        </ul>
      </div>
    </el-col>
    <!-- 标签管理 -->
    <el-dialog
      :visible.sync="tagsListVisible"
      class="addDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      width="30%"
      top="6%"
    >
      <div class="addMain" style="padding-bottom:40px;">
        <div class="addTopbar">
          <span class="englishView" style="margin-top: -20px">标签列表</span>
        </div>
        <div style="text-align: right;">
          <el-button
            title="新增"
            type="primary"
            size="small"
            style="height:32px;padding:8px 18px;margin:10px 0;background-image: linear-gradient(to right, #5861f0, #3b44db);border-color:#5861f0;"
            icon="el-icon-circle-plus-outline"
            @click.native="addTagLabel"
            round
            >新增标签</el-button
          >
        </div>
        <el-table
          :data="userTypeList"
          :header-cell-style="{ color: '#333', 'font-size': '16px' }"
          style="width: 100%"
          class="scrollStyle"
          max-height="50vh"
        >
          <el-table-column label="序号" width="60" type="index">
          </el-table-column>
          <el-table-column prop="name" label="标签名称"> </el-table-column>
          <el-table-column label="操作" width="120">
            <template slot-scope="scope">
              <el-button
                title="删除"
                class="sinProBtn delBtn"
                @click="delTags(scope.row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>
    <!-- 新增标签 -->
    <el-dialog
      :visible.sync="addTagsVisible"
      class="addDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      width="30%"
      top="6%"
    >
      <div class="addMain">
        <div class="addTopbar">
          <span class="englishView">新增标签</span>
          <img src="@/assets/img/new_files.png" alt="" />
        </div>
        <el-form label-width="100px" class="weaponForm">
          <el-form-item label="标签名称">
            <el-input v-model="tag_name"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer" class="addFooter">
        <el-button
          @click="addTagSubmit"
          type="primary"
          class="sureBtn"
          :loading="loadtagSure"
          >确认新增</el-button
        >
      </div>
    </el-dialog>
    <!-- 新增&编辑目录 -->
    <el-dialog
      :visible.sync="addDirectoryVisible"
      class="addDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      width="30%"
      top="6%"
    >
      <div class="addMain">
        <div class="addTopbar">
          <span class="englishView">{{
            directory_type === "add" ? "新增目录" : "编辑目录"
          }}</span>
          <img
            :src="
              directory_type === 'add'
                ? require('@/assets/img/new_catalog.png')
                : require('@/assets/img/edit_catalog.png')
            "
            alt=""
          />
        </div>
        <el-form label-width="100px" class="weaponForm">
          <el-form-item label="目录名称" prop="description">
            <el-input v-model="directory_name"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer" class="addFooter">
        <el-button
          @click="addDirSubmit"
          type="primary"
          class="sureBtn"
          :loading="loadDirSure"
          >{{ directory_type === "add" ? "确认新增" : "确认修改" }}</el-button
        >
      </div>
    </el-dialog>
    <!-- 新增笔记 -->
    <el-dialog
      :visible.sync="addNoteVisible"
      class="addDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      width="70%"
      top="3%"
    >
      <div class="addMain">
        <div class="addTopbar">
          <span class="englishView">新增笔记</span>
          <img src="@/assets/img/new_files.png" alt="" />
        </div>
        <el-form
          :model="editForm"
          style="height:100%;max-height: calc(86vh - 160px);margin-top: 30px;"
          :rules="editRules"
          class="scrollStyle editor"
          ref="forms"
        >
          <el-row>
            <el-col :span="12">
              <el-form-item prop="note_name" label="笔记名称">
                <el-input
                  v-model="editForm.note_name"
                  style="width:70%"
                ></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item prop="label" label="笔记标签">
                <el-select
                  v-model="editForm.label"
                  placeholder="选择用户类型"
                  style="width:70%"
                >
                  <el-option
                    v-for="item in userTypeList"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                  >
                  </el-option>
                </el-select>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="管理标签"
                  placement="top"
                >
                  <el-button
                    style="background:#434be0;border-color: #434be0;color:#fff;padding: 10px 12px;margin-left:10px;"
                    icon="el-icon-s-tools"
                    @click="manageTags"
                  ></el-button>
                </el-tooltip>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item prop="classify" label="笔记内容">
                <el-radio-group
                  text-color="#ffffff"
                  fill="#3b44db"
                  v-model="editForm.classify"
                >
                  <el-radio-button :label="1">MARKDOWN</el-radio-button>
                  <el-radio-button :label="2"
                    >&nbsp;&nbsp;&nbsp;富&nbsp;&nbsp;&nbsp;&nbsp;文&nbsp;&nbsp;&nbsp;&nbsp;本&nbsp;&nbsp;&nbsp;</el-radio-button
                  >
                </el-radio-group>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item prop="note_premission" label="可见权限">
                <el-select
                  v-model="editForm.note_premission"
                  placeholder="请选择可见权限"
                  style="width:70%"
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
          <el-form-item prop="content" style="height:500px">
            <tinymce
              v-show="editForm.classify == 2"
              ref="bzlc"
              :height="500"
              :id="'noteCreate'"
              :tinyVal="editForm.content"
            ></tinymce>
            <mavon-editor
              v-show="editForm.classify == 1"
              :class="navigation ? 'mavon_normal' : 'mavon'"
              style="min-height:500px"
              @imgAdd="imgAdd"
              @imgDel="imgDel"
              @navigationToggle="navigationChange"
              :boxShadow="true"
              previewBackground="#f0f2f5"
              :editable="true"
              :subfield="true"
              :autofocus="true"
              defaultOpen="preview"
              v-model="editForm.content"
              ref="md"
            >
            </mavon-editor>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer" class="addFooter">
        <el-button
          @click="addSubmit"
          type="primary"
          class="sureBtn"
          :loading="loadNoteSureAdd"
          >新增笔记</el-button
        >
      </div>
    </el-dialog>
    <!-- 笔记操作日志 -->
    <el-dialog
      :visible.sync="noteLogVisible"
      class="addDialog flieLog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      width="50%"
      top="3%"
    >
      <div class="addMain">
        <div class="addTopbar">
          <span class="englishView">操作日志</span>
          <img src="@/assets/img/operation_log.png" alt="" />
        </div>
        <el-row
          :gutter="50"
          class="scrollStyle"
          style="margin:0;height:calc(100% - 78px);padding-top:50px;"
        >
          <el-col
            :span="16"
            style="height:100%;"
            v-if="noteLogDetail.length !== 0"
          >
            <div class="rmMiddle" style="padding-left:0;">
              <el-steps
                direction="vertical"
                :space="70"
                :active="noteLogDetail.length"
              >
                <el-step v-for="(sLine, index) in noteLogDetail" :key="index">
                  <template slot="title">
                    <div class="step_box">
                      <p class="cont">
                        <span class="setpSty"></span>
                        【{{ sLine.user_name }}】{{
                          sLine.action === 1
                            ? "新增了"
                            : sLine.action === 2
                            ? "修改了"
                            : "删除了"
                        }}“{{ sLine.note_name }}”
                      </p>
                      <p class="time">{{ sLine.action_time }}</p>
                    </div>
                  </template>
                </el-step>
              </el-steps>
            </div>
          </el-col>
        </el-row>
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
      :append-to-body="true"
    >
      <span class="spans">{{
        dialogType === 0
          ? "删除笔记"
          : dialogType === 1
          ? "版本回退"
          : "删除目录"
      }}</span>
      <p class="contentPsty">
        {{
          dialogType === 0
            ? "删除后可在任务快照恢复任务，确认删除笔记?"
            : dialogType === 1
            ? "回退操作不可恢复，确认回退版本?"
            : "目录及目录下的笔记都将被删除，确认删除?"
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
    <!--笔记模态框-->
    <el-dialog
      :visible.sync="noteOutsideVisible"
      width="30%"
      top="15%"
      class="delDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
    >
      <span class="spans">请选择导出笔记格式</span>
      <p class="contentPsty">
        <el-col :span="12" class="pdf_note">
          <img
            src="@/assets/img/img_notePDF.png"
            @click="noteDownload('pdf')"
          />
          <!-- @click="
              curRowData.classify === 2
                ? noteDownload('pdf')
                : $message.warning(
                    'markdown格式笔记不支持pdf导出，请用md格式导出！'
                  )
            " -->
        </el-col>
        <el-col :span="12" class="md_note">
          <img src="@/assets/img/img_noteMD.png" @click="noteDownload('md')" />
        </el-col>
      </p>
      <div slot="footer">
        <el-button
          type="info"
          class="btnCancle"
          @click="noteOutsideVisible = false"
          >取 消</el-button
        >
      </div>
    </el-dialog>
    <!-- 编辑笔记 -->
    <el-drawer
      :visible.sync="editNote"
      size="80%"
      class="addTaskModal"
      :withHeader="false"
      :append-to-body="true"
    >
      <div
        style="height:100%;"
        v-loading="detailGetLoading"
        element-loading-text="数据加载中"
        element-loading-background="rgba(0, 0, 0, 0.6)"
      >
        <div class="addTaskBox">
          <div class="addModalTop" style="padding: 40px 70px 20px;">
            <div class="one_level">
              <span class="noteTitle"
                >{{ currentName + "  /  " + curRowData.note_name + "  /  "
                }}<a style="font-size:30px;color:#000">编辑笔记</a></span
              >
              <div class="pull_right">
                <el-button
                  size="small"
                  class="editBtn"
                  :loading="saveeditLoading"
                  @click="saveEdit"
                  round
                  >保存编辑 <i class="el-icon-edit"></i>
                </el-button>
                <el-button
                  size="small"
                  class="delBtn"
                  @click="noteEdit(0)"
                  round
                  >取消编辑 <i class="el-icon-delete"></i>
                </el-button>
              </div>
            </div>
          </div>
          <div class="mainBox">
            <el-row :gutter="40" style="height: 100%;margin:0;padding:0 30px">
              <el-form
                :model="editForm"
                style="height:100%"
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
                        v-model="editForm.label"
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
                      <el-tooltip
                        class="item"
                        effect="dark"
                        content="管理标签"
                        placement="top"
                      >
                        <el-button
                          style="background:#434be0;border-color: #434be0;color:#fff;padding: 10px 12px;margin-left:10px;"
                          icon="el-icon-s-tools"
                          @click="manageTags"
                        ></el-button>
                      </el-tooltip>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item prop="classify" label="笔记内容">
                      <el-radio-group
                        text-color="#ffffff"
                        fill="#3b44db"
                        v-model="editForm.classify"
                      >
                        <el-radio-button :label="1">MARKDOWN</el-radio-button>
                        <el-radio-button :label="2"
                          >&nbsp;&nbsp;&nbsp;富&nbsp;&nbsp;&nbsp;&nbsp;文&nbsp;&nbsp;&nbsp;&nbsp;本&nbsp;&nbsp;&nbsp;</el-radio-button
                        >
                      </el-radio-group>
                    </el-form-item>
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
                <el-form-item prop="content" style="height:calc(100% - 165px)">
                  <tinymce
                    v-if="editNote"
                    v-show="editForm.classify == 2"
                    ref="bzlcc"
                    :height="620"
                    :id="'noteEdit'"
                    :tinyVal="editForm.content"
                  ></tinymce>
                  <mavon-editor
                    v-show="editForm.classify == 1"
                    :class="navEdit ? 'mavon_normal' : 'mavon'"
                    style="min-height:620px"
                    @imgAdd="imgAdd"
                    @imgDel="imgDel"
                    @navigationToggle="navEditChange"
                    :boxShadow="true"
                    previewBackground="#f0f2f5"
                    :editable="true"
                    :subfield="true"
                    :autofocus="true"
                    defaultOpen="preview"
                    v-model="editForm.content"
                    ref="md_e"
                  >
                  </mavon-editor>
                </el-form-item>
              </el-form>
            </el-row>
          </div>
        </div>
        <div @click="editNote = false" class="closeBtn">
          <i class="el-icon-arrow-right"></i>
        </div>
      </div>
    </el-drawer>
    <!-- 回退预览 -->
    <el-dialog
      :visible.sync="versionBackVisible"
      class="addDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      width="50%"
      top="3%"
    >
      <div class="addMain">
        <div class="addTopbar">
          <span class="englishView">回退预览</span>
          <img src="@/assets/img/img_VersionPreview.png" alt="" />
        </div>
        <div v-if="versionCont" class="content scrollStyle">
          <mavon-editor
            class="mavon detailEditor"
            style="max-height: 560px;"
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
      <div slot="footer" class="addFooter">
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
    <!-- 笔记批量上传 -->
    <el-dialog
      :visible.sync="noteUploadVisible"
      class="addDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      width="30%"
      top="6%"
    >
      <div class="addMain">
        <div class="addTopbar">
          <span class="englishView">笔记上传</span>
          <img src="@/assets/img/img_noteupload.png" alt="" />
        </div>
        <div class="content" style="padding:0">
          <el-form label-width="100px">
            <el-form-item label="可见权限">
              <el-select
                v-model="note_pro"
                placeholder="请选择可见权限"
                style="width:100%"
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
            <el-form-item label="笔记上传">
              <el-upload
                class="upload-demo"
                accept=".txt,.md"
                drag
                ref="noteUpload"
                :auto-upload="false"
                :on-change="changeNote"
                :on-remove="handleRemove"
                :on-exceed="handleExceed"
                :file-list="uploadList"
                :http-request="uploadFile"
                :limit="10"
                action="#"
                multiple
              >
                <i class="el-icon-upload"></i>
                <div class="el-upload__text">
                  将文件拖到此处，或<em>点击上传</em>
                </div>
                <div class="el-upload__tip" slot="tip">
                  只能上传.txt/.md文件，且不超过500kb
                </div>
              </el-upload>
            </el-form-item>
          </el-form>
        </div>
      </div>
      <div slot="footer" class="addFooter">
        <el-button
          @click="uploadNote(versionRow)"
          class="btnSure"
          :loading="sureUpload"
          type="warning"
          >导 入</el-button
        >
        <el-button
          type="info"
          class="btnCancle"
          @click="noteUploadVisible = false"
          >放 弃</el-button
        >
      </div>
    </el-dialog>
  </el-row>
</template>
<script>
/* eslint-disable */
import {
  taskNoteTree,
  taskNotesAdd,
  taskNotesEdit,
  getTaskDetail,
  logDetails,
  noteBack,
  delNote,
  editState,
  noteedit,
  dirAdd,
  dirEdit,
  dirDelete,
  noteLabel,
  tagAdd,
  tagDel,
  taskNoteSearch,
  noteUpload,
  uploadImg,
  delImg,
  noteExport
} from "@/api/task";
import tinymce from "./tinymce-editor";
export default {
  name: "taskNote",
  components: {
    tinymce
  },
  data() {
    return {
      notePageState: false, // 管理分页功能状态
      detailNoData: true,
      detailSearch: "",
      detailPage: 1,
      detailSize: 10,
      detailTotalSize: -1,
      taskNotesArr: [],
      node_name: "根目录",
      node: null,
      resolve: null,
      noteTreeProps: {
        children: "sub_dir",
        label: "dir_name"
        // isLeaf: 'leaf'
      },
      // 标签操作
      tagsListVisible: false,
      addTagsVisible: false,
      tag_name: "",
      loadtagSure: false,
      // 目录操作
      addDirectoryVisible: false,
      directory_type: "add",
      directory_name: "",
      loadDirSure: false,
      // 笔记操作
      addNoteVisible: false,
      loadNoteSureAdd: false,
      noteLogVisible: false,
      noteLogDetail: [],
      detailGetLoading: false,
      // 笔记详情
      is_load: false,
      notesListShow: true,
      curRowData: {},
      currentName: "",
      editNote: false,
      editForm: {
        note_name: "",
        note_premission: 0,
        label: "",
        classify: 1,
        content: ""
      },
      editRules: {
        note_name: [
          { required: true, message: "请输入笔记名称", trigger: "blur" },
          { min: 1, max: 16, message: '名称长度在 1 到 16 个字符', trigger: 'blur' },
        ],
        label: [
          { required: true, message: "选择用户类型", trigger: "blur change" }
        ],
        classify: [
          { required: true, message: "请选择笔记内容", trigger: "blur change" }
        ],
        belong_to_dir: [
          { required: true, message: "请选择笔记归属", trigger: "blur change" }
        ],
        note_premission: [
          { required: true, message: "请选择可见权限", trigger: "blur change" }
        ]
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
      noteBelongList: [
        {
          id: 0,
          name: "等后台接口"
        }
      ],
      editLoading: false,
      delVisible: false,
      dialogType: 0,
      loadSureDel: false,
      userTypeList: [],
      saveeditLoading: false,
      noteSearchList: [],
      noteSearchState: false,
      noteStr: '',
      noteFlag: '',
      search_page: 1,
      search_page_size: 10,
      searchTotalSize: 0,
      noteOutsideVisible: false,
      // 回退预览
      versionBackVisible: false,
      versionCont: null,
      versionRow: null,
      // 笔记批量上传
      noteUploadVisible: false,
      uploadList: [],
      noteData: [],   
      sureUpload: false,
      note_pro: 0,
      navigation: false,
      navEdit: false
    };
  },
  mounted() {
    //this.noteTreeLoadNode(this.node_save, this.resolve)
    this.getAllLabel()
  },
  watch:{
    editNote(a){
      if(!a){
        this.noteEdit(3)
      }
    }
  },
  created() {
  },
  created() {},
  created() {},
  computed: {
    taskId() {
      return this.$store.state.user.task_id;
    }
  },
  methods: {
    // 获取所有笔记标签
    getAllLabel() {
      noteLabel()
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
    // 管理标签
    manageTags() {
      this.tagsListVisible = true;
    },
    addTagLabel() {
      this.tag_name = "";
      this.addTagsVisible = true;
    },
    addTagSubmit() {
      if (this.tag_name === "") {
        this.$message.warning("标签名称不能为空");
        return false;
      } else if (this.tag_name.length >= 20) {
        this.$message.warning("标签名称请小于20字符");
        return false;
      }
      this.loadtagSure = true;
      tagAdd({ label_name: this.tag_name })
        .then(response => {
          this.loadtagSure = false;
          if (response.data.success) {
            // this.tagsListVisible = false;
            this.addTagsVisible = false;
            this.$message.success(response.data.info);
            this.getAllLabel();
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.loadtagSure = false;
          this.$message.error(error.message);
        });
    },
    delTags(row) {
      this.$confirm("确认删除该标签？")
        .then(() => {
          tagDel({ label_id: row.id })
            .then(response => {
              if (response.data.success) {
                this.getAllLabel();
              } else {
                this.$message.warning(response.data.info);
              }
            })
            .catch(error => {
              this.$message.error(error.message);
            });
        })
        .catch(() => {});
    },
    // 笔记搜索
    noteSearch(search, flag){
      this.editNote = false
      let send = {
        task_id: this.taskId,
        search: search,
        page: this.search_page,
        max_count: this.search_page_size,
        keyword: 'note',
        flag: flag
      }
      this.noteStr = search
      this.noteFiag = flag
      taskNoteSearch(send)
        .then(response => {
          if (response.data.success) {
            let d = response.data.data
            for(let i=0;i<d.length;i++){
              d[i].note_name = this.brightenKeyword(d[i].note_name, search)
              d[i].content = this.brightenKeyword(d[i].content, search)
            }
            this.noteSearchList = d
            this.noteSearchState = true;
            this.searchTotalSize = response.data.total
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    // 搜索高亮
    brightenKeyword(val, keyword) {
      // 方法1：筛选变色
      // val = val + '';
      // if (val.indexOf(keyword) !== -1 && keyword !== '') {
      //     return val.replace(keyword, '<font color="#409EFF">' + keyword + '</font>')
      // } else {
      //     return val
      // }
      // 方法2：用正则表达式
      const Reg = new RegExp(keyword, "i");
      if (val) {
        const res = val.replace(
          Reg,
          `<span style="color: #FF7800;">${keyword}</span>`
        );
        return res;
      }
    },
    // 树节点
    // 懒加载
    noteTreeLoadNode(node, resolve) {
      if(!this.notePageState){
        this.detailPage = 1
      }
      this.editNote = false
      this.is_load = false
      this.detailNoData = true
      this.notesListShow = true
      this.noteSearchState = false
      this.node = node
      this.resolve = resolve
      this.node.childNodes = [];
      let sendD = null;
      if (node.level === 0 || node.data.id === 0) {
        sendD = {
          task_id: this.taskId,
          is_primary: 1,
          page: this.detailPage,
          max_count: this.detailSize
        };
      } else {
        sendD = {
          task_id: this.taskId,
          page: this.detailPage,
          max_count: this.detailSize,
          dir_id: node.data.id,
          is_primary: 0
        };
      }
      this.detailGetLoading = true;
      taskNoteTree(sendD)
        .then(response => {
          this.detailGetLoading = false;
          this.is_load = true;
          if (response.data.success) {
            this.notePageState = false;
            if(node.level !== undefined && node.level === 0){
              resolve([{ dir_name: '根目录',id: 0,sub_dir: response.data.data.sub_dir}])
            }else{
              resolve(response.data.data.sub_dir)
            }
            if (
              (node.level !== undefined && node.level === 0) ||
              node.data.id === 0
            ) {
              this.node_name = "根目录";
            } else {
              this.node_name = response.data.data.dir_name;
            }
            let d = response.data.data.note_info;
            if (d.length === 0) {
              this.detailNoData = false;
              return false;
            }
            if (node.parent != undefined) {
              for (let i = 0; i < d.length; i++) {
                d[i].parentLabel = node.parent.label;
              }
            }
            this.taskNotesArr = d;
            this.detailTotalSize = response.data.data.total;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.detailGetLoading = false;
          this.$message.error(error.message);
        });
    },
    handleNodeClick(data){
      this.noteSearchState = false;
      if(this.is_load){
        if(data.dir_name !== "根目录"){
          let node = this.$refs.structure.getNode(data.id); // 通过节点id找到对应树节点对象
          node.loaded = false;
          node.expand(); 
        }else{
          let node = this.$refs.structure.getNode(0); // 通过节点id找到对应树节点对象
          node.loaded = false;
          node.expand(); 
        }
      }
    },
    // 分页
    detailSizeChange(val) {
      this.detailSize = val;
      this.notePageState = true;
      this.noteTreeLoadNode(this.node, this.resolve);
    },
    detailCurrentChange(val) {
      this.detailPage = val;
      this.notePageState = true;
      this.noteTreeLoadNode(this.node, this.resolve);
    },
    navigationChange(state){
      this.navigation = state
    },
    navEditChange(state){
      this.navEdit = state
    },
    // 新增&编辑目录
    addDirectory(type) {
      this.directory_type = type;
      this.addDirectoryVisible = true;
      if (type === "edit") {
        this.directory_name = this.node.data.dir_name;
      } else {
        this.directory_name = "";
      }
    },
    addDirSubmit() {
      if (this.directory_name === "") {
        this.$message.warning("请输入目录名称");
        return false;
      } else if (this.directory_name.length > 16) {
        this.$message.warning("目录名称小于16字符");
        return false;
      }
      let sendD = null;
      if (this.directory_type === "add") {
        console.log(this.node)
        if (this.node.data !== undefined && this.node.data.dir_name !== "根目录"){
          sendD = {
            task_id: this.taskId,
            primary: 0,
            pid: this.node.data.id,
            filename: this.directory_name
          };
        } else {
          sendD = {
            task_id: this.taskId,
            primary: 1,
            filename: this.directory_name
          };
        }
        dirAdd(sendD)
          .then(response => {
            this.loadDirSure = false;
            this.addDirectoryVisible = false;
            if (response.data.success) {
              if(this.node.data !== undefined && this.node.data.dir_name !== "根目录"){
                let node = this.$refs.structure.getNode(this.node.parent.data.id); // 通过节点id找到对应树节点对象
                node.loaded = false;
                node.expand(); 
              }else{
                let node = this.$refs.structure.getNode(0); // 通过节点id找到对应树节点对象
                node.loaded = false;
                node.expand(); 
              }
            } else {
              this.$message.warning(response.data.info);
            }
          })
          .catch(error => {
            this.loadDirSure = false;
            this.addDirectoryVisible = false;
            this.$message.error(error.message);
          });
      } else {
        sendD = {
          dir_id: this.node.data.id,
          dir_name: this.directory_name
        };
        dirEdit(sendD)
          .then(response => {
            this.loadDirSure = false;
            this.addDirectoryVisible = false;
            if (response.data.success) {
              if(this.node.data !== undefined && this.node.data.dir_name !== "根目录"){
                let node = this.$refs.structure.getNode(this.node.parent.data.id); // 通过节点id找到对应树节点对象
                node.loaded = false;
                node.expand(); 
              }else{
                let node = this.$refs.structure.getNode(0); // 通过节点id找到对应树节点对象
                node.loaded = false;
                node.expand(); 
              }
            } else {
              this.$message.warning(response.data.info);
            }
          })
          .catch(error => {
            this.loadDirSure = false;
            this.addDirectoryVisible = false;
            this.$message.error(error.message);
          });
      }
    },
    // 删除目录
    delDirectory() {
      this.dialogType = 2;
      this.dialogData = this.node;
      this.delVisible = true;
    },
    // 导入笔记&监控上传笔记列表
    changeNote(file, fileList){
      console.log(file)
      let isJPGCon = file.name.split(".");
      isJPGCon = isJPGCon[isJPGCon.length - 1];
      const isLt2M = file.size / 1024 / 1024 < 2.5;
      let st = ['txt','md']
      if (st.indexOf(isJPGCon) < 0) {
        this.$message.error("上传笔记文件只能是 txt 或 md 格式!");
        return false
      }
      if (!isLt2M) {
        this.$message.error("上传笔记文件大小不能超过 2.5MB!");
        return false
      }
      let existFile = fileList.slice(0, fileList.length - 1).find(f => f.name === file.name);
      if (existFile) {
        this.$message.error('当前笔记已经存在!');
        fileList.pop();
      }
      this.uploadList = fileList;
    },
    // 上传笔记
		uploadFile(file) {
      this.noteData.append('myfiles', file.file);  // append增加数据
    },
    //移除
    handleRemove(file, fileList) {
      this.uploadList = fileList;
      // return this.$confirm(`确定移除 ${ file.name }？`);
    },
    // 选取笔记超过数量提示
    handleExceed(files, fileList) {
      this.$message.warning(`当前限制选择 10 个笔记，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
    },
    uploadNote(){
      if (this.uploadList.length === 0) {
        this.$message({ message: '请至少选择一个需上传的笔记文件', type: 'warning'  })
        return false
      }
      this.sureUpload = true
      this.noteData = new FormData();  // new formData对象
      this.$refs.noteUpload.submit();  // 提交调用uploadFile函数
      this.noteData.append('p_dir_id', this.node.data.id);  // 添加目录构id
      this.noteData.append('label', this.userTypeList.length !== 0?this.userTypeList[0].id:''); // 添加默认标签
      this.noteData.append('classify', 1);  // 添加文本属性
      this.noteData.append('note_premission', this.note_pro);  // 添加token
      noteUpload(this.noteData)
        .then(response => {
          this.sureUpload = false;
          this.noteUploadVisible = false;
          if (response.data.success) {
            this.detailPage = 1;
            this.noteTreeLoadNode(this.node, this.resolve);
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.sureUpload = false;
          this.noteUploadVisible = false;
          this.$message.error(error.message);
        });
    },
    // 新增笔记
    addNote() {
      var f = this.$refs["forms"];
      if (f != undefined && f != null) {
        this.$refs["forms"].resetFields();
      }
      this.editForm = {
        note_name: "",
        note_premission: 0,
        label: "",
        classify: 1,
        content: ""
      };
      this.addNoteVisible = true;
    },
    // 确认新增笔记
    addSubmit() {
      this.$refs["forms"].validate(valid => {
        if (valid) {
          this.loadNoteSureAdd = true;
          const sendD = {
            p_dir_id: this.node.data.id,
            content: this.editForm.classify === 1? this.editForm.content:this.$refs.bzlc.release(),
            note_name: this.editForm.note_name,
            label: this.editForm.label,
            classify: this.editForm.classify,
            note_premission: this.editForm.note_premission
          };
          taskNotesAdd(sendD)
            .then(response => {
              this.loadNoteSureAdd = false;
              this.addNoteVisible = false;
              if (response.data.success) {
                this.detailPage = 1;
                this.noteTreeLoadNode(this.node, this.resolve);
              } else {
                this.$message.warning(response.data.info);
              }
            })
            .catch(error => {
              this.loadNoteSureAdd = false;
              this.addNoteVisible = false;
              this.$message.error(error.message);
            });
        } else {
          this.$message.error("请完善各项内容");
          return false;
        }
      });
    },
    // 查看笔记详情及相关操作
    checkSinNote(item) {
      this.noteSearchState = false;
      this.notesListShow = false;
      this.detailGetLoading = true;
      this.editNote = false;
      let send = {
        note_id: item.note_id
      };
      getTaskDetail(send)
        .then(res => {
          this.detailGetLoading = false;
          if (res.data.success) {
            this.curRowData = res.data.data;
            this.$set(this.curRowData, "content", res.data.data.content);
            this.$set(this.curRowData, "details", res.data.data.back_info);
            this.editForm = res.data.data;
          } else {
            this.$message.warning(res.data.info);
          }
        })
        .catch(error => {
          this.detailGetLoading = false;
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
            for(let i=0;i<this.userTypeList.length;i++){
              if(this.userTypeList[i].name === this.editForm.label){
                this.editForm.label = this.userTypeList[i].id 
              }
            }
          } else {
            this.$message.warning(res.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    imgAdd(pos, $file){
      // 第一步.将图片上传到服务器.
      let formdata = new FormData();
      formdata.append('images', $file);
      uploadImg(formdata).then(res => {
        if (res.data.success) {
          let json =  "http://192.168.8.243:8080" + res.data.img_addr; //取出上传成功后的url
          if(this.addNoteVisible){
            this.$refs.md.$imglst2Url([[pos, json]])
          }else{
            this.$refs.md_e.$imglst2Url([[pos, json]])
          }
        } else {
          this.$message({type: json.status, message: json});
        }
      });
    },
    imgDel(pos){
      let arr = pos[0].split('/images/')
      delImg({img: arr[1]})
        .then(() => {
          this.$message.success('删除成功')
        })
        .catch(res => {
          console.log(res)
        })
    },
    // 编辑笔记
    noteEdit(flag) {
      let f = flag
      var data = {
        task_id: this.taskId,
        note_id: this.curRowData.id,
        flag: f === 3?0:f
      };
      this.editLoading = true;
      this.$set(this.editForm, "content", "");
      editState(data)
        .then(res => {
          this.editLoading = false;
          if (res.data.code === 200) {
            this.editNote = true;
            this.getEditForm()
            clearInterval(this.interVal);
            this.interVal = setInterval(() => {
              // 编辑5分钟后自动保存
              if (this.editNote) {
                this.saveEdit();
              }
            }, 300000);
          } else {
            if(f !== 3){
              this.editNote = false;
              this.$message.warning(res.data.info);
            }
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
            content: this.editForm.classify === 1? this.editForm.content:this.$refs.bzlcc.release(),
            note_name: this.editForm.note_name,
            label: this.editForm.label,
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
                this.noteTreeLoadNode(this.node, this.resolve);
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
    versionView(val){
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
              this.versionCont = res.data.data
            } else {
              this.$message.warning(res.data.info);
            }
          })
          .catch(error => {
            this.$message.error(error.message);
          });
    },
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
              this.detailPage = 1;
              this.noteTreeLoadNode(this.node, this.resolve)
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
      } else if (this.dialogType === 1) {
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
              this.noteTreeLoadNode(this.node, this.resolve)
            } else {
              this.$message.warning(res.data.info);
            }
            this.taskDeteilDrawer = false;
            this.delVisible = false;
          })
          .catch(error => {
            this.loadSureDel = false;
            this.delVisible = false;
            this.versionBackVisible = false;
            this.$message.error(error.message);
          });
      } else if (this.dialogType === 2) {
        var data = {
          dir_id: this.dialogData.data.id
        };
        dirDelete(data)
          .then(res => {
            this.loadSureDel = false;
            if (res.data.success) {
              this.$message.success("删除成功");
              let node = this.$refs.structure.getNode(this.node.parent.data.id); // 通过节点id找到对应树节点对象
              node.loaded = false;
              node.expand();
              // let that = this
              // const parent = this.dialogData.parent;
              // const children = parent.data.sub_dir || parent.data;
              // const index = children.findIndex(d => d.id === that.dialogData.id);
              // children.splice(index, 1);
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
      }
    },
    // 笔记查看日志
    noteLogLook() {
      var sendD = {
        task_id: this.taskId,
        key_word: "note"
      };
      logDetails(sendD)
        .then(response => {
          if (response.data.success) {
            this.noteLogVisible = true;
            this.noteLogDetail = response.data.data;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    searchSizeChange(val){
      this.search_page_size = val;
      this.search_page = 1;
      this.noteSearch(this.noteStr, this.noteFlag)
    },
    searchCurrentChange(val) {
      this.search_page = val;
      this.noteSearch(this.noteStr, this.noteFlag)
    },
    // 笔记导出
    noteDownload(type) {
      let send = {
        note_id: this.curRowData.id,
        type: type,
        token: this.$store.getters.token
      }
      noteExport(send)
        .then(response => {
          if (response.data.code !== undefined) {
            this.$message.warning(response.data.info);
            return false
          }
          const a = document.createElement("a");
          a.href =
            "http://192.168.8.243:10000/api/task/v1/download_note?note_id=" +
            this.curRowData.id
          + "&type=" + type
          + "&token=" + this.$store.getters.token;
          a.download = this.curRowData.note_name;
          document.querySelector("body").appendChild(a);
          a.click();
          document.querySelector("body").removeChild(a);
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
  },
  filters: {
    beautySub(str, len) {
      let reg = /[\u4e00-\u9fa5]/g, //专业匹配中文
        slice = str.substring(0, len),
        chineseCharNum = ~~(slice.match(reg) && slice.match(reg).length),
        realen = slice.length * 2 - chineseCharNum;
      return str.substr(0, realen) + (realen < str.length ? "..." : "");
    }
  }
};
</script>
<style lang="scss" scoped>
.delDialog {
  .spans {
    font-size: 25px;
    text-align: center;
    display: block;
  }
  .contentPsty {
    font-size: 16px;
    margin: 26px;
    font-weight: bold;
    text-align: center;
  }
}
</style>
