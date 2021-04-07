<template>
  <div
    class="taskView"
    v-loading="listLoading"
    element-loading-text="数据加载中"
    element-loading-background="rgba(0, 0, 0, 0.6)"
  >
    <div class="mainTop">
      <el-row style="margin-bottom: 8px;" :gutter="20">
        <el-col :span="15">
          <span class="englishView">任务列表</span>
          <img src="@/assets/img/tasklist.png" alt="" />
        </el-col>
        <el-col :span="4">
          <el-button
            title="新增"
            type="primary"
            size="medium"
            style="height:42px;padding:8px 20px;background-image: linear-gradient(to right, #5861f0, #3b44db);border-color:#5861f0;"
            @click="addEditSinTask('', 'add')"
            round
          >
            新增任务
            <i class="el-icon-circle-plus-outline"></i>
          </el-button>
          <el-button
            title="检索"
            type="primary"
            size="medium"
            style="height:42px;padding:8px 20px;margin-left:20px;background-image: linear-gradient(to right, #64db7d, #3fbf59);border-color:#64db7d;"
            @click="allSearchVisible = true"
            round
          >
            全局检索
            <i class="iconfont icon-jiansuo"></i>
          </el-button>
        </el-col>
        <el-col :span="5">
          <el-input
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
      <el-table
        :data="proListData"
        v-if="noDataIs"
        class="proTable scrollStyle"
        style="width: 100%;"
      >
        <el-table-column type="index" label="序号" width="50">
        </el-table-column>
        <el-table-column prop="title" label="任务名称" show-overflow-tooltip>
        </el-table-column>
        <el-table-column prop="user" label="创建人"> </el-table-column>
        <el-table-column label="任务进度" width="200">
          <template slot-scope="scope">
            <el-progress
              :stroke-width="10"
              :percentage="Number(scope.row.task_process)"
              :class="[Number(scope.row.task_process) === 100 ? 'hundred' : '']"
            ></el-progress>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="任务时长" width="300">
          <template slot-scope="scope">
            <div class="taskTime">
              <span class="time">{{ scope.row.start_time }}</span>
              <span class="divider"> — </span>
              <span class="time">{{ scope.row.end_time }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="260" fixed="right">
          <template slot-scope="scope">
            <el-button
              title="详情"
              class="sinProBtn detailBtn"
              @click="checkDetail(scope.row)"
            >
              详情
            </el-button>
            <el-button
              title="编辑"
              v-if="task_permission === 0 ? scope.row.user === base_info : true"
              class="sinProBtn editBtn"
              @click="addEditSinTask(scope.row, 'edit')"
            >
              编辑
            </el-button>
            <el-button
              title="删除"
              v-if="task_permission === 0 ? scope.row.user === base_info : true"
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
    <!--新增确认抽屉-->
    <el-drawer
      :visible.sync="addVisible"
      class="addTaskModal"
      size="80%"
      :withHeader="false"
      :close-on-press-escape="false"
    >
      <div class="addTaskBox">
        <div class="addModalTop" style="padding: 50px 70px;">
          <span class="englishView">{{
            taskType === "add" ? "新增任务" : "编辑任务"
          }}</span>
          <img
            :src="
              taskType === 'add'
                ? require('@/assets/img/newTask.png')
                : require('@/assets/img/img_edittask.png')
            "
            alt=""
          />
        </div>
        <el-form
          ref="form"
          :model="form"
          :rules="rules"
          style="padding: 30px 70px;"
          label-position="left"
          label-width="80px"
        >
          <el-row style="height:100%;">
            <el-col :span="12" style="height:100%;">
              <div class="leftModal scrollStyle">
                <el-form-item label="任务名称" prop="name">
                  <el-input
                    style="width: 70%;"
                    v-model.trim="form.name"
                    placeholder="请输入任务名称"
                  >
                  </el-input>
                </el-form-item>
                <el-form-item label="任务描述" prop="describe">
                  <el-input
                    style="width: 70%;"
                    type="textarea"
                    v-model="form.describe"
                    :rows="4"
                  ></el-input>
                </el-form-item>
                <el-form-item label="任务时长" prop="time">
                  <el-date-picker
                    style="width:70%;"
                    v-model="form.time"
                    type="datetimerange"
                    :editable="false"
                    range-separator="至"
                    start-placeholder="开始日期"
                    end-placeholder="结束日期"
                    value-format="yyyy-MM-dd HH:mm:ss"
                  >
                  </el-date-picker>
                </el-form-item>
                <el-form-item label="任务指派" prop="participant">
                  <el-checkbox-group v-model="form.participant">
                    <el-checkbox
                      v-for="item in userList"
                      :key="item.id"
                      :label="item.id"
                      border
                      >{{ item.name }}</el-checkbox
                    >
                  </el-checkbox-group>
                </el-form-item>
              </div>
            </el-col>
          </el-row>
        </el-form>
        <el-button
          @click="sureAddTask"
          type="primary"
          class="sureBtn"
          :loading="loadSureAdd"
          >{{ taskType === "add" ? "新增任务" : "保存任务" }}</el-button
        >
        <div @click="addVisible = false" class="closeBtn">
          <i class="el-icon-arrow-right"></i>
        </div>
      </div>
    </el-drawer>
    <!--任务详情模抽屉-->
    <el-drawer
      :visible.sync="taskDetailDrawer"
      class="addTaskModal"
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
        <div class="addTaskBox">
          <div class="addModalTop">
            <span class="englishView">任务详情</span>
            <img src="@/assets/img/taskDetails.png" alt="" />
          </div>
          <el-input
            class="searchBoxPos"
            v-if="
              activeName != 'first' &&
                activeName != 'second' &&
                notesListShow &&
                portInfoIs
            "
            placeholder="请输入搜索内容"
            @input="enterDetailCheck"
            @keypress.enter.native="checkDetailResult"
            v-model="detailSearch"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="checkDetailResult"
            ></el-button>
          </el-input>
          <el-select
            @change="checkSixth"
            v-model="hostChoose"
            v-if="activeName === 'sixth'"
            class="hostPos"
            placeholder="请选择"
          >
            <el-option label="筛选主机" value=""> </el-option>
            <el-option
              v-for="item in hostEnum"
              :key="item.id"
              :label="item.name + '(' + item.ip + ')'"
              :value="item.id"
            >
            </el-option>
          </el-select>
          <el-select
            v-model="noteChoose"
            v-if="activeName === 'third'"
            class="hostPos"
            placeholder="请选择"
          >
            <el-option label="搜索（名称）" value="name"> </el-option>
            <el-option label="搜索（内容）" value="content"> </el-option>
          </el-select>
          <div
            class="pageShowStyle"
            :class="activeName == 'fourth' ? 'pageDirectory' : ''"
            v-if="
              activeName != 'first' &&
                activeName != 'second' &&
                activeName != 'third' &&
                activeName != 'eighth' &&
                notesListShow &&
                portInfoIs &&
                detailNoData &&
                !fileSearchState
            "
          >
            <el-pagination
              @size-change="detailSizeChange"
              @current-change="detailCurrentChange"
              :current-page="detailPage"
              :page-sizes="pageSizeArr"
              :page-size="detailSize"
              layout="total, sizes, prev, pager, next, jumper"
              :total="detailTotalSize"
            >
            </el-pagination>
          </div>
          <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="数据概览" name="first" class="firstPane">
              <el-form
                :model="taskDetail"
                label-position="left"
                label-width="80px"
              >
                <el-row :gutter="20" style="height:100%;">
                  <el-col :span="24" style="height:32%;">
                    <div class="rightModal">
                      <el-col :span="18" style="height:100%;">
                        <div class="rmTop">
                          <ul>
                            <li>
                              <div>
                                {{ taskDetail.masterAmount }}
                              </div>
                              <span>主机数量</span>
                            </li>
                            <li>
                              <div>
                                {{ taskDetail.leakAmount }}
                              </div>
                              <span>漏洞数量</span>
                            </li>
                            <li>
                              <div>
                                {{ taskDetail.portAmount }}
                              </div>
                              <span>端口数量</span>
                            </li>
                            <li>
                              <div>
                                {{ taskDetail.voucherAmount }}
                              </div>
                              <span>凭证数量</span>
                            </li>
                            <li>
                              <div>
                                {{ taskDetail.fileAmount }}
                              </div>
                              <span>文件数量</span>
                            </li>
                            <li>
                              <div>
                                {{ taskDetail.noteAmount }}
                              </div>
                              <span>笔记数量</span>
                            </li>
                          </ul>
                        </div>
                      </el-col>
                      <el-col :span="6" style="height:100%;">
                        <div class="rmMiddle">
                          <div id="progressTask"></div>
                        </div>
                      </el-col>
                    </div>
                  </el-col>
                  <el-col :span="8" class="logTable">
                    <el-table
                      v-if="taskDetail.mindLog != undefined"
                      :data="taskDetail.mindLog.slice(0, 10)"
                      :header-cell-style="{ background: '#fff', color: '#222' }"
                      height="100%"
                      style="width: 100%"
                    >
                      <el-table-column
                        label="思维导图日志"
                        :show-overflow-tooltip="true"
                      >
                        <template slot-scope="scope">
                          <span
                            :style="
                              scope.row.type === 1
                                ? 'color:#3fbf59'
                                : scope.row.type === 2
                                ? 'color:#3b44db'
                                : 'color:#ed5642'
                            "
                            >【{{ scope.row.user }}】
                            {{
                              scope.row.type === 1
                                ? "新增了"
                                : scope.row.type === 2
                                ? "修改了"
                                : "删除了"
                            }}
                            {{ scope.row.name }}</span
                          >
                        </template>
                      </el-table-column>
                      <el-table-column
                        prop="time"
                        label="时间"
                        width="110"
                        :show-overflow-tooltip="true"
                      >
                      </el-table-column>
                    </el-table>
                  </el-col>
                  <el-col :span="8" class="logTable">
                    <el-table
                      v-if="taskDetail.noteLog != undefined"
                      :data="taskDetail.noteLog.slice(0, 10)"
                      :header-cell-style="{ background: '#fff', color: '#222' }"
                      height="100%"
                      style="width: 100%"
                    >
                      <el-table-column
                        label="笔记日志"
                        :show-overflow-tooltip="true"
                      >
                        <template slot-scope="scope">
                          <span
                            :style="
                              scope.row.type === 1
                                ? 'color:#3fbf59'
                                : scope.row.type === 2
                                ? 'color:#3b44db'
                                : 'color:#ed5642'
                            "
                            >【{{ scope.row.user }}】
                            {{
                              scope.row.type === 1
                                ? "新增了"
                                : scope.row.type === 2
                                ? "修改了"
                                : "删除了"
                            }}
                            {{ scope.row.name }}</span
                          >
                        </template>
                      </el-table-column>
                      <el-table-column
                        prop="time"
                        label="时间"
                        width="110"
                        :show-overflow-tooltip="true"
                      >
                      </el-table-column>
                    </el-table>
                  </el-col>
                  <el-col :span="8" class="logTable">
                    <el-table
                      v-if="taskDetail.fileLog != undefined"
                      :data="taskDetail.fileLog.slice(0, 10)"
                      :header-cell-style="{ background: '#fff', color: '#222' }"
                      height="100%"
                      style="width: 100%"
                    >
                      <el-table-column
                        label="文件日志"
                        :show-overflow-tooltip="true"
                      >
                        <template slot-scope="scope">
                          <span
                            :style="
                              scope.row.type === 1
                                ? 'color:#3fbf59'
                                : scope.row.type === 2
                                ? 'color:#3b44db'
                                : 'color:#ed5642'
                            "
                            >【{{ scope.row.user }}】
                            {{
                              scope.row.type === 1
                                ? "新增了"
                                : scope.row.type === 2
                                ? "修改了"
                                : "删除了"
                            }}
                            {{ scope.row.name }}</span
                          >
                        </template>
                      </el-table-column>
                      <el-table-column
                        prop="time"
                        label="时间"
                        width="110"
                        :show-overflow-tooltip="true"
                      >
                      </el-table-column>
                    </el-table>
                  </el-col>
                </el-row>
              </el-form>
            </el-tab-pane>
            <el-tab-pane label="详情信息" name="second" class="firstPane">
              <el-form
                :model="taskDetail"
                label-position="left"
                label-width="80px"
              >
                <el-row :gutter="20" style="height:100%;">
                  <el-col :span="16" style="height:100%;">
                    <div class="detail_box scrollStyle">
                      <el-form-item label="任务名称">
                        <div class="detail_msg">{{ taskDetail.title }}</div>
                      </el-form-item>
                      <el-form-item label="任务描述">
                        <div class="detail_msg">
                          {{ taskDetail.description }}
                        </div>
                      </el-form-item>
                      <el-form-item label="任务时长">
                        <div class="detail_msg">{{ taskDetail.time }}</div>
                      </el-form-item>
                      <el-form-item label="参与人员">
                        <ul class="joinUser">
                          <li
                            v-for="(item, i) in taskDetail.participate"
                            :key="i + 'a'"
                          >
                            <el-tooltip
                              class="item"
                              effect="dark"
                              :content="item.name"
                              placement="top"
                            >
                              <p class="orgTitle">
                                <span class="point"></span>{{ item.name }}
                              </p>
                            </el-tooltip>
                          </li>
                        </ul>
                      </el-form-item>
                    </div>
                  </el-col>
                  <el-col
                    :span="8"
                    style="height:100%;"
                    v-if="taskDetail.hasOwnProperty('timeLine')"
                  >
                    <div class="task_process">
                      <p>任务进程</p>
                      <el-steps
                        class="scrollStyle"
                        direction="vertical"
                        :space="70"
                        :active="taskDetail.timeLine.active"
                      >
                        <el-step
                          v-for="(sLine, index) in taskDetail.timeLine.lineDet"
                          :key="index"
                        >
                          <template slot="title">
                            <span class="setpSty">STEP{{ index + 1 }}</span
                            >{{ sLine.title }}
                          </template>
                          <template slot="description">
                            {{ sLine.time }}
                          </template>
                        </el-step>
                      </el-steps>
                    </div>
                  </el-col>
                </el-row>
              </el-form>
            </el-tab-pane>
            <el-tab-pane
              label="任务笔记"
              name="third"
              class="firstPane scrollStyle"
            >
              <task-note v-if="noteState" ref="noteSon"></task-note>
            </el-tab-pane>
            <el-tab-pane
              label="文件管理"
              name="fourth"
              class="firstPane scrollStyle"
            >
              <el-row :gutter="20" style="height:100%;" v-if="fileState">
                <el-col :span="5" class="directoryTree">
                  <el-tree
                    class="filesTree"
                    ref="fileStr"
                    node-key="id"
                    :load="fileTreeLoadNode"
                    :props="fileTreeProps"
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
                <el-col :span="19" class="fileTableBox">
                  <div
                    style="height: calc(100% - 70px);"
                    v-if="!fileSearchState"
                  >
                    <div class="task_filter">
                      <span class="title">{{ node_name }}</span>
                      <div class="pull_right">
                        <el-button
                          size="small"
                          class="addNote"
                          v-if="node_name !== '根目录'"
                          @click="addFile"
                          round
                          >新增文件 <i class="el-icon-circle-plus-outline"></i>
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
                          class="lookAtLog"
                          @click="fileLogLook"
                          round
                          >查看日志 <i class="el-icon-circle-plus-outline"></i>
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
                    <div class="list_box" v-if="fileNoData">
                      <el-table
                        :data="taskFilesArr"
                        :key="filesTableKey"
                        class="filesTable"
                        height="calc(100% - 50px)"
                      >
                        <el-table-column type="index" label="序号" width="50">
                        </el-table-column>
                        <el-table-column
                          prop="file_name"
                          label="文件名称"
                          show-overflow-tooltip
                        >
                        </el-table-column>
                        <el-table-column
                          prop="create_user"
                          label="创建人"
                        ></el-table-column>
                        <el-table-column
                          prop="score"
                          label="文件描述"
                          show-overflow-tooltip
                        >
                          <template slot-scope="scope">
                            <span>
                              {{ scope.row.description }}
                            </span>
                          </template>
                        </el-table-column>
                        <el-table-column
                          prop="create_time"
                          label="创建时间"
                          width="200"
                        >
                        </el-table-column>
                        <el-table-column label="操作" width="250">
                          <template slot-scope="scope">
                            <el-button
                              title="下载"
                              class="sinProBtn editBtn"
                              type="primary"
                              @click="downloadSinFile(scope.row)"
                            >
                              下载
                            </el-button>
                            <el-button
                              title="删除"
                              class="sinProBtn delBtn"
                              type="success"
                              @click="checkScoreCon(scope.row)"
                            >
                              删除
                            </el-button>
                          </template>
                        </el-table-column>
                      </el-table>
                    </div>
                    <div class="detailNoDataIs" v-show="!fileNoData">
                      <img src="@/assets/img/noData.png" alt="" />
                      <p>暂无数据</p>
                    </div>
                  </div>
                  <div class="searchDetail" v-if="fileSearchState">
                    <ul class="searchCard scrollStyle">
                      <!-- @click="checkSinNote(item)" -->
                      <li
                        v-for="item in fileSearchList"
                        :key="item.id"
                        class="searchItem"
                        style="cursor: default;"
                      >
                        <el-col :span="12">
                          <div>
                            <strong>笔记名称: </strong>
                            <span v-html="item.file_name"></span>
                          </div>
                        </el-col>
                        <el-col :span="12">
                          <div>
                            <strong>创建时间: </strong>{{ item.create_time }}
                          </div>
                        </el-col>
                        <el-col :span="24">
                          <div>
                            <strong>创建人: </strong>{{ item.create_user }}
                          </div>
                        </el-col>
                        <el-col :span="24" class="level">
                          <span class="label">
                            {{ item.box_check }} points
                          </span>
                        </el-col>
                        <el-button
                          title="详情"
                          class="detailBtn"
                          type="primary"
                          @click="downloadSinFile(item)"
                        >
                          下载
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
              </el-row>
            </el-tab-pane>
            <el-tab-pane
              label="漏洞列表"
              name="fifth"
              class="otherPane scrollStyle"
            >
              <div style="text-align: right;">
                <el-button
                  title="新增"
                  type="primary"
                  size="medium"
                  style="height:36px;padding:8px 20px;margin-bottom:10px;background-image: linear-gradient(to right, #5861f0, #3b44db);border-color:#5861f0;"
                  icon="el-icon-circle-plus-outline"
                  @click="addEditBugTask('', 'add')"
                  round
                  >新增漏洞</el-button
                >
              </div>
              <el-table
                :data="taskLeaksArr"
                v-if="detailNoData"
                border
                class="filesTable"
              >
                <el-table-column type="index" label="序号" width="50">
                </el-table-column>
                <el-table-column prop="name" label="名称" show-overflow-tooltip>
                </el-table-column>
                <el-table-column
                  prop="quote"
                  label="引用"
                  show-overflow-tooltip
                >
                </el-table-column>
                <el-table-column
                  prop="describe"
                  label="描述"
                  show-overflow-tooltip
                >
                </el-table-column>
                <el-table-column prop="host" label="主机"> </el-table-column>
                <el-table-column label="等级" width="150">
                  <template slot-scope="scope">
                    <el-tag
                      :type="
                        scope.row.level === 0
                          ? ''
                          : scope.row.level === 1
                          ? 'warning'
                          : 'danger'
                      "
                      disable-transitions
                      >{{
                        scope.row.level === 0
                          ? "低风险"
                          : scope.row.level === 1
                          ? "中风险"
                          : "高风险"
                      }}</el-tag
                    >
                  </template>
                </el-table-column>
                <el-table-column prop="user" label="创建者"> </el-table-column>
                <el-table-column
                  prop="create_time"
                  label="创建时间"
                  width="200"
                >
                </el-table-column>
                <el-table-column label="操作">
                  <template slot-scope="scope">
                    <el-button
                      title="编辑"
                      class="sinProBtn editBtn"
                      type="primary"
                      @click="addEditBugTask(scope.row, 'edit')"
                    >
                      编辑
                    </el-button>
                    <el-button
                      title="删除"
                      class="sinProBtn delBtn"
                      type="primary"
                      @click="delThisData(scope.row, 0)"
                    >
                      删除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane
              label="主机凭证"
              name="sixth"
              class="otherPane scrollStyle"
            >
              <div style="text-align: right;">
                <el-button
                  title="新增"
                  type="primary"
                  size="medium"
                  style="height:36px;padding:8px 20px;margin-bottom:10px;background-image: linear-gradient(to right, #5861f0, #3b44db);border-color:#5861f0;"
                  icon="el-icon-circle-plus-outline"
                  @click="addProof('', 'add')"
                  round
                  >新增凭证</el-button
                >
              </div>
              <el-table :data="taskRolesArr" v-if="detailNoData" border>
                <el-table-column type="index" label="序号" width="50">
                </el-table-column>
                <el-table-column prop="name" label="名称" show-overflow-tooltip>
                </el-table-column>
                <el-table-column label="主机">
                  <template slot-scope="scope">
                    {{ scope.row.ip }}
                  </template>
                </el-table-column>
                <el-table-column prop="user" label="创建者"></el-table-column>
                <el-table-column prop="username" label="用户名">
                </el-table-column>
                <el-table-column prop="password" label="密码">
                </el-table-column>
                <el-table-column label="操作">
                  <template slot-scope="scope">
                    <el-button
                      title="编辑"
                      class="sinProBtn editBtn"
                      type="primary"
                      @click="addProof(scope.row, 'edit')"
                    >
                      编辑
                    </el-button>
                    <el-button
                      title="删除"
                      class="sinProBtn delBtn"
                      type="primary"
                      @click="delThisData(scope.row, 1)"
                    >
                      删除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane
              label="主机列表"
              name="seventh"
              class="otherPane scrollStyle"
            >
              <div style="text-align: right;" v-if="portInfoIs">
                <el-button
                  title="新增"
                  type="primary"
                  size="medium"
                  style="height:36px;padding:8px 20px;margin-bottom:10px;background-image: linear-gradient(to right, #5861f0, #3b44db);border-color:#5861f0;"
                  icon="el-icon-circle-plus-outline"
                  @click="addHost('', 'add')"
                  round
                  >新增主机</el-button
                >
              </div>
              <div v-if="detailNoData" style="height:100%;">
                <el-table :data="taskMastersArr" border v-if="portInfoIs">
                  <el-table-column type="index" label="序号" width="50">
                  </el-table-column>
                  <el-table-column
                    prop="name"
                    label="名称"
                    show-overflow-tooltip
                  >
                  </el-table-column>
                  <el-table-column prop="ip" label="主机IP"></el-table-column>
                  <el-table-column prop="user" label="创建者"></el-table-column>
                  <el-table-column prop="port_count" label="开放端口数量">
                  </el-table-column>
                  <el-table-column label="操作系统">
                    <template slot-scope="scope">
                      <span style="color:#539cff;">
                        {{ scope.row.os_info }}
                      </span>
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" width="280">
                    <template slot-scope="scope">
                      <el-button
                        title="端口信息"
                        class="sinProBtn"
                        type="primary"
                        @click="chenckPortDetail(scope.row)"
                      >
                        端口信息
                      </el-button>
                      <el-button
                        title="编辑"
                        class="sinProBtn editBtn"
                        type="primary"
                        @click="addHost(scope.row, 'edit')"
                      >
                        编辑
                      </el-button>
                      <el-button
                        title="删除"
                        class="sinProBtn delBtn"
                        type="primary"
                        @click="delThisData(scope.row, 2)"
                      >
                        删除
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
                <div class="dnoteDetail" v-if="!portInfoIs">
                  <div class="portList scrollStyle">
                    <div class="postTitle">
                      <i
                        class="iconfont icon-fanhui1"
                        style="cursor: pointer;"
                        @click="portInfoIs = true"
                      ></i>
                      <span>{{
                        portOptId.name !== undefined ? portOptId.name : ""
                      }}</span>
                      <span>/</span>
                      <span>端口列表</span>
                      <el-button
                        title="新增"
                        type="primary"
                        size="medium"
                        class="addPort"
                        icon="el-icon-circle-plus-outline"
                        @click="addPort('', 'add')"
                        round
                        >新增端口</el-button
                      >
                      <el-input
                        class="searchBoxPos portInput"
                        size="small"
                        placeholder="请输入搜索内容"
                        v-model="port_search"
                        @input="enterPortCheck"
                        @keypress.enter.native="checkPortSearch"
                      >
                        <el-button
                          size="small"
                          slot="append"
                          icon="el-icon-search"
                          @click="checkPortSearch"
                        ></el-button>
                      </el-input>
                    </div>
                    <el-table
                      :data="sinHostPortArr"
                      :header-cell-style="{
                        color: '#333',
                        'font-size': '16px'
                      }"
                      border
                      style="width: 100%"
                    >
                      <el-table-column label="序号" width="60" type="index">
                      </el-table-column>
                      <el-table-column prop="name" label="端口名称">
                      </el-table-column>
                      <el-table-column prop="port" label="端口号">
                      </el-table-column>
                      <el-table-column label="操作" width="180px">
                        <template slot-scope="scope">
                          <el-button
                            title="编辑"
                            class="sinProBtn editBtn"
                            type="primary"
                            @click="addPort(scope.row, 'edit')"
                          >
                            编辑
                          </el-button>
                          <el-button
                            title="删除"
                            class="sinProBtn delBtn"
                            type="primary"
                            @click="delThisData(scope.row, 3)"
                          >
                            删除
                          </el-button>
                        </template>
                      </el-table-column>
                    </el-table>
                    <div class="pagePortStyle">
                      <el-pagination
                        @size-change="portSizeChange"
                        @current-change="portCurrentChange"
                        :current-page="port_page"
                        :page-sizes="[10, 25, 50, 100]"
                        :page-size="post_page_size"
                        layout="total, sizes, prev, pager, next, jumper"
                        :total="portTotalSize"
                      >
                      </el-pagination>
                    </div>
                  </div>
                </div>
              </div>
            </el-tab-pane>
            <el-tab-pane
              label="思维导图"
              name="eighth"
              class="otherPane"
              style="height:100%;"
            >
              <mind-maps
                ref="mindmap"
                :taskId="taskId"
                v-show="mindState"
              ></mind-maps>
            </el-tab-pane>
          </el-tabs>
          <div class="detailNoDataIs" v-if="!detailNoData">
            <img src="@/assets/img/noData.png" alt="" />
            <p>暂无数据</p>
          </div>
          <div @click="taskDetailDrawer = false" class="closeBtn">
            <i class="el-icon-arrow-right"></i>
          </div>
        </div>
      </div>
    </el-drawer>
    <!-- 新增文件 -->
    <el-dialog
      :visible.sync="addFileVisible"
      class="addDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
      top="6%"
    >
      <div class="addMain">
        <div class="addTopbar">
          <span class="englishView">新增文件</span>
          <img src="@/assets/img/new_files.png" alt="" />
        </div>
        <el-form
          :model="ruleForm"
          status-icon
          :rules="rules1"
          ref="forms"
          label-width="100px"
          class="weaponForm"
        >
          <el-form-item label="文件上传" prop="file" class="fifty">
            <el-input v-model="ruleForm.fileName" readonly>
              <el-upload
                slot="suffix"
                class="upload-demo"
                ref="upload"
                action="#"
                accept=".txt,.doc,.docx,.xls,.jpg,.png,.md,.pdf,.jpeg,.json"
                :show-file-list="false"
                :auto-upload="false"
                :on-change="changeFile"
              >
                <el-button
                  style="background: #434be0;border-color: #434be0;"
                  slot="trigger"
                  size="small"
                  type="primary"
                  icon="iconfont icon-kaishi"
                ></el-button>
              </el-upload>
            </el-input>
          </el-form-item>
          <el-form-item label="文件描述" prop="description">
            <el-input
              type="textarea"
              :rows="5"
              v-model="ruleForm.description"
            ></el-input>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer" class="addFooter">
        <el-button
          @click="addSubmit"
          type="primary"
          class="sureBtn"
          :loading="loadFileSureAdd"
          >新增文件</el-button
        >
      </div>
    </el-dialog>
    <!-- 文件操作日志 -->
    <el-dialog
      :visible.sync="fileLogVisible"
      class="addDialog flieLog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
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
            v-if="fileLogDetail.length !== 0"
          >
            <div class="rmMiddle" style="padding-left:0;">
              <el-steps
                direction="vertical"
                :space="70"
                :active="fileLogDetail.length"
              >
                <el-step v-for="(sLine, index) in fileLogDetail" :key="index">
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
                        }}“{{ sLine.file_name }}”
                      </p>
                      <p class="time">{{ sLine.create_time }}</p>
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
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <div class="contentPsty">
        此操作将移除任务 {{ delCon }}
        <p
          style="padding:20px 0;text-align:center;font-weight:600;font-size:18px;color:#f66;"
        >
          一旦删除,数据将全部销毁,请谨慎操作!!!
        </p>
      </div>
      <div slot="footer">
        <el-button
          @click="sureDelLink"
          class="btnSure"
          type="warning"
          :loading="loadSureDel"
          >确 定</el-button
        >
        <el-button type="info" class="btnCancle" @click="delVisible = false"
          >取 消</el-button
        >
      </div>
    </el-dialog>
    <!--详情中删除确认模态框-->
    <el-dialog
      :visible.sync="detailDelVisible"
      width="25%"
      top="15%"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <p class="contentPsty" v-html="detailDelCon"></p>
      <div slot="footer">
        <el-button
          @click="sureDetailDelClick"
          class="btnSure"
          type="warning"
          :loading="loadSureDetailDel"
          >确 定</el-button
        >
        <el-button
          type="info"
          class="btnCancle"
          @click="detailDelVisible = false"
          >放 弃</el-button
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
    <!--目录删除确认模态框-->
    <el-dialog
      :visible.sync="delDirVisible"
      width="30%"
      top="15%"
      class="delDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
    >
      <span class="spans">删除目录</span>
      <p class="contentPsty">
        目录及目录下的笔记都将被删除，确认删除?
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
          :loading="loadSureDirDel"
          >确 定</el-button
        >
        <el-button type="info" class="btnCancle" @click="delDirVisible = false"
          >放 弃</el-button
        >
      </div>
    </el-dialog>
    <!-- 漏洞 添加&编辑 -->
    <el-drawer
      :visible.sync="bugEditDrawer"
      size="80%"
      class="addTaskModal"
      :withHeader="false"
    >
      <div
        style="height:100%;"
        v-loading="detailLoading"
        element-loading-text="数据加载中"
        element-loading-background="rgba(0, 0, 0, 0.6)"
      >
        <div class="addTaskBox">
          <div class="addModalTop" style="padding: 50px 70px;">
            <span class="englishView">{{
              bugType === "add" ? "添加漏洞" : "编辑漏洞"
            }}</span>
            <img
              :src="
                bugType === 'add'
                  ? require('@/assets/img/new_bug.png')
                  : require('@/assets/img/edit_bug.png')
              "
              alt=""
            />
          </div>
          <div
            style="height:calc(100% - 50px);width:100%;padding:20px"
            class="scrollStyle"
          >
            <el-form
              ref="bugEditForm"
              class="editor scrollStyle"
              :model="bugEditForm"
              :rules="noteAddRules"
              label-position="left"
              label-width="80px"
              style="height:100%"
            >
              <el-form-item label="选择主机" prop="host_id">
                <el-select
                  v-model="bugEditForm.host_id"
                  style="width: 30%;"
                  placeholder="筛选主机"
                >
                  <el-option
                    v-for="(item, index) in hostEnum"
                    :key="index"
                    :label="item.name + '(' + item.ip + ')'"
                    :value="item.id"
                  ></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="漏洞名称" prop="name">
                <el-input
                  v-model="bugEditForm.name"
                  style="width: 30%;"
                ></el-input>
              </el-form-item>
              <el-form-item label="漏洞等级" prop="level">
                <el-radio-group class="bug_radio" v-model="bugEditForm.level">
                  <el-radio-button :label="0">低风险</el-radio-button>
                  <el-radio-button :label="1">中风险</el-radio-button>
                  <el-radio-button :label="2">高风险</el-radio-button>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="漏洞描述" prop="description">
                <tinymce
                  ref="bugdescirbeedit"
                  :id="'bugdescirbeedit'"
                  :height="300"
                  :tinyVal="bugEditForm.description"
                ></tinymce>
              </el-form-item>
              <el-form-item label="漏洞引用" prop="quote">
                <tinymce
                  ref="bugquoteedit"
                  :id="'bugquoteedit'"
                  :height="300"
                  :tinyVal="bugEditForm.quote"
                ></tinymce>
              </el-form-item>
            </el-form>
          </div>
          <el-button
            @click="sureAddBug"
            type="primary"
            class="sureBtn sureEdit"
            :loading="loadSureAdd"
            >{{ bugType === "add" ? "确认添加" : "保存编辑" }}</el-button
          >
        </div>
        <div @click="bugEditDrawer = false" class="closeBtn">
          <i class="el-icon-arrow-right"></i>
        </div>
      </div>
    </el-drawer>
    <!-- 主机凭证 创建&编辑-->
    <el-dialog
      :visible.sync="addProofVisible"
      class="addDialog"
      width="45%"
      top="6%"
      :withHeader="false"
    >
      <div class="addMain">
        <div class="addTopbar">
          <span class="englishView">{{
            proofType === "add" ? "新建凭证" : "编辑凭证"
          }}</span>
          <img
            :src="
              proofType === 'add'
                ? require('@/assets/img/new_proof.png')
                : require('@/assets/img/img_Editcertificate.png')
            "
            alt=""
          />
        </div>
        <el-form
          ref="proofAddForm"
          class="editor scrollStyle"
          :model="proofAddForm"
          :rules="noteAddRules"
          label-position="left"
          label-width="80px"
          style="height:80%"
        >
          <el-form-item label="凭证名称" prop="name">
            <el-input
              style="width:50%"
              v-model.trim="proofAddForm.name"
              placeholder="请输入凭证名称"
            >
            </el-input>
          </el-form-item>
          <el-form-item label="主机IP" prop="host_id">
            <el-select
              style="width:50%"
              v-model="proofAddForm.host_id"
              placeholder="请选择主机IP"
            >
              <el-option
                :value="item.id"
                :label="item.ip"
                v-for="(item, index) in IPEnum"
                :key="index"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label=" 用户名" prop="username">
            <el-input
              style="width:50%"
              v-model.trim="proofAddForm.username"
              placeholder="请输入用户名"
            >
            </el-input>
          </el-form-item>
          <el-form-item label="登录密码" prop="password">
            <el-input
              style="width:50%"
              v-model.trim="proofAddForm.password"
              placeholder="请输入登录密码"
            >
            </el-input>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer" class="addFooter">
        <el-button
          @click="sureAddProof"
          type="primary"
          class="sureBtn"
          :loading="loadSureAdd"
          >{{ proofType === "add" ? "创建凭证" : "确认修改" }}</el-button
        >
      </div>
    </el-dialog>
    <!-- 主机 创建&编辑 -->
    <el-dialog
      :visible.sync="addHostVisible"
      class="addDialog"
      width="30%"
      top="6%"
      :withHeader="false"
    >
      <div class="addMain">
        <div class="addTopbar">
          <span class="englishView">{{
            hostType === "add" ? "新建主机" : "编辑主机"
          }}</span>
          <img
            :src="
              hostType === 'add'
                ? require('@/assets/img/new_host.png')
                : require('@/assets/img/img_edithost.png')
            "
            alt=""
          />
        </div>
        <el-form
          ref="hostAddForm"
          class="editor scrollStyle"
          :model="hostAddForm"
          :rules="noteAddRules"
          label-position="left"
          label-width="80px"
        >
          <el-form-item label="主机名称" prop="name">
            <el-input
              v-model.trim="hostAddForm.name"
              placeholder="请输入主机名称"
            >
            </el-input>
          </el-form-item>
          <el-form-item label="主机IP" prop="ip">
            <el-input v-model.trim="hostAddForm.ip" placeholder="请输入主机IP">
            </el-input>
          </el-form-item>
          <el-form-item label="操作系统" prop="os_info">
            <el-select
              style="width:100%"
              v-model="hostAddForm.os_info"
              placeholder="请选择操作系统"
            >
              <el-option
                :value="item"
                :label="item"
                v-for="(item, index) in systemEnum"
                :key="index"
              ></el-option>
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer" class="addFooter">
        <el-button
          @click="sureAddHost"
          type="primary"
          class="sureBtn"
          :loading="loadSureAdd"
          >{{ hostType === "add" ? "创建主机" : "确认修改" }}</el-button
        >
      </div>
    </el-dialog>
    <!--漏洞凭证主机删除确认模态框-->
    <el-dialog
      :visible.sync="delProofVisible"
      width="30%"
      top="15%"
      class="delDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
    >
      <p class="contentPsty" style="font-size: 18px;color: #333;">
        {{
          this.selectRowType === 0
            ? "确认删除该漏洞?"
            : this.selectRowType === 1
            ? "确认删除该凭证?"
            : this.selectRowType === 2
            ? "确认删除该主机?"
            : "确认删除该端口?"
        }}
      </p>
      <div slot="footer">
        <el-button
          @click="sureDelProof"
          class="btnSure"
          type="warning"
          :loading="loadSureProofDel"
          >确 定</el-button
        >
        <el-button
          type="info"
          class="btnCancle"
          @click="delProofVisible = false"
          >放 弃</el-button
        >
      </div>
    </el-dialog>
    <!-- 端口 创建&编辑 -->
    <el-dialog
      :visible.sync="addPortVisible"
      class="addDialog"
      width="40%"
      top="6%"
      :withHeader="false"
    >
      <div class="addMain">
        <div class="addTopbar">
          <span class="englishView">{{
            portType === "add" ? "新建端口" : "编辑端口"
          }}</span>
          <img
            :src="
              portType === 'add'
                ? require('@/assets/img/img_newport.png')
                : require('@/assets/img/img_editport.png')
            "
            alt=""
          />
        </div>
        <el-form
          ref="portAddForm"
          class="editor scrollStyle"
          :model="portAddForm"
          :rules="noteAddRules"
          label-position="left"
          label-width="80px"
        >
          <el-form-item label="端口名称" prop="port_name">
            <el-input
              v-model.trim="portAddForm.port_name"
              placeholder="请输入端口名称"
            >
            </el-input>
          </el-form-item>
          <el-form-item label="端口号" prop="port">
            <el-input
              v-model.trim="portAddForm.port"
              placeholder="请输入端口号"
            >
            </el-input>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer" class="addFooter">
        <el-button
          @click="sureAddPort"
          type="primary"
          class="sureBtn"
          :loading="loadSureAdd"
          >{{ portType === "add" ? "创建端口" : "确认修改" }}</el-button
        >
      </div>
    </el-dialog>
    <!-- 全局搜索 -->
    <el-drawer
      :visible.sync="allSearchVisible"
      size="80%"
      class="addTaskModal"
      :withHeader="false"
      :append-to-body="true"
    >
      <div
        style="height:100%;"
        v-loading="allSearchLoad"
        element-loading-text="数据加载中"
        element-loading-background="rgba(0, 0, 0, 0.6)"
      >
        <div class="addTaskBox">
          <div class="allSearchTop">
            <el-input
              placeholder="请输入内容"
              v-model="searchInfo"
              class="inputInfo"
              @input="enterAllCheck"
              @keypress.enter.native="clickAllCheck"
            >
              <el-select
                v-model="infoType"
                class="selectBefore"
                slot="prepend"
                placeholder="请选择"
                @change="allSearchSelect"
              >
                <el-option label="笔记" value="note"></el-option>
                <el-option label="文件" value="file"></el-option>
                <el-option label="主机" value="host"></el-option>
                <el-option label="知识库" value="knowledge"></el-option>
              </el-select>
              <el-button
                slot="append"
                icon="iconfont icon-jiansuo"
                @click="allSearchList"
              ></el-button>
            </el-input>
          </div>
          <el-row
            :gutter="50"
            class="scrollStyle"
            style="margin:0;padding: 30px 10px 0;transform: scale(1);height: 100%;background: #fff;"
          >
            <el-col :span="24" v-if="infoData !== null">
              <el-table
                :data="infoData"
                v-if="infoType === 'note' || infoType === 'knowledge'"
                border
                class="filesTable"
              >
                <el-table-column label="笔记名称" show-overflow-tooltip>
                  <template slot-scope="scope">
                    <span v-html="scope.row.note_name"></span>
                  </template>
                </el-table-column>
                <el-table-column label="笔记内容" show-overflow-tooltip>
                  <template slot-scope="scope">
                    <span v-html="scope.row.note_contetn"></span>
                  </template>
                </el-table-column>
                <el-table-column label="所属任务" show-overflow-tooltip>
                  <template slot-scope="scope">
                    <span v-html="scope.row.task_name"></span>
                  </template>
                </el-table-column>
                <el-table-column
                  v-if="infoType === 'note'"
                  label="所在位置"
                  show-overflow-tooltip
                >
                  <template slot-scope="scope">
                    <span v-html="scope.row.note_path"></span>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="90">
                  <template slot-scope="scope">
                    <el-button
                      title="查看"
                      class="sinProBtn editBtn"
                      type="primary"
                      @click="goinDetail(scope.row, infoType)"
                    >
                      查看
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
              <el-table
                :data="infoData"
                v-if="infoType === 'file'"
                border
                class="filesTable"
              >
                <el-table-column label="文件名称" show-overflow-tooltip>
                  <template slot-scope="scope">
                    <span v-html="scope.row.file_name"></span>
                  </template>
                </el-table-column>
                <el-table-column label="所属任务" show-overflow-tooltip>
                  <template slot-scope="scope">
                    <span v-html="scope.row.task_name"></span>
                  </template>
                </el-table-column>
                <el-table-column label="所在位置" show-overflow-tooltip>
                  <template slot-scope="scope">
                    <span v-html="scope.row.file_path"></span>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="90">
                  <template slot-scope="scope">
                    <el-button
                      title="查看"
                      class="sinProBtn editBtn"
                      type="primary"
                      @click="goinDetail(scope.row, infoType)"
                    >
                      查看
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
              <el-table
                :data="infoData"
                v-if="infoType === 'host'"
                border
                class="filesTable"
              >
                <el-table-column label="主机名称" show-overflow-tooltip>
                  <template slot-scope="scope">
                    <span v-html="scope.row.host_name"></span>
                  </template>
                </el-table-column>
                <el-table-column label="主机IP" show-overflow-tooltip>
                  <template slot-scope="scope">
                    <span v-html="scope.row.host_ip"></span>
                  </template>
                </el-table-column>
                <el-table-column label="所属任务" show-overflow-tooltip>
                  <template slot-scope="scope">
                    <span v-html="scope.row.task_name"></span>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="90">
                  <template slot-scope="scope">
                    <el-button
                      title="查看"
                      class="sinProBtn editBtn"
                      type="primary"
                      @click="goinDetail(scope.row, infoType)"
                    >
                      查看
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
              <div class="pagePortStyle" v-if="infoData !== null">
                <el-pagination
                  @size-change="allSizeChange"
                  @current-change="allCurrentChange"
                  :current-page="all_page"
                  :page-sizes="[10, 25, 50, 100]"
                  :page-size="all_page_size"
                  layout="total, sizes, prev, pager, next, jumper"
                  :total="allTotalSize"
                >
                </el-pagination>
              </div>
            </el-col>
            <el-col
              :span="24"
              class="listDetail"
              v-if="infoData === null && searchInfo !== ''"
              style="height:100%;padding: 30px 40px;"
            >
              <div class="noData">
                <img src="@/assets/img/noData.png" style="margin-top: 20%;" />
                <div>暂无数据</div>
              </div>
            </el-col>
            <el-col
              :span="24"
              class="listDetail"
              v-if="searchInfo === ''"
              style="height:100%;padding: 30px 40px;"
            >
              <div class="noData">
                <img src="@/assets/img/nodata1.png" />
                <div>请输入关键字查询</div>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>
      <div @click="allSearchVisible = false" class="closeBtn">
        <i class="el-icon-arrow-right"></i>
      </div>
    </el-drawer>
  </div>
</template>
<script>
/* eslint-disable */
import {
  taskList,
  taskDetails,
  allUser,
  taskFiles,
  taskLeaks,
  addBug,
  delBug,
  taskRoles,
  addProof,
  delProof,
  taskMasters,
  optHost,
  portDetail,
  taskAdd,
  taskEdit,
  taskDel,
  fileAdd,
  fileDel,
  fileDirAdd,
  fileDirEdit,
  fileDirDelete,
  logDetails,
  taskNoteSearch,
  portOperation,
  allSearch
} from "@/api/task";
import taskNote from "./taskNote";
import mindMaps from "./mindMaps";
// import mindmap from "@hellowuxin/mindmap";
import tinymce from "./tinymce-editor";
import { isIp,isPort } from "@/assets/js/validate";
var ipCheck = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入主机IP'));
  } else if (!isIp(value)) {
    callback(new Error('请输入正确的IP'));
  } else {
    callback();
  }
};
var portCheck = (rule, value, callback) => {
  if (!isPort(value)) {
    callback(new Error('请输入正确的端口号(端口范围0-65535)'));
  } else {
    callback();
  }
};
export default {
  name: "taskList",
  components: {
    taskNote,
    tinymce,
    mindMaps
  },
  data() {
    return {
      task_permission: 0, // 0为普通用户 1为管理员
      firstState: 0,
      fileIdCon: null,
      listLoading: false,
      proListData: [],
      search: "",
      createTime: "",
      page: 1,
      page_size: 10,
      totalSize: 0,
      delVisible: false,
      loadSureDel: false,
      taskType: "add",
      userList: [], // 任务新增与编辑中的用户列表
      delCon: "",
      leakId: null,
      multipleSelection: [],
      restaurants: [],
      addVisible: false,
      loadSureAdd: false,
      stopVisible: false,
      loadSureStop: false,
      restartVisible: false,
      loadSureRestart: false,
      exportVisible: false,
      loadSureExport: false,
      site: [],
      checkList: [],
      form: {
        name: "",
        describe: "",
        time: "",
        participant: []
      },
      taskId: "",
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
      rules: {
        name: [
          {
            required: true,
            message: "请输入任务名称",
            trigger: "blur"
          },
          { min: 1, max: 16, message: '名称长度在 1 到 16 个字符', trigger: 'blur' }
        ],
        describe: [
          {
            required: true,
            message: "请输入任务描述",
            trigger: "blur"
          },
          { min: 1, max: 120, message: '描述长度在 1 到 120 个字符', trigger: 'blur' }
        ],
        time: [
          {
            required: true,
            message: "请选择任务时长",
            trigger: "blur"
          }
        ],
        participant: [
          {
            required: true,
            message: "请选择任务指派对象",
            trigger: "change"
          }
        ]
      },
      taskDetailDrawer: false,
      taskDetail: {},
      noDataIs: true,
      noFarrIds: [],
      activeName: "first",
      // userBelong: [],
      // defaultProps: {
      //   children: "children",
      //   label: "label"
      // },
      // modalArr: [],
      // masterArr: [],
      // weapon: [],
      // addModalList: [],
      reviewDrawer: false,
      detailSearch: "",
      detailPage: 1,
      detailSize: 10,
      detailTotalSize: -1,
      pageSizeArr: [],
      taskNotesArr: [],
      // 文件相关
      is_load: false,
      noteState: false,
      fileNoData: false,
      filesTableKey: "",
      noteChoose: 'name',
      // 任务 --- 文件管理
      filePageState: false, // 管理分页功能状态
      fileState: false,
      taskFilesArr: [],
      fileTreeProps: {
        children: "sub_dir",
        label: "dir_name"
        // isLeaf: 'leaf'
      },
      node_name: "根目录",
      node: null,
      resolve: null,
      taskRolesArr: [],
      addFileVisible: false,
      ruleForm: {
        file: "",
        fileName: "",
        size: "",
        description: ""
      },
      rules1: {
        fileName: [{ required: true, message: "请上传文件", trigger: "blur" }],
        description: [
          { required: true, message: "请输入文件描述", trigger: "blur" },
          { min: 1, max: 120, message: '描述长度在 1 到 120 个字符', trigger: 'blur' }
        ]
      },
      loadFileSureAdd: false,
      fileLogVisible: false,
      fileLogDetail: [],
      taskLeaksArr: [],
      taskRolesArr: [],
      taskMastersArr: [],
      // 文件搜索
      fileSearchList: [],
      fileSearchState: false,
      search_page: 1,
      search_page_size: 10,
      searchTotalSize: 0,
      // 目录操作
      addDirectoryVisible: false,
      directory_type: "add",
      directory_name: "",
      loadDirSure: false,
      loadSureDirDel: false,
      delDirVisible: false,
      // 详情
      detailGetLoading: false,
      taskId: null,
      notesListShow: true,
      sinNote: {},
      oldNoteContent: "",
      detailNoData: true,
      detailDelVisible: false,
      detailDelCon: "",
      loadSureDetailDel: false,
      loadSureSaveNoteEdit: false,
      isNoNoteEdit: true,
      noteEditIs: false,
      noteEdittwoArea: false,
      hostChoose: "",
      // 漏洞操作
      hostEnum: [],
      bugType: 'add',
      bugRowData: null,
      bugEditDrawer: false,
      detailLoading: false,
      bugEditForm: {
        host_id: "",
        name: "",
        level: "",
        description: "",
        quote: ""
      },
      // 验证规则
      noteAddRules: {
        title: [
          { required: true, message: "请输入笔记标题", trigger: "blur" },
          { min: 1, max: 16, message: '标题长度在 1 到 16 个字符', trigger: 'blur' }
        ],
        roleSee: [
          { required: true, message: "请选择查看权限", trigger: "blur change" }
        ],
        // content: [
        //   { required: true, message: "请输入笔记内容", trigger: "blur" }
        // ],
        note_type: [
          { required: true, message: "请选择笔记类型", trigger: "blur change" }
        ],
        name: [
          { required: true, message: "请输入名称", trigger: "blur" },
          { min: 1, max: 16, message: '名称长度在 1 到 16 个字符', trigger: 'blur' }
        ],
        host_id: [
          { required: true, message: "请选择主机", trigger: "blur change" }
        ],
        ip: [
          { required: true, validator: ipCheck, trigger: "blur" }
        ],
        username: [
          { required: true, message: "请输入账号用户名", trigger: "blur" },
          { min: 1, max: 16, message: '用户名长度在 1 到 16 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入登录密码', trigger: 'blur' },
          { min: 1, max: 32, message: '密码长度在 1 到 32 个字符', trigger: 'blur' }
        ],
        os_info: [
          { required: true, message: "请选择操作系统", trigger: "blur change" }
        ],
        level: [
          { required: true, message: "请选择漏洞等级", trigger: "blur change" }
        ],
        port_name:[
          { min: 1, max: 64, message: '名称长度在 1 到 64 个字符', trigger: 'blur' }
        ],
        port: [
          { validator: portCheck, trigger: 'blur' }
        ]
      },
      // 主机凭证
      addProofVisible: false, // 主机凭证新增弹框
      IPEnum: [],
      proofAddForm: {
        name: "",
        host_id: "",
        username: "",
        password: ""
      },
      proofType: 'add',
      proofRowData: null,
      // 主机
      systemEnum:[
        'Windows','Linux','MacOS','未知'
      ],
      addHostVisible: false, // 主机新增弹框
      hostAddForm: {
        name: "",
        ip: "",
        os_info: "",
        ports: ""
      },
      hostType: 'add',
      hostRowData: null,
      portInfoIs: true,
      sinHostPortArr: [],
      mindState: false,
      // 主机--端口操作
      port_search: '',
      post_page_size: 10,
      port_page: 1,
      portOptId: null,
      portTotalSize: 0,
      addPortVisible: false,
      portAddForm: {
        port_name: "",
        port: 0
      },
      portType: 'add',
      portRowData: null,
      // 漏洞、凭证、主机共用
      delThisRow: null,
      selectRowType: 0,
      delProofVisible: false,
      loadSureProofDel: false,
      // 全局检索
      allSearchVisible: false,
      allSearchLoad: false,
      infoType: "note",
      oldInfoType: "",
      searchInfo: "",
      infoData: null,
      all_page: 1,
      all_page_size:10,
      allTotalSize: 0
    };
  },
  computed: {
    base_info() {
      return this.$store.getters.base;
    }
  },
  watch: {
    detailTotalSize(val) {
      if (val === 0) {
        this.detailNoData = false;
      } else {
        this.detailNoData = true;
      }
    }
  },
  mounted() {
    //this.adminUser = this.$store.getters.roles[0] === "admin" ? true : false;
    this.getAllLeakList();
    this.getAllUserList();
  },
  created() {},
  methods: {
    // 获取用户列表
    getAllUserList() {
      allUser()
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
    // 获取任务列表
    getAllLeakList() {
      var sendD = {
        keyword: this.search,
        page: this.page,
        max_count: this.page_size
      };
      this.listLoading = true;
      taskList(sendD)
        .then(response => {
          this.listLoading = false;
          if (response.data.success) {
            this.proListData = response.data.data;
            this.totalSize = response.data.total;
            this.task_permission = response.data.task_permission;
            if (this.totalSize == 0) {
              this.noDataIs = false;
            } else {
              this.noDataIs = true;
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
    // 关键词搜索
    enterCheck(val) {
      if (val == "") {
        this.page = 1;
        this.page_size = 10;
        this.getAllLeakList();
      }
    },
    clickCheck() {
      if (this.search != "") {
        this.page = 1;
        this.getAllLeakList();
      }
    },
    // 分页
    handleSizeChange(val) {
      this.page_size = val;
      this.getAllLeakList();
    },
    handleCurrentChange(val) {
      this.page = val;
      this.getAllLeakList();
    },
    // 新增单个任务
    addEditSinTask(row, type) {
      this.taskType = type;
      if (type === "edit") {
        this.form = {
          name: row.title,
          describe: row.description,
          time: [new Date(row.start_time), new Date(row.end_time)],
          participant: row.particpant
        };
        this.taskId = row.task_id;
      } else {
        this.form = {
          name: "",
          describe: "",
          time: "",
          participant: []
        };
      }
      var f = this.$refs["form"];
      if (f != undefined && f != null) {
        this.$refs["form"].resetFields();
      }
      this.addVisible = true;
    },
    sureAddTask() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          this.loadSureAdd = true;
          let sendD = {
            title: this.form.name,
            description: this.form.describe,
            participant: this.form.participant,
            end_time: this.form.time[1],
            start_time: this.form.time[0]
          };
          if (this.taskType === "edit") {
            sendD.task_id = this.taskId;
            taskEdit(sendD, this.$store.getters.token)
              .then(response => {
                this.loadSureAdd = false;
                if (response.data.success) {
                  this.addVisible = false;
                  this.getAllLeakList();
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
            taskAdd(sendD)
              .then(response => {
                this.loadSureAdd = false;
                if (response.data.success) {
                  this.addVisible = false;
                  this.getAllLeakList();
                } else {
                  this.$message.warning(response.data.info);
                }
              })
              .catch(error => {
                this.loadSureAdd = false;
                this.addVisible = false;
                this.$message.error(error.message);
              });
          }
        } else {
          this.$message.error("请完善各项内容");
          return false;
        }
      });
    },
    // 查看详情
    checkDetail(row) {
      this.$store.commit("getTaskId", row.task_id);
      this.taskId = row.task_id;
      this.activeName = "first";
      this.taskDetailDrawer = true;
      this.detailGetLoading = true;
      this.checkFirst();
    },
    // 详情信息获取
    checkFirst() {
      this.detailTotalSize = -1;
      taskDetails(this.taskId)
        .then(response => {
          this.detailGetLoading = false;
          if (response.data.success) {
            this.taskDetail = response.data.data;
            this.progressChart(
              "progressTask",
              this.taskDetail.process,
              "#08ccc2",
              ["#0dd1be", "#2dfda5"]
            );
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.detailGetLoading = false;
          this.$message.error(error.message);
        });
    },
    progressChart(chartId, value, txt_color, gradient) {
      let chart = this.$echarts.init(document.getElementById(chartId));
      let opition = {
        backgroundColor: "#fff",
        title: [
          {
            text: "任务进度",
            left: "48%",
            top: "57%",
            textAlign: "center",
            textStyle: {
              fontWeight: "normal",
              fontSize: "14",
              color: "#666",
              textAlign: "center"
            }
          }
        ],
        series: [
          {
            type: "pie",
            clockWise: true,
            hoverAnimation: false, //鼠标经过的特效
            radius: ["53%", "85%"],
            center: ["50%", "50%"],
            labelLine: {
              normal: {
                show: false
              }
            },
            label: {
              normal: {
                position: "center"
              }
            },
            data: [
              {
                value: value, // 环形百分比
                itemStyle: {
                  normal: {
                    color: {
                      colorStops: [
                        {
                          offset: 0, //颜色的开始位置
                          color: gradient[0] // 0% 处的颜色
                        },
                        {
                          offset: 1, //颜色的结束位置
                          color: gradient[1] // 100% 处的颜色
                        }
                      ]
                    }
                  }
                },
                label: {
                  normal: {
                    formatter: "{c}%",
                    position: "center",
                    show: true,
                    textStyle: {
                      fontSize: "30",
                      fontWeight: "bold",
                      color: txt_color
                    }
                  }
                }
              },
              {
                value: 100 - value,
                itemStyle: {
                  normal: {
                    color: "#efefef"
                  }
                }
              }
            ]
          }
        ]
      };
      chart.setOption(opition, true);
      window.addEventListener("resize", () => {
        chart.resize();
      });
    },
    // 删除协同导图
    sinDetailDel(sin) {
      this.mind_id = sin.id;
      let span =
        '<span style="font-weight:600;padding-left:15px;">' +
        sin.title +
        "</span>";
      this.detailDelCon = "是否确认删除协同导图" + span + "?";
    },
    // 确认删除
    // sureDetailDelClick() {
    //   this.loadSureDetailDel = true;
    //   const sendd = {
    //     mind_id: this.mind_id,
    //     is_delete: true
    //   };
    //   delMind(sendd)
    //     .then(response => {
    //       this.loadSureDetailDel = false;
    //       this.detailDelVisible = false;
    //       if (response.data.success) {
    //         this.$message.success("删除成功!");
    //         if (this.taskMindsArr.length === 1) {
    //           this.detailPage = 1;
    //         }
    //         this.checkSeventh();
    //       } else {
    //         this.$message.warning(response.data.info);
    //       }
    //     })
    //     .catch(error => {
    //       this.loadSureDetailDel = false;
    //       this.detailDelVisible = false;
    //       this.$message.error(error.message);
    //     });
    // },
    // 文件管理
    // 树节点
    // 懒加载
    fileTreeLoadNode(node, resolve) {
      // console.log(this.detailPage)
      if(!this.filePageState){
        this.detailPage = 1
      }
      this.is_load = false;
      this.fileNoData = true;
      this.fileSearchState = false
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
      taskFiles(sendD)
        .then(response => {
          this.is_load = true;
          if (response.data.success) {
            this.filePageState =  false
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
            let d = response.data.data.file_info;
            if (d.length === 0) {
              this.fileNoData = false;
              return false;
            }
            this.taskFilesArr = d;
            this.filesTableKey = Math.random();
            this.detailTotalSize = response.data.data.total;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    handleNodeClick(data){
      this.fileSearchState = false
      if(this.is_load){
        if(data.dir_name !== "根目录"){
          let node = this.$refs.fileStr.getNode(data.id); // 通过节点id找到对应树节点对象
          node.loaded = false;
          node.expand();
        }else{
          let node = this.$refs.fileStr.getNode(0); // 通过节点id找到对应树节点对象
          node.loaded = false;
          node.expand();
        }
      }
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
        if (this.node.data !== undefined && this.node.data.dir_name !== "根目录") {
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
        fileDirAdd(sendD)
          .then(response => {
            this.loadDirSure = false;
            this.addDirectoryVisible = false;
            if (response.data.success) {
              if(this.node.data !== undefined && this.node.data.dir_name !== "根目录"){
                let node = this.$refs.fileStr.getNode(this.node.parent.data.id); // 通过节点id找到对应树节点对象
                node.loaded = false;
                node.expand();
              }else{
                let node = this.$refs.fileStr.getNode(0);
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
        fileDirEdit(sendD)
          .then(response => {
            this.loadDirSure = false;
            this.addDirectoryVisible = false;
            if (response.data.success) {
              if(this.node.data !== undefined && this.node.data.dir_name !== "根目录"){
                let node = this.$refs.fileStr.getNode(this.node.parent.data.id); // 通过节点id找到对应树节点对象
                node.loaded = false;
                node.expand();
              }else{
                let node = this.$refs.fileStr.getNode(0);
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
      this.dialogData = this.node;
      this.delDirVisible = true;
    },
    // 目录确认删除
    sureEdit() {
      this.loadSureDel = true;
      var data = {
          dir_id: this.dialogData.data.id,
        };
        fileDirDelete(data)
          .then(res => {
            this.loadSureDel = false;
            if (res.data.success) {
              this.$message.success("删除成功");
              let node = this.$refs.fileStr.getNode(this.node.parent.data.id); // 通过节点id找到对应树节点对象
              node.loaded = false;
              node.expand();
            } else {
              this.$message.warning(res.data.info);
            }
            this.delDirVisible = false;
          })
          .catch(error => {
            this.loadSureDel = false;
            this.delDirVisible = false;
            this.$message.error(error.message);
          });
    },
    // 上传文件
    changeFile(file) {
      let isJPGCon = file.name.split(".");
      isJPGCon = isJPGCon[isJPGCon.length - 1];
      let st = [
        "txt",
        "doc",
        "docx",
        "xls",
        "jpg",
        "png",
        "md",
        "pdf",
        "jpeg",
        "json"
      ];
      if (st.indexOf(isJPGCon) < 0) {
        this.$message.warning("文件仅限txt, doc, docx, xls, jpg, png, md, pdf, jpeg, json格式");
        return;
      }
      this.ruleForm.fileName = file.name;
      this.ruleForm.file = file.raw;
      this.ruleForm.size = this.$bytesToSize(file.size);
    },
    addFile() {
      var f = this.$refs["forms"];
      if (f != undefined && f != null) {
        this.$refs["forms"].resetFields();
      }
      this.ruleForm = {
        file: "",
        fileName: "",
        size: "",
        description: ""
      }
      this.addFileVisible = true;
    },
    // 新增文件
    addSubmit() {
      this.$refs["forms"].validate(valid => {
        if (valid) {
          this.loadFileSureAdd = true;
          const sendD = new FormData();
          sendD.append("p_dir_id", this.node.data.id);
          sendD.append("file", this.ruleForm.file);
          sendD.append("description", this.ruleForm.description);
          fileAdd(sendD)
            .then(response => {
              this.loadFileSureAdd = false;
              this.addFileVisible = false;
              if (response.data.success) {
                this.detailPage = 1
                this.fileTreeLoadNode(this.node, this.resolve);
              } else {
                this.$message.warning(response.data.info);
              }
            })
            .catch(error => {
              this.loadFileSureAdd = false;
              this.addFileVisible = false;
              this.$message.error(error.message);
            });
        } else {
          this.$message.error("请完善各项内容");
          return false;
        }
      });
    },
    // 文件下载
    downloadSinFile(row) {
      const a = document.createElement("a");
      a.href =
        "http://192.168.8.243:10000/api/file/v1/download_file?file_id=" +
        row.file_id;
      // +
      // "&token=" +
      // this.$store.getters.token;
      a.download = row.file_name;
      document.querySelector("body").appendChild(a);
      a.click();
      document.querySelector("body").removeChild(a);
    },
    // 文件删除
    checkScoreCon(row) {
      this.fileIdCon = row.file_id;
      let span =
        '<span style="font-weight:600;padding-left:15px;">' +
        row.file_name +
        "</span>";
      this.detailDelCon = "是否确认删除文件" + span + "?";
      this.detailDelVisible = true;
    },
    // 确认删除
    sureDetailDelClick() {
      this.loadSureDetailDel = true;
      const sendd = {
        file_id: this.fileIdCon
      };
      fileDel(sendd)
        .then(response => {
          this.loadSureDetailDel = false;
          this.detailDelVisible = false;
          if (response.data.success) {
            this.$message.success("删除成功!");
            this.detailPage = 1
            this.fileTreeLoadNode(this.node, this.resolve)
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.loadSureDetailDel = false;
          this.detailDelVisible = false;
          this.$message.error(error.message);
        });
    },
    // 文件查看日志
    fileLogLook() {
      var sendD = {
        task_id: this.taskId,
        key_word: "file"
      };
      logDetails(sendD)
        .then(response => {
          if (response.data.success) {
            this.fileLogVisible = true;
            this.fileLogDetail = response.data.data;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    // 文件搜索
    fileSearch(search, flag){
      let send = {
        task_id: this.taskId,
        search: search,
        page: this.search_page,
        max_count: this.search_page_size,
        keyword: 'file',
        flag: flag
      }
      taskNoteSearch(send)
        .then(response => {
          if (response.data.success) {
            let d = response.data.data
            for(let i=0;i<d.length;i++){
              d[i].file_name = this.brightenKeyword(d[i].file_name, search)
            }
            this.fileSearchList = d
            this.fileSearchState = true;
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
    searchSizeChange(val){
      this.search_page = 1;
      this.search_page_size = val;
      this.fileSearch(this.detailSearch, '')
    },
    searchCurrentChange(val) {
      this.search_page = val;
      this.fileSearch(this.detailSearch, '')
    },
    // 数据概览获取
    checkSecond() {
      this.detailGetLoading = false;
    },
    // 清除form表单
    formReset(form) {
      var f = this.$refs[form];
      if (f != undefined && f != null) {
        this.$refs[form].resetFields();
      }
    },
    // 漏洞列表获取
    checkFifth() {
      var sendD = {
        id: this.taskId,
        search: this.detailSearch,
        page: this.detailPage,
        pageSize: this.detailSize
      };
      taskLeaks(sendD)
        .then(response => {
          this.detailGetLoading = false;
          if (response.data.success) {
            this.taskLeaksArr = response.data.data;
            this.detailTotalSize = response.data.total;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.detailGetLoading = false;
          this.$message.error(error.message);
        });
    },
    // 漏洞操作
    addEditBugTask(row, type) {
      this.getHostList();
      this.bugType = type;
      this.bugEditDrawer = true;
      this.detailLoading = true;
      if (type === "add") {
        setTimeout(() => {
          this.$set(this.bugEditForm, "description", "");
          this.$set(this.bugEditForm, "quote", "");
          this.detailLoading = false;
        }, 500);
        this.formReset("bugEditForm");
      } else {
        this.bugRowData = row;
        var hostid = this.hostEnum.filter(item => item.ip === row.host);
        this.bugEditForm.host_id = hostid.length > 0 ? hostid[0].id : "";
        this.bugEditForm.name = row.name;
        this.bugEditForm.level = row.level;
        setTimeout(() => {
          this.$set(
            this.bugEditForm,
            "quote",
            row.quote === null ? "" : row.quote
          );
          this.$set(
            this.bugEditForm,
            "description",
            row.describe === null ? "" : row.describe
          );
          this.detailLoading = false;
        }, 500);
      }
    },
    // 漏洞 确认添加/编辑
    sureAddBug() {
      var form = "bugEditForm";
      var content = this.$refs.bugdescirbeedit.release();
      var content1 = this.$refs.bugquoteedit.release();
      this.$refs[form].validate(valid => {
        if (valid) {
          var data = {
            id: this.bugType === "add" ? undefined : this.bugRowData.id,
            name: this.bugEditForm.name,
            description: content,
            quote: content1,
            level: this.bugEditForm.level, //风险等级 1-低 2是中 3是高
            host_id: this.bugEditForm.host_id
          };
          this.loadSureAdd = true;
          addBug(data)
            .then(response => {
              this.loadSureAdd = false;
              if (response.data.success) {
                this.bugType === "add"
                  ? this.$message.success("创建成功")
                  : this.$message.success("编辑成功");
                this.bugEditDrawer = false;
                this.checkFifth();
              } else {
                this.$message.warning(response.data.info);
              }
            })
            .catch(error => {
              this.loadSureAdd = false;
              this.bugEditDrawer = false;
              this.$message.error(error.message);
            });
        } else {
          this.$message.error("请完善各项内容");
          return false;
        }
      });
    },
    // 删除、凭证、主机漏洞
    delThisData(row, type){
      this.selectRowType = type
      this.delThisRow = row
      this.delProofVisible = true
    },
    // 确认删除
    sureDelProof(){
      this.loadSureProofDel = true;
      let data = {
        id: this.delThisRow.id
      }
      if(this.selectRowType === 0){ // 确认删除漏洞
        delBug(data)
          .then(response => {
            this.loadSureProofDel = false;
            if (response.data.success) {
              this.delProofVisible = false;
              this.$message.success("删除成功");
              this.checkFifth();
            } else {
              this.$message.warning(response.data.info);
            }
          })
          .catch(error => {
            this.loadSureProofDel = false;
            this.delProofVisible = false;
            this.$message.error(error.message);
          });
      }else if(this.selectRowType === 1){ // 确认删除凭证
        delProof(data)
          .then(response => {
            this.loadSureProofDel = false;
            if (response.data.success) {
              this.delProofVisible = false;
              this.$message.success("删除成功");
              this.checkSixth();
            } else {
              this.$message.warning(response.data.info);
            }
          })
          .catch(error => {
            this.loadSureProofDel = false;
            this.delProofVisible = false;
            this.$message.error(error.message);
          });
      }else if(this.selectRowType === 2){ // 确认删除主机
        optHost(data, 'delete')
          .then(response => {
            this.loadSureProofDel = false;
            if (response.data.success) {
              this.delProofVisible = false;
              this.$message.success("删除成功");
              this.checkSeventh();
            } else {
              this.$message.warning(response.data.info);
            }
          })
          .catch(error => {
            this.loadSureProofDel = false;
            this.delProofVisible = false;
            this.$message.error(error.message);
          });
      }
      else if(this.selectRowType === 3){ // 确认删除端口
        portOperation(data, 'delete')
          .then(response => {
            this.loadSureProofDel = false;
            if (response.data.success) {
              this.delProofVisible = false;
              this.$message.success("删除成功");
              this.chenckPortDetail(this.portOptId);
            } else {
              this.$message.warning(response.data.info);
            }
          })
          .catch(error => {
            this.loadSureProofDel = false;
            this.delProofVisible = false;
            this.$message.error(error.message);
          });
      }
    },
    // 主机列表选项
    getHostList() {
      var sendD = {
        id: this.taskId,
        search: "",
        page: 1,
        pageSize: 99999
      };
      taskMasters(sendD)
        .then(response => {
          if (response.data.success) {
            this.hostEnum = response.data.data;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    // 主机凭证获取
    checkSixth() {
      this.detailGetLoading = true;
      var sendD = {
        id: this.taskId,
        search: this.detailSearch,
        page: this.detailPage,
        pageSize: this.detailSize,
        host_search: this.hostChoose
      };
      taskRoles(sendD)
        .then(response => {
          this.detailGetLoading = false;
          if (response.data.success) {
            this.taskRolesArr = response.data.data;
            this.detailTotalSize = response.data.total;
            this.IPEnum = response.data.host_ips
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.detailGetLoading = false;
          this.$message.error(error.message);
        });
    },
    // 添加&编辑凭证
    addProof(row, type){
      this.proofType = type
      this.addProofVisible = true;
      if(type === 'add'){
        this.formReset('proofAddForm')
        this.proofAddForm = {
          name: "",
          host_id: "",
          username: "",
          password: ""
        }
      }else{
        this.proofRowData = row;
        let host = this.IPEnum.filter(item => item.ip === row.ip)
        this.proofAddForm = {
          name: row.name,
          host_id: host.length > 0 ? host[0].id : "",
          username: row.username,
          password: row.password
        }
      }
    },
    // 凭证确认创建
    sureAddProof() {
      this.$refs["proofAddForm"].validate(valid => {
        if (valid) {
          let data = {
              id: this.proofType === 'add'?undefined:this.proofRowData.id,
              name: this.proofAddForm.name,
              username: this.proofAddForm.username,
              password: this.proofAddForm.password,
              host_id: this.proofAddForm.host_id,
            };
          this.loadSureAdd = true;
          addProof(data)
            .then(response => {
              this.loadSureAdd = false;
              if (response.data.success) {
                this.addProofVisible = false;
                this.$message.success(response.data.info)
                this.checkSixth();
              } else {
                this.$message.warning(response.data.info);
              }
            })
            .catch(error => {
              this.loadSureAdd = false;
              this.addProofVisible = false;
              this.$message.error(error.message);
            });
        } else {
          this.$message.error("请完善各项内容");
          return false;
        }
      });
    },
    // 主机列表获取
    checkSeventh() {
      var sendD = {
        id: this.taskId,
        search: this.detailSearch,
        page: this.detailPage,
        pageSize: this.detailSize
      };
      taskMasters(sendD)
        .then(response => {
          this.detailGetLoading = false;
          if (response.data.success) {
            this.taskMastersArr = response.data.data;
            this.detailTotalSize = response.data.total;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.detailGetLoading = false;
          this.$message.error(error.message);
        });
    },
    // 新增&编辑主机
    addHost(row, type){
      this.hostType = type
      this.addHostVisible = true;
      if(type === 'add'){
        this.formReset('hostAddForm')
        this.hostAddForm = {
          name: "",
          ip: "",
          os_info: "",
          ports: ""
        }
      }else{
        this.hostRowData = row;
        this.hostAddForm = {
          name: row.name,
          ip: row.ip,
          os_info: row.os_info,
        }
      }
    },
    // 主机确认创建&修改
    sureAddHost() {
      this.$refs["hostAddForm"].validate(valid => {
        if (valid) {
          var data = {
            id: this.hostType === 'add'?undefined:this.hostRowData.id,
            task_id: this.taskId,
            name: this.hostAddForm.name,
            ip: this.hostAddForm.ip,
            os_info: this.hostAddForm.os_info,
          };
          this.loadSureAdd = true;
          optHost(data, this.hostType === 'add'?'post':'put')
            .then(response => {
              this.loadSureAdd = false;
              if (response.data.success) {
                this.addHostVisible = false;
                this.$message.success(response.data.info);
                this.checkSeventh();
              } else {
                this.$message.warning(response.data.info);
              }
            })
            .catch(error => {
              this.loadSureAdd = false;
              this.addHostVisible = false;
              this.$message.error(error.message);
            });
        } else {
          this.$message.error("请完善各项内容");
          return false;
        }
      });
    },
    // 端口信息列表查看
    chenckPortDetail(row) {
      this.portOptId = row
      this.portInfoIs = false;
      let send = {
        host_id: row.id,
        search: this.port_search,
        page_size: this.post_page_size,
        page: this.port_page
      }
      portDetail(send)
        .then(response => {
          this.detailGetLoading = false;
          if (response.data.success) {
            this.sinHostPortArr = response.data.data;
            this.portTotalSize = response.data.total;
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.detailGetLoading = false;
          this.$message.error(error.message);
        });
    },
    portSizeChange(val){
      this.post_page_size = val
      this.chenckPortDetail(this.portOptId)
    },
    portCurrentChange(val){
      this.port_page = val
      this.chenckPortDetail(this.portOptId)
    },
    enterPortCheck(val){
      this.port_page = 1;
      this.post_page_size = 10;
      this.chenckPortDetail(this.portOptId)
    },
    checkPortSearch(){
      this.port_page = 1;
        this.chenckPortDetail(this.portOptId)
    },
    // 新增&编辑 端口
    addPort(row, type){
      this.portType = type
      this.addPortVisible = true;
      if(type === 'add'){
        this.formReset('portAddForm')
        this.portAddForm = {
          port_name: "",
          port: ""
        }
      }else{
        this.portRowData = row;
        this.portAddForm = {
          port_name: row.name,
          port: row.port
        }
      }
    },
    // 端口确认创建&修改
    sureAddPort() {
      this.$refs["portAddForm"].validate(valid => {
        if (valid) {
          if(this.portAddForm.port === ''&&this.portAddForm.port_name === ''){
            this.$message.warning('端口名称与端口号至少一个不为空！');
            return false
          }
          var data = {
            id: this.portType === 'add'?undefined:this.portRowData.id,
            host_id: this.portType === 'add'?this.portOptId.id:undefined,
            name: this.portAddForm.port_name,
            port: this.portAddForm.port
          };
          this.loadSureAdd = true;
          portOperation(data, this.portType === 'add'?'post':'put')
            .then(response => {
              this.loadSureAdd = false;
              if (response.data.success) {
                this.addPortVisible = false;
                this.$message.success(response.data.info);
                this.chenckPortDetail(this.portOptId);
              } else {
                this.$message.warning(response.data.info);
              }
            })
            .catch(error => {
              this.loadSureAdd = false;
              this.addPortVisible = false;
              this.$message.error(error.message);
            });
        } else {
          this.$message.error("请完善各项内容");
          return false;
        }
      });
    },
    // 详情切换
    handleClick() {
      this.detailPage = 1;
      this.detailSize = 10;
      this.detailSearch = "";
      this.pageSizeArr = [10, 25, 50, 100];
      this.hostChoose = "";
      this.notesListShow = true;
      this.mindListShow = true;
      this.portInfoIs = true;
      if (this.activeName === "third") {
        this.detailSize = 9;
        this.pageSizeArr = [9, 18, 54, 99];
      }
      this.changeView();
    },
    changeView() {
      if (this.activeName !== "third") {
        this.detailGetLoading = true;
        this.noteState = false;
      }
      if (this.activeName !== "fourth") {
        this.fileState = false;
      }
      if (this.activeName !== "eighth") {
        this.mindState = false;
      }
      switch (this.activeName) {
        case "first":
          this.checkFirst();
          this.detailNoData = true;
          break;
        case "second":
          this.detailNoData = true;
          this.checkSecond();
          break;
        case "third":
          this.noteState = true;
          this.detailNoData = true;
          if (this.detailSearch != "") {
            this.$refs.noteSon.noteSearch(this.detailSearch, this.noteChoose)
          }
          break;
        case "fourth":
          this.fileState = true;
          this.detailGetLoading = false;
          if (this.detailSearch != "") {
            this.fileSearch(this.detailSearch, '')
          }
          break;
        case "fifth":
          this.checkFifth();
          break;
        case "sixth":
          this.getHostList();
          this.checkSixth();
          break;
        case "seventh":
          this.checkSeventh();
          break;
        case "eighth":
          this.mindState = true;
          this.detailGetLoading = false;
          this.detailNoData = true;
          this.$refs.mindmap.getData(this.detailSearch);
      }
    },
    // 详情抽屉关键词搜索
    enterDetailCheck(val) {
      if (val == "") {
        this.detailPage = 1;
        this.detailSize = 10;
        if (this.activeName === "second") {
          this.detailSize = 9;
        } 
        this.changeView();
      }
    },
    checkDetailResult() {
      if (this.detailSearch != "") {
        this.detailPage = 1;
        this.changeView();
      }
    },
    // 分页
    detailSizeChange(val) {
      this.detailSize = val;
      if(this.activeName === "fourth"){
        this.filePageState =  true
        this.fileTreeLoadNode(this.node, this.resolve)
      }else{
        this.changeView();
      }
    },
    detailCurrentChange(val) {
      this.detailPage = val;
      if(this.activeName === "fourth"){
        this.filePageState =  true
        this.fileTreeLoadNode(this.node, this.resolve)
      }else{
        this.changeView();
      }
    },
    // // 附件下载
    // downLoadFile() {
    //   const a = document.createElement("a");
    //   a.href = this.$ctx + "/vulner/download?id=" + this.leakDetailCon.id;
    //   a.download = this.leakDetailCon.fileName;
    //   document.querySelector("body").appendChild(a);
    //   a.click();
    //   document.querySelector("body").removeChild(a);
    // },
    // 删除任务
    delSinLeak(row) {
      this.leakId = row.task_id;
      this.delCon = row.title;
      this.delVisible = true;
    },
    sureDelLink() {
      this.loadSureDel = true;
      let sendD = {
        task_id: this.leakId
      };
      taskDel(sendD)
        .then(response => {
          this.loadSureDel = false;
          this.delVisible = false;
          if (response.data.success) {
            if (this.proListData.length === 1) {
              this.page = 1;
            }
            this.getAllLeakList();
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
    // ---------全局搜索------------
    enterAllCheck(val) {
      if (val == "") {
        this.all_page = 1;
        this.all_page_size = 10;
        this.allSearchList();
      }
    },
    clickAllCheck() {
      if (this.searchInfo != "") {
        this.all_page = 1;
        this.allSearchList();
      }
    },
    allSearchSelect(val){
      if(this.oldInfoType !== val){
        this.all_page = 1
        this.allSearchList()
      }
      this.oldInfoType = val
    },
    allSizeChange(val){
      this.all_page_size = val
      this.allSearchList()
    },
    allCurrentChange(val){
      this.all_page = val
      this.allSearchList()
    },
    allSearchList(){
      if (this.searchInfo == "") {
        this.$message.warning('请输入搜索关键字');
        return false
      }
      this.allSearchLoad = true
      let sendD = {
        keyword: this.searchInfo,
        search_flag: this.infoType,
        page: this.all_page,
        max_count: this.all_page_size
      }
      allSearch(sendD)
        .then(response => {
          this.allSearchLoad = false;
          if (response.data.success) {
            let d = response.data.data
            for(let i=0;i<d.length;i++){
              if(this.infoType === 'host'){
                d[i].host_name = this.brightenKeyword(d[i].host_name, this.searchInfo)
                d[i].host_ip = this.brightenKeyword(d[i].host_ip, this.searchInfo)
              } else if(this.infoType === 'file'){
                d[i].file_name = this.brightenKeyword(d[i].file_name, this.searchInfo)
              } else{
                d[i].note_name = this.brightenKeyword(d[i].note_name, this.searchInfo)
                d[i].note_contetn = this.brightenKeyword(d[i].note_contetn, this.searchInfo)
              }
            }
            this.infoData = d
            this.allTotalSize = response.data.total
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.allSearchLoad = false;
          this.$message.error(error.message);
        });
    },
    goinDetail(row, type){
      if(type === 'note'){
        this.$store.commit("getTaskId", row.task_id);
        this.taskId = row.task_id;
        this.activeName = "third";
        this.taskDetailDrawer = true;
        this.noteState = true;
        this.detailNoData = true;
        this.detailSearch = this.searchInfo;
        this.noteChoose = row.is_name_content; 
        this.$nextTick(() => {
          this.$refs.noteSon.noteSearch(this.detailSearch, this.noteChoose);
        });
      }else if(type === 'file'){
        this.$store.commit("getTaskId", row.task_id);
        this.taskId = row.task_id;
        this.activeName = "fourth";
        this.taskDetailDrawer = true;
        this.fileState = true;
        this.detailGetLoading = false;
        this.detailSearch = this.searchInfo;
        this.$nextTick(() => {
          this.fileSearch(this.detailSearch, '');
        });
      }else if(type === 'host'){
        this.$store.commit("getTaskId", row.task_id);
        this.taskId = row.task_id;
        this.activeName = "seventh";
        this.taskDetailDrawer = true;
        this.detailSearch = this.searchInfo;
        this.checkSeventh()
      }else{
        this.$router.push({
          path:'/main/knowledge',
          query:{
            allSearch: this.searchInfo,      //跳转时需要携带的参数
            taskId: row.task_id,
            taskName: row.task_name
          }
        })
      }
    }
  }
};
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.taskView {
  height: 100%;
  padding: 30px 30px 20px;
  background: #fff;
  position: relative;
  border-radius: 20px;
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
    height: calc(100% - 60px);
    .proTable {
      height: calc(100% - 68px);
      .taskTime {
        .time {
          color: #999999;
          background: #f2f3f7;
          padding: 8px 10px;
        }
        .divider {
          color: #999999;
          margin: 0 8px;
        }
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
  .sinTaskDe {
    .content {
      max-height: 500px;
      .box-card {
        .clearfix {
          span {
            font-size: 20px;
            font-weight: 600;
            line-height: 40px;
          }
          .checkTimeLine {
            float: right;
          }
        }
        .item {
          p {
            margin-bottom: 10px;
          }
          .titleSty {
            font-weight: bold;
          }
        }
      }
    }
  }
  .dnoteDetail{
    height: 100%;
    .portList{
      width: 70%;
      height: 100%;
      .postTitle{
        font-size: 18px;
        padding: 10px 0;
        margin: 10px 0;
        position: relative;
        .icon-fanhui1{
          color: #5861f0;
          font-size: 18px;
          margin-right: 10px;
        }
        span{
          margin: 10px 5px;
        }
        .addPort{
          height:36px;
          padding:8px 20px;
          margin-bottom:10px;
          background-image: linear-gradient(to right, #5861f0, #3b44db);
          border-color:#5861f0;
          position: absolute;
          left: calc(80% - 127px);
          top: 2px;
        }
        .portInput{
          z-index: 5;
          width: 20%;
          position: absolute;
          left: 80%;
          top: 0px;
        }
      }
    }
  }
}
</style>
<style rel="stylesheet/scss" lang="scss">
.taskView {
  .mainList {
    .el-table {
      overflow: auto;
      &:before {
        height: 0;
      }
    }
  }
  .portList{
    //分页样式
    .pagePortStyle{
      background: #fff;
      padding: 20px;
      overflow: hidden;
      .el-pagination{
        float: right;
        padding:0;
        .el-pagination__total{
          float: left;
        }
        .el-pagination__sizes{
          margin:0 0 0 24px;
          float: right;
          .el-select{
            .el-input{
              margin:0;
            }
          }
        }
        .el-pager{
          .number{
            margin:0 5px;
            border: 1px solid #D9D9D9;
            border-radius: 3px;
          }
          .number.active,.number:hover{
            color:#fff;
            background: #5861f0;
            border: 1px solid #5861f0;
          }
        }
      }
    }
  }
}
</style>
