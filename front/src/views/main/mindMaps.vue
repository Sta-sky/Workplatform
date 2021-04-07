<template>
  <div style="height:100%;width:100%">
    <div class="fileTableBox" style="height: 100%">
      <div class="task_filter" v-loading="listloading">
        <span class="title" style="color:#eff2f6">根目录</span>
        <div class="pull_right">
          <el-button size="small" class="addDirectory" @click="addMap" round
            >新建导图 <i class="el-icon-circle-plus-outline"></i>
          </el-button>
          <el-button
            size="small"
            style="box-shadow:2px 2px 9px #8187e8"
            class="lookAtLog"
            @click="
              {
                mindLogVisible = true;
              }
            "
            round
            >查看日志 <i class="el-icon-circle-plus-outline"></i>
          </el-button>
        </div>
      </div>
      <div
        style="height:100%;"
        v-loading="mapsLoading"
        element-loading-text="数据加载中"
      >
        <div class="list_box scrollStyle" v-if="mapNoData">
          <div
            class="sinNote"
            v-for="(item, i) in mapList"
            :key="i"
            @click="showMapDetile(item)"
          >
            <p class="title">
              <img src="@/assets/img/siweidaotu.png" alt="" />
              <el-tooltip
                class="item"
                effect="dark"
                :content="item.title"
                placement="top"
              >
                <span class="name">{{ item.title | beautySub(8) }}</span>
              </el-tooltip>
            </p>
            <p class="graph" :title="item.description">
              {{ item.description }}
            </p>
            <div class="btm">
              <!-- <el-tooltip
              class="item"
              effect="dark"
              v-if="item.parentLabel"
              :content="item.parentLabel"
              placement="top"
            >
              <div class="tag_one" v-if="item.parentLabel">
                {{ item.parentLabel | beautySub(3) }}
              </div>
            </el-tooltip> -->
              <div class="tag_two">
                {{ item.user }}
              </div>
              <el-tooltip
                class="item"
                effect="dark"
                :content="item.create_time"
                placement="top"
              >
                <div class="tag_three">
                  {{ item.create_time }}
                </div>
                <!-- <div class="tag_three">{{ item.create_time | beautySub(4) }}</div> -->
              </el-tooltip>
            </div>
          </div>
        </div>
      </div>
      <div class="detailNoDataIs" style="top: 39.5%;" v-if="!mapNoData">
        <img src="@/assets/img/noData.png" alt="" />
        <p>暂无数据</p>
      </div>
      <!-- <div class="pageStyle" v-if="mapNoData">
        <el-pagination
          class="pageShowView"
          @size-change="detailSizeChange"
          @current-change="detailCurrentChange"
          :current-page="page"
          :page-sizes="[10, 25, 50, 100]"
          :page-size="pagesize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
        >
        </el-pagination>
      </div> -->
    </div>
    <!-- 思維導圖詳情 -->
    <el-drawer
      :visible.sync="editMapDrawer"
      size="100%"
      class="addTaskModal mindmapdialog"
      :append-to-body="true"
      :withHeader="false"
    >
      <div
        style="height:100%;"
        v-loading="detailLoading"
        element-loading-text="数据加载中"
        element-loading-background="rgba(0, 0, 0, 0.6)"
      >
        <div class="addTaskBox">
          <div class="addModalTop" style="background:none;padding: 30px 70px;">
            <i
              class="iconfont icon-fanhui1"
              @click="editMapDrawer = false"
              style="color:#c8c9cc;font-size:18px"
            ></i>
            <el-breadcrumb
              separator="/"
              style="line-height:13px;display: inline-block; padding-left: 10px; font-size: 18px;"
            >
              <el-breadcrumb-item>{{ curMapData.title }}</el-breadcrumb-item>
            </el-breadcrumb>
            <div class="pull_right">
              <el-popover placement="right" width="200" trigger="click">
                <el-table
                  :data="editList"
                  style="height:500px"
                  class="scrollStyle"
                >
                  <el-table-column
                    width="50"
                    type="index"
                    label="序号"
                  ></el-table-column>
                  <el-table-column
                    show-overflow-tooltip
                    width="100"
                    property="username"
                    label="姓名"
                  ></el-table-column>
                </el-table>
                <el-button
                  size="small"
                  class="addDirectory"
                  slot="reference"
                  round
                  >在线编辑人数（{{ editList.length }} ）<i
                    class="el-icon-tickets"
                  ></i>
                </el-button>
              </el-popover>
              <el-button
                size="small"
                class="addDirectory"
                @click="extractNote"
                round
                >提取笔记 <i class="el-icon-circle-plus-outline"></i>
              </el-button>
              <el-button
                size="small"
                class="lookAtLog"
                @click="
                  {
                    mindLogVisible = true;
                  }
                "
                style="box-shadow:2px 2px 9px #8187e8"
                round
                >查看日志 <i class="el-icon-circle-plus-outline"></i>
              </el-button>
              <el-button
                size="small"
                style="box-shadow:2px 2px 9px #60d879"
                class="addNote"
                @click="delMap"
                round
                >删除导图 <i class="el-icon-delete"></i>
              </el-button>
            </div>
          </div>
          <div
            style="height:calc(100% - 80px);width:100%;padding:20px;position:relative"
            class="scrollStyle modalMain"
          >
            <div class="newSearch scrollStyle">
              <el-input
                class="searchBoxPos srh"
                placeholder="请输入搜索内容"
                clearable
                @input="nodeDetailCheck"
                @keypress.enter.native="nodeDetailResult"
                v-model="detailSrh"
              >
                <el-button
                  slot="append"
                  icon="el-icon-search"
                  @click="nodeDetailResult"
                ></el-button>
              </el-input>
              <span v-show="showTips"
                >共搜索到{{ "  " + srhData.total + "  " }}条相关内容</span
              >
              <div class="contents">
                <div
                  class="sinNote"
                  v-for="(item, i) in srhData.list"
                  :key="i"
                  @click="showNodeDetile(item)"
                >
                  <p class="title">
                    <el-tooltip
                      class="item"
                      effect="dark"
                      :content="item.type === 'node' ? item.content : item.node"
                      placement="top"
                    >
                      <span class="name">{{
                        item.type === "node" ? item.content : item.node
                      }}</span>
                    </el-tooltip>
                  </p>
                  <p class="type">
                    {{
                      item.type === "port"
                        ? "端口"
                        : item.type === "note"
                        ? "笔记"
                        : item.type === "node"
                        ? "节点"
                        : "目录"
                    }}
                  </p>
                  <p class="graph" :title="item.content">{{ item.content }}</p>
                </div>
              </div>
            </div>
            <el-row style="height:100%;width:100%">
              <el-col
                :span="24"
                class="mapCol"
                v-loading="mapEditLoading"
                element-loading-text="编辑状态查询中"
                element-loading-background="#afafaf29"
              >
                <mindmap
                  class="mindMapVal"
                  ref="mindView"
                  @showDetial="nodeDetail"
                  @delnode="nodeDel"
                  @click="nodeClick"
                  @nodeedited="addLock"
                  @contextMenu="nodeContextMenu"
                  @updateNodeName="updataNodeName"
                  @dragEnd="dragEnd"
                  :draggable="true"
                  :xSpacing="60"
                  :editable="editable"
                  :ySpacing="30"
                  :showUndo="false"
                  :showNodeAdd="false"
                  :strokeWidth="2"
                  v-model="mapdata"
                ></mindmap
              ></el-col>
            </el-row>
          </div>
        </div>
        <div @click="editMapDrawer = false" class="closeBtn">
          <i class="el-icon-arrow-right"></i>
        </div>
      </div>
      <el-drawer size="35%" :append-to-body="true" :visible.sync="innerDrawer">
        <div class="nodeDetail scrollStyle">
          <div class="ondoBtn">
            <el-switch
              v-model="nodeDetialData.is_work"
              @change="workStateChg"
              active-color="#f65160"
              :width="50"
              :active-text="nodeDetialData.is_work ? '待工作' : '标记为待工作'"
            ></el-switch>
          </div>
          <div class="title">
            <span :title="nodeDetialData.name">{{ nodeDetialData.name }}</span>
            <el-button class="addDirectory" @click="informationVisible = true"
              >信息收集<i class="el-icon-right"></i
            ></el-button>
          </div>
          <div class="os">
            <span class="system">{{
              nodeDetialData.os ? nodeDetialData.os : "未知"
            }}</span>
            <span class="systemtype">{{
              nodeDetialData.ascription ? nodeDetialData.ascription : "未知"
            }}</span>
          </div>
          <div class="ports">
            <span>端口</span>
            <div class="postslist">
              <div class="portsUl">
                <div
                  class="portli"
                  v-for="(item, index) in nodeDetialData.port"
                  :key="index"
                >
                  <div class="port">{{ item.port }}</div>
                  <div class="portname">{{ item.name }}</div>
                </div>
                <div
                  class="portli moreport"
                  v-if="nodeDetialData.port"
                  @click="showPort()"
                >
                  <div class="port">MORE</div>
                  <div class="portname">...</div>
                </div>
                <div
                  class="portli moreport"
                  style="width:20%;margin-left:40%"
                  v-else
                  @click="showPort()"
                >
                  <div class="port">暂无数据</div>
                  <div class="portname">...</div>
                </div>
              </div>
            </div>
          </div>
          <div class="strs">
            <span>目录</span>
            <div class="strsslist">
              <ul class="strsUl">
                <li
                  v-for="(item, index) in nodeDetialData.dir"
                  :title="item"
                  :key="index"
                >
                  {{ item }}
                </li>
                <li style="overflow:unset;" v-if="nodeDetialData.dir">
                  <el-button class="morestr" @click="showFile()"
                    >MORE...</el-button
                  >
                </li>
                <li style="overflow:unset; width:20%;margin-left:40%" v-else>
                  <el-button class="morestr" @click="showFile()"
                    >暂无数据...</el-button
                  >
                </li>
              </ul>
            </div>
          </div>
          <div class="files scrollStyle">
            <span>脚本</span>
            <el-select
              class="select"
              multiple
              ref="fileSelect"
              v-model="checkFile"
            >
              <el-option
                v-for="(item, index) in fileList"
                :key="index"
                :label="item.name"
                :value="item.id"
              ></el-option>
              <el-button
                class="addDirectory"
                :loading="loadEdit"
                round
                style="position:absolute;bottom:5px;right:20px"
                @click="commitFile"
                >保存</el-button
              >
            </el-select>
          </div>
          <div class="note">
            <div style="width:100%;height:50px">
              <span>笔记</span>
              <el-button :loading="loadEdit" class="btn" round @click="saveNote"
                >保存笔记</el-button
              >
            </div>
            <div class="nodeContent scrollStyle">
              <el-input
                type="textarea"
                class="text"
                :autosize="{ minRows: 10, maxRows: 114 }"
                v-model="nodeDetialData.note"
              ></el-input>
            </div>
          </div>
        </div>
      </el-drawer>
    </el-drawer>
    <!-- 端口详情 -->
    <el-drawer
      :visible.sync="portDrawer"
      class="addTaskModal"
      :append-to-body="true"
      size="80%"
      :withHeader="false"
      :close-on-press-escape="false"
    >
      <div
        style="height:100%;"
        v-loading="portLoading"
        element-loading-text="数据加载中"
        element-loading-background="rgba(0, 0, 0, 0.6)"
      >
        <div class="addTaskBox">
          <div class="addModalTop">
            <span class="englishView">端口详情</span>
            <img src="@/assets/img/port_detail.png" alt="" />
          </div>
          <el-button
            size="small"
            class="addDirectory"
            style="position: absolute;"
            @click="addPortDialog = true"
            round
            >新增端口 <i class="el-icon-circle-plus-outline"></i>
          </el-button>
          <el-select
            class="searchBoxPos"
            style="right:2%"
            placeholder="请选择筛选主机IP"
            @change="showPort()"
            @clear="hostId = ''"
            clearable
            v-model="hostId"
          >
            <el-option
              v-for="(item, index) in hostLists"
              :key="index"
              :label="item.ip"
              :value="item.id"
            ></el-option>
          </el-select>
          <div
            class=""
            v-if="!detailNoData"
            style="height:calc(100% - 170px);width:100%;padding:20px"
          >
            <el-table
              :data="portLists"
              fit
              border
              style="height:calc(100% - 60px)"
              class="scrollStyle"
            >
              <el-table-column label="名称" property="name"></el-table-column>
              <el-table-column
                show-overflow-tooltip
                property="port"
                label="端口"
              ></el-table-column>
              <el-table-column
                show-overflow-tooltip
                property="ip"
                label="IP"
              ></el-table-column>
              <el-table-column label="操作" width="150px">
                <template slot-scope="scope"
                  ><el-button type="danger" @click="delPort(scope.row)" round
                    >删除</el-button
                  >
                </template>
              </el-table-column>
            </el-table>
            <div class="pageStyle">
              <el-pagination
                class="pageShowView"
                @size-change="detailSizeChange"
                @current-change="detailCurrentChange"
                :current-page="page"
                :page-sizes="[10, 25, 50, 100]"
                :page-size="pagesize"
                layout="total, sizes, prev, pager, next, jumper"
                :total="total"
              >
              </el-pagination>
            </div>
          </div>
          <div class="detailNoDataIs" v-if="detailNoData">
            <img src="@/assets/img/noData.png" alt="" />
            <p>暂无数据</p>
          </div>
          <div @click="portDrawer = false" class="closeBtn">
            <i class="el-icon-arrow-right"></i>
          </div>
        </div>
      </div>
    </el-drawer>
    <!-- 目录详情 -->
    <el-drawer
      :visible.sync="fileDrawer"
      class="addTaskModal"
      :append-to-body="true"
      size="80%"
      :withHeader="false"
      :close-on-press-escape="false"
    >
      <div
        style="height:100%;"
        v-loading="portLoading"
        element-loading-text="数据加载中"
        element-loading-background="rgba(0, 0, 0, 0.6)"
      >
        <div class="addTaskBox">
          <div class="addModalTop">
            <span class="englishView">目录详情</span>
            <img src="@/assets/img/file_detail.png" alt="" />
          </div>
          <el-button
            size="small"
            class="addDirectory"
            style="position: absolute;"
            @click="addFileDialog = true"
            round
            >新增目录<i class="el-icon-circle-plus-outline"></i>
          </el-button>
          <el-button
            size="small"
            class="addDirectory"
            style="position:absolute;right:400px"
            @click="importFileShow"
            round
            >导入目录文件<i class="el-icon-document"></i>
          </el-button>
          <el-input
            class="searchBoxPos"
            style="right:2%"
            placeholder="请输入搜索内容"
            @input="enterDetailCheck"
            @keypress.enter.native="checkDetailResult"
            v-model="search"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="checkDetailResult"
            ></el-button>
          </el-input>
          <div
            class=""
            v-if="!detailNoData"
            style="height:calc(100% - 170px);width:100%;padding:20px"
          >
            <el-table
              :data="reportList"
              fit
              border
              style="height:calc(100% - 60px)"
              class="scrollStyle"
            >
              <el-table-column
                label="目录"
                property="content"
              ></el-table-column>
              <el-table-column label="操作" width="150px">
                <template slot-scope="scope"
                  ><el-button type="danger" @click="delPort(scope.row)" round
                    >删除</el-button
                  >
                </template>
              </el-table-column>
            </el-table>
            <div class="pageStyle">
              <el-pagination
                class="pageShowView"
                @size-change="detailSizeChange"
                @current-change="detailCurrentChange"
                :current-page="page"
                :page-sizes="[10, 25, 50, 100]"
                :page-size="pagesize"
                layout="total, sizes, prev, pager, next, jumper"
                :total="total"
              >
              </el-pagination>
            </div>
          </div>
          <div class="detailNoDataIs" v-if="detailNoData">
            <img src="@/assets/img/noData.png" alt="" />
            <p>暂无数据</p>
          </div>
          <div @click="fileDrawer = false" class="closeBtn">
            <i class="el-icon-arrow-right"></i>
          </div>
        </div>
      </div>
    </el-drawer>
    <!-- 新增端口 -->
    <el-dialog
      :visible.sync="addPortDialog"
      class="addDialog"
      :append-to-body="true"
      :close-on-click-modal="true"
      :close-on-press-escape="true"
      width="30%"
      top="15%"
    >
      <div class="addMain">
        <div class="addTopbar" style="height:30px;text-align:center">
          <span class="englishView" style="float:unset">新增端口</span>
        </div>
        <el-form
          :model="portForm"
          status-icon
          :rules="rules1"
          ref="forms1"
          label-width="100px"
          class="weaponForm"
        >
          <el-form-item
            label="端口IP"
            prop="ip"
            style="width:100%"
            class="fifty"
          >
            <el-select
              class="searchBoxPos"
              placeholder="请选择或输入筛选主机IP"
              clearable
              filterable
              allow-create
              default-first-option
              v-model="portForm.ip"
            >
              <el-option
                v-for="(item, index) in hostLists"
                :key="index"
                :label="item.ip"
                :value="item.ip"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item
            label="端口名称"
            prop="portname"
            style="width:100%"
            class="fifty"
          >
            <el-input
              maxlength="18"
              v-model="portForm.portname"
              clearable
              placeholder="请输入端口名称"
            >
            </el-input>
          </el-form-item>
          <el-form-item label="开放端口" prop="outport">
            <el-input
              placeholder="请输入开放端口"
              v-model.number="portForm.outport"
            ></el-input>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer">
        <el-button
          @click="addPort"
          class="btnSure"
          type="warning"
          :loading="loadFileSureAdd"
          >确 定</el-button
        >
        <el-button type="info" class="btnCancle" @click="addPortDialog = false"
          >取 消</el-button
        >
      </div>
    </el-dialog>
    <!-- 导入目录文件 -->
    <el-dialog
      :visible.sync="loadFileDialog"
      class="addDialog"
      :append-to-body="true"
      :close-on-click-modal="true"
      :close-on-press-escape="true"
      width="30%"
      top="15%"
    >
      <div class="addMain">
        <div class="addTopbar" style="height:30px;text-align:center">
          <span class="englishView" style="float:unset">导入目录文件</span>
        </div>
        <el-form
          :model="fileLoadForm"
          status-icon
          :rules="rules1"
          ref="forms2"
          label-width="100px"
          class="weaponForm"
        >
          <el-form-item
            label="选择文件"
            prop="file"
            style="width:100%"
            class="fifty"
          >
            <el-input
              readonly
              v-model="fileLoadForm.fileName"
              placeholder="请选择文件"
            >
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
        </el-form>
      </div>
      <div slot="footer">
        <el-button
          @click="sureAddFile"
          class="btnSure"
          type="warning"
          :loading="loadFileSureAdd"
          >确 定</el-button
        >
        <el-button type="info" class="btnCancle" @click="loadFileDialog = false"
          >取 消</el-button
        >
      </div>
    </el-dialog>
    <!-- 新增目录 -->
    <el-dialog
      :visible.sync="addFileDialog"
      class="addDialog"
      :append-to-body="true"
      :close-on-click-modal="true"
      :close-on-press-escape="true"
      width="30%"
      top="15%"
    >
      <div class="addMain">
        <div class="addTopbar" style="height:30px;text-align:center">
          <span class="englishView" style="float:unset">新增目录</span>
        </div>
        <el-form
          :model="fileForm"
          status-icon
          :rules="rules1"
          ref="forms2"
          label-width="100px"
          class="weaponForm"
        >
          <el-form-item
            label="开放目录"
            prop="file"
            style="width:100%"
            class="fifty"
          >
            <el-input
              v-model="fileForm.file"
              clearable
              placeholder="请输入开放目录"
            >
            </el-input>
          </el-form-item>
        </el-form>
      </div>
      <div slot="footer">
        <el-button
          @click="addFile"
          class="btnSure"
          type="warning"
          :loading="loadFileSureAdd"
          >确 定</el-button
        >
        <el-button type="info" class="btnCancle" @click="addFileDialog = false"
          >取 消</el-button
        >
      </div>
    </el-dialog>
    <!-- 创建思维导图 -->
    <el-dialog
      :visible.sync="addMapDialog"
      class="addDialog"
      :append-to-body="true"
      :close-on-click-modal="true"
      :close-on-press-escape="true"
      width="50%"
      top="6%"
    >
      <div class="addMain">
        <div class="addTopbar">
          <span class="englishView">创建思维导图</span>
          <img src="@/assets/img/new_mindmap.png" alt="" />
        </div>
        <el-form
          :model="ruleForm"
          status-icon
          :rules="rules1"
          ref="forms"
          label-width="100px"
          class="weaponForm"
        >
          <el-form-item label="名称" prop="name" class="fifty">
            <el-input
              maxlength="20"
              v-model="ruleForm.name"
              placeholder="请输入思维导图名称"
            >
            </el-input>
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input
              placeholder="请输入思维导图描述"
              type="textarea"
              maxlength="399"
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
          >确认创建</el-button
        >
      </div>
    </el-dialog>
    <!--删除确认模态框-->
    <el-dialog
      :visible.sync="delVisible"
      width="30%"
      :append-to-body="true"
      :close-on-click-modal="true"
      :close-on-press-escape="true"
      top="15%"
    >
      <div class="contentPsty">
        确认移除
        <p
          :title="delCon"
          style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding:20px 0;text-align:center;font-weight:600;font-size:18px;color:#f66;"
        >
          {{ delCon }}？
        </p>
      </div>
      <div slot="footer">
        <el-button
          @click="sureDelMind"
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
    <!-- +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ -->
    <!-- 思维导图日志 -->
    <el-drawer
      :visible.sync="mindLogVisible"
      size="80%"
      class="addTaskModal mindLog"
      :withHeader="false"
      :append-to-body="true"
    >
      <div class="addTaskBox">
        <div class="addModalTop" style="padding: 40px 70px 20px;">
          <span class="englishView">操作日志</span>
          <img src="@/assets/img/operation_log.png" alt="" />
        </div>
        <el-row
          :gutter="50"
          class="scrollStyle"
          v-if="mindLogVisible"
          v-infinite-scroll="logPageload"
          :infinite-scroll-disabled="logDisabled"
          style="margin:0;height:calc(100% - 78px);padding-top:50px;"
        >
          <el-col
            :span="16"
            style="height:100%;"
            v-if="mindLogDetail.length !== 0"
          >
            <div class="rmMiddle" style="padding-left:0;">
              <el-steps
                direction="vertical"
                :space="70"
                :active="mindLogDetail.length"
              >
                <el-step v-for="(sLine, index) in mindLogDetail" :key="index">
                  <template slot="title">
                    <div class="step_box">
                      <p class="cont">
                        <span class="setpSty"></span>
                        {{ sLine.user }}:{{
                          sLine.action === 1
                            ? "新增"
                            : sLine.action === 2
                            ? "修改"
                            : "删除"
                        }}“{{ sLine.mind_name }}”
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
      <div @click="mindLogVisible = false" class="closeBtn">
        <i class="el-icon-arrow-right"></i>
      </div>
    </el-drawer>
    <!-- 思维导图-信息收集框 -->
    <el-drawer
      :visible.sync="informationVisible"
      size="80%"
      class="addTaskModal"
      :withHeader="false"
      :append-to-body="true"
    >
      <div
        style="height:100%;"
        v-loading="informationLoad"
        element-loading-text="数据加载中"
        element-loading-background="rgba(0, 0, 0, 0.6)"
      >
        <div class="addTaskBox">
          <div class="informationTop">
            <el-input
              placeholder="请输入内容"
              v-model="searchInfo"
              class="inputInfo"
              @input="enterCheck"
              @keypress.enter.native="clickCheck"
            >
              <el-select
                v-model="infoType"
                class="selectBefore"
                slot="prepend"
                placeholder="请选择"
              >
                <el-option label="SHODAN" value="shodan"></el-option>
                <el-option label="ZOOMEYE" value="zoomeye"></el-option>
                <el-option label="WHOIS" value="whois"></el-option>
              </el-select>
              <el-select
                v-model="infoFlag"
                class="selectAfter"
                slot="prepend"
                placeholder="请选择"
                @change="infoFlagChange"
              >
                <el-option label="IP" :value="1"></el-option>
                <el-option label="域名" :value="2"></el-option>
                <el-option label="网段" :value="3"></el-option>
              </el-select>
            </el-input>
          </div>
          <el-row
            :gutter="50"
            style="margin:0;transform: scale(1);height:calc(100% - 78px);background: #f2f3f7;"
          >
            <!-- 格式一 -->
            <el-col
              :span="24"
              class="listDetail scrollStyle"
              v-if="
                (infoData !== null && infoType === 'zoomeye') ||
                  (infoType === 'shodan' && infoFlag === 2 && searchInfo !== '')
              "
              style="height:100%;padding: 30px 40px;"
            >
              <div
                class="infoBox"
                v-for="(item, index) in infoData"
                :key="index"
              >
                <el-col :span="8" class="detailLeft">
                  <div class="title">
                    <i class="iconfont icon-yuming"></i>
                    {{ item.ip }}
                  </div>
                  <div class="label" v-if="item.portinfo">
                    <span
                      >{{ item.portinfo.port }}/{{
                        item.portinfo.service
                      }}</span
                    >
                  </div>
                  <div class="info">{{ item.country }}</div>
                  <div class="info">{{ item.timestamp }}</div>
                </el-col>
                <el-col :span="16" class="detailRight">
                  <div class="cont scrollStyle">
                    {{ item.info }}
                  </div>
                </el-col>
              </div>
              <div class="pageStyle">
                <el-pagination
                  class="pageShowView"
                  @current-change="infoCurrentChange"
                  :current-page="infoPage"
                  :page-size="infoSize"
                  layout="total, prev, pager, next, jumper"
                  :total="infoTotalSize"
                >
                </el-pagination>
              </div>
            </el-col>
            <!-- 格式二 -->
            <el-col
              :span="24"
              class="listDetail scrollStyle"
              v-if="
                infoData !== null &&
                  infoType === 'shodan' &&
                  infoFlag === 1 &&
                  searchInfo !== ''
              "
              style="height:100%;padding: 30px 40px;background: #fff;"
            >
              <el-col :span="12" class="listLeft">
                <div class="title" v-if="infoData">
                  <i class="iconfont icon-yuming"></i>
                  {{ infoData.ip }}
                </div>
                <ul class="detail_box" v-if="infoData">
                  <li>
                    <p class="name">Country</p>
                    <p class="value">{{ infoData.country_name }}</p>
                  </li>
                  <li>
                    <p class="name">Organization</p>
                    <p class="value" style="word-break:break-word;">
                      {{ infoData.org }}
                    </p>
                  </li>
                  <li>
                    <p class="name">ISP</p>
                    <p class="value">{{ infoData.country_name }}</p>
                  </li>
                  <li>
                    <p class="name">Last Update</p>
                    <p class="value">{{ infoData.last_update }}</p>
                  </li>
                  <li>
                    <p class="name">ASN</p>
                    <p class="value">{{ infoData.asn_code }}</p>
                  </li>
                </ul>
                <div class="title">
                  <img src="@/assets/img/jishu.png" />
                  Web Technologies
                </div>
                <div class="webCont" v-if="infoData">
                  {{ infoData.web === "" ? "暂无数据" : infoData.web }}
                </div>
                <div class="title">
                  <i class="iconfont icon-quexian"></i>
                  Vulnerabilities
                </div>
                <div
                  class="vulnerCont scrollStyle"
                  v-if="
                    infoData && infoData.vulns.length !== 0 && searchInfo !== ''
                  "
                >
                  <ul v-for="(item, index) in infoData.vulns" :key="index">
                    <li class="name">{{ item.name }}</li>
                    <li class="summary">{{ item.summary }}</li>
                  </ul>
                </div>
              </el-col>
              <el-col :span="12" class="listRight">
                <div class="title">
                  <i class="iconfont icon-duankou"></i>
                  Ports
                </div>
                <ul class="portsCont scrollStyle" v-if="infoData">
                  <li
                    class="portCard"
                    v-for="(item, index) in infoData.ports"
                    :key="index"
                  >
                    {{ item }}
                  </li>
                </ul>
                <div class="title">
                  <i class="iconfont icon-fuwuqi1"></i>
                  Services
                </div>
                <ul class="servicesCont scrollStyle" v-if="infoData">
                  <li
                    class="serviceCard"
                    v-for="(item, index) in infoData.protocol_list"
                    :key="index"
                  >
                    {{ item }}
                  </li>
                </ul>
              </el-col>
            </el-col>
            <!-- 格式三 -->
            <el-col
              :span="24"
              class="listDetail scrollStyle"
              v-if="
                infoData !== null && infoType === 'whois' && searchInfo !== ''
              "
              style="height:100%;padding: 30px 40px;"
            >
              <ul class="listTable" v-if="infoData">
                <li>
                  <p class="name">WHIOIS SERVER</p>
                  <p class="value">{{ infoData.whois_server }}</p>
                </li>
                <li>
                  <p class="name">UPDATED DATE</p>
                  <p class="value" style="word-break:break-word;">
                    {{ infoData.update_time }}
                  </p>
                </li>
                <li>
                  <p class="name">CREATION DATE</p>
                  <p class="value">{{ infoData.create_time }}</p>
                </li>
                <li>
                  <p class="name">REGISTRAR REGISTRATION EXPIRATION DATE</p>
                  <p class="value">{{ infoData.expire_time }}</p>
                </li>
                <li>
                  <p class="name">REGISTRAR</p>
                  <p class="value">{{ infoData.registrar }}</p>
                </li>
                <li>
                  <p class="name">REGISTRAR ABUSE CONTACT EMAIL</p>
                  <p class="value">{{ infoData.email }}</p>
                </li>
                <li>
                  <p class="name">REGISTRAR ABUSE CONTACT PHONE</p>
                  <p class="value">{{ infoData.phone }}</p>
                </li>
                <li>
                  <p class="name">REGISTRANT STATE/PROVINCE</p>
                  <p class="value">{{ infoData.registrant_state }}</p>
                </li>
                <li v-for="(item, index) in infoData.name_server" :key="index">
                  <p class="name">NAME SERVER</p>
                  <p class="value">{{ item }}</p>
                </li>
              </ul>
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
      <div @click="informationVisible = false" class="closeBtn">
        <i class="el-icon-arrow-right"></i>
      </div>
    </el-drawer>
  </div>
</template>
<script>
// 思维导图源码修改  @hellowuxin/mindmap/mindmap.ump.min.js 修改内容有注释《《 2021.01.20 修改 》》
import mindmap from "@chenyanggis/mindmap";
import {
  createMind,
  mapList,
  mapDetail,
  nodeUnlock,
  addNode,
  delNode,
  addfile,
  loadFile,
  portList,
  fileSave,
  nodeSearch,
  noteSave,
  fileList,
  addhostport,
  hostList,
  delFile,
  nodeWorkChg,
  fileslist,
  delSingleNode,
  nodedetail,
  delport,
  disconnect,
  nodeLock,
  nodeLockState,
  nodeExtract,
  modifyNode,
  mindLog,
  infoDetail,
  singlemindLog
} from "@/api/mindmap";
export default {
  name: "mindMaps",
  props: {
    taskId: Number
  },
  data() {
    return {
      addMapDialog: false, // 创建思维导图
      delVisible: false,
      portDrawer: false,
      fileDrawer: false,
      portLoading: false,
      detailNoData: false,
      addPortDialog: false,
      addFileDialog: false,
      loadFileDialog: false,
      getChangeMsg: false, // 提交后是否得到socket消息 没有就手动请求更新数据
      hostId: "",
      delCon: "",
      delId: "",
      loadEdit: false,
      loadSureDel: false,
      loadFileSureAdd: false,
      mindmapsocket: null,
      onlinesocket: null,
      mapdata: [],
      hostLists: [],
      reportList: [],
      mapdataConst: "",
      editNode: null,
      curMapData: {},
      editable: false,
      mapNoData: true,
      mapList: [],
      portLists: [], // 端口列表
      checkFile: "",
      fileList: [
        // 思维导图脚本列表
      ],
      nodeDetialData: {},
      ruleForm: {
        name: "",
        description: ""
      },
      portForm: {
        portname: "",
        outport: null,
        ip: ""
      },
      fileForm: {
        file: "",
        fileName: "",
        rowfile: ""
      },
      fileLoadForm: {
        fileName: "",
        file: null
      },
      rules1: {
        file: [{ required: true, message: "请输入开放目录", trigger: "blur" }],
        name: [
          { required: true, message: "请输入思维导图名称", trigger: "blur" }
        ],
        ip: [
          { required: true, message: "请选择或输入筛选主机IP", trigger: "blur" }
        ],
        // portname: [
        //   { required: true, message: "请输入端口名称", trigger: "blur" }
        // ],
        outport: [
          // { required: false, message: "请输入开放端口", trigger: "blur" },
          // { required: false, type: "number", message: "开放端口必须为数字值" }
        ]
      },
      editList: [
        // 在线编辑人数列表
      ],
      page: 1,
      pagesize: 10,
      total: 0,
      search: "",
      detailSrh: "",
      showTips: false,
      srhData: { total: 0, list: [] },
      listloading: false,
      mapsLoading: false,
      innerDrawer: false,
      editMapDrawer: false,
      detailLoading: false,
      mapEditLoading: false,
      // ----------------------------------
      // 日志
      mindLogVisible: false,
      mindLogDetail: [],
      logPage: 0,
      logPageSize: 20,
      logDisabled: false,
      // 信息收集搜索
      informationVisible: false,
      informationLoad: false,
      infoType: "whois",
      infoFlag: 2,
      searchInfo: "", //49.234.104.166 baidu.com 49.234.104.166
      infoPage: 1,
      infoSize: 20,
      infoTotalSize: 0,
      infoData: null
    };
  },
  components: {
    mindmap
  },
  mounted() {},
  created() {
    this.getData("");
    // this.initSocket()
  },
  watch: {
    mindLogVisible(a) {
      if (!a) {
        this.logDisabled = false;
        this.mindLogDetail = [];
        this.logPage = 0;
      }
    },
    editMapDrawer(newval, oldval) {
      if (!newval && oldval) {
        this.unLock();
        this.mindmapsocket.close();
        this.onlinesocket.close();
        // 断开协同在线
        this.disOnline();
      }
    },
    innerDrawer(newval, oldval) {
      if (!newval && oldval) {
        this.unLock();
      }
    }
  },
  methods: {
    // --------链接websocket------

    initSocket(url, val) {
      // val = 0 : 导图更新 val = 1 : 在线人数更新
      let scoket = new WebSocket(this.$websocketattr + url);
      //心跳检测
      var heartCheck = {
        timeout: 60000, //60ms
        timeoutObj: null,
        end: function() {
          clearTimeout(this.timeoutObj);
        },
        reset: function() {
          clearTimeout(this.timeoutObj);
          this.start();
        },
        start: function() {
          this.timeoutObj = setTimeout(function() {
            scoket.send(0);
          }, 6000);
        }
      };
      // eslint-disable-next-line
      scoket.onmessage = e => {
        this.getChangeMsg = true;
        if (val === 0) {
          this.refreshMap(e);
        } else {
          this.refreshOnline(e);
        }
        heartCheck.reset();
      };
      scoket.onopen = () => {
        heartCheck.start();
      };
      scoket.onclose = () => {
        console.log("断开链接");
        heartCheck.end();
      };
      if (val === 0) {
        this.mindmapsocket = scoket;
      } else {
        this.onlinesocket = scoket;
      }
    },
    // wensoceket消息 更新导图
    refreshMap(val) {
      // eslint-disable-next-line
      if (val.data === "1") {
        return;
      } else {
        // console.log("收到导图更新", val);
      }
      var data = JSON.parse(val.data).message.data[0];
      var str = JSON.stringify([data]);
      var c = str.replaceAll("index", "node_index");
      var d = c.replaceAll("id", "id_source");
      var data1 = JSON.parse(d);
      this.mapdata = data1;
      this.mapdataConst = JSON.stringify(data1);
    },
    // wensoceket消息 更新在线人数
    refreshOnline(val) {
      // eslint-disable-next-line
      if(val.data === '1') return
      // console.log("收到在线人数更新", val);
      var data = JSON.parse(val.data);
      this.editList = data.message;
    },
    // --------导图列表---------
    // 获取列表
    getData(val) {
      this.mapNoData = true;
      var data = {
        page: 1,
        page_size: 1000,
        search: val,
        task_id: this.taskId
      };
      this.listloading = true;
      // axios({
      //   method: "get",
      //   url:
      //     "http://192.168.8.236:7300/mock/5ff809bb0ded6600220c9789/LaneGeanPlat/mind/mind_map"
      //   // "http://192.168.8.236:7300/mock/5ff809bb0ded6600220c9789/LaneGeanPlat/mainmap"
      // })
      mapList(data)
        .then(res => {
          this.listloading = false;
          if (res.data.success) {
            this.mapList = res.data.data;
            if (res.data.data.length === 0) {
              this.mapNoData = false;
            }
          } else {
            this.$message.warning(res.data.info);
          }
        })
        .catch(error => {
          this.listloading = false;
          this.$message.error(error);
        });
    },
    // 导图列表日志
    showLogs() {
      var data = {
        page: this.logPage,
        page_size: this.logPageSize,
        mind_id: this.curMapData.id
      };
      singlemindLog(data)
        .then(response => {
          if (response.data.success) {
            if (!this.mindLogVisible) {
              this.mindLogVisible = true;
            }
            let data = response.data.data;
            if (!data) {
              data = [];
            }
            // 上次list的长度
            let len = this.mindLogDetail.length;
            this.mindLogDetail = this.mindLogDetail.concat(data);
            if (data && data.length == 0 && !len) {
              this.$message.warning("没有找到相关数据");
            } else if (data && data.length < 20) {
              if (this.logPage !== 1) {
                this.$message.warning("暂无更多日志");
              }
            } else {
              this.logDisabled = false;
            }
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
      // 单个导图比日志
    },
    // 查看单个导图
    showMapDetile(val) {
      this.detailSrh = "";
      this.srhData.total = 0;
      this.srhData.list = [];
      this.curMapData = val;
      this.detailLoading = true;
      this.mapsLoading = true;
      var urlMind = "/mind/" + val.id + "/",
        urlOnline = "/online/" + val.id + "/";
      this.initSocket(urlMind, 0);
      this.initSocket(urlOnline, 1);
      this.getMapData();
    },
    getMapData() {
      mapDetail({ mind_id: this.curMapData.id })
        .then(res => {
          this.mapsLoading = false;
          this.detailLoading = false;
          if (res.data.success) {
            var str = JSON.stringify(res.data.data);
            var b = str.replaceAll("title", "name");
            var d = b.replaceAll("id", "id_source");
            var e = d.replaceAll("index", "node_index");
            var data = JSON.parse(e);
            this.editList = data.online_list;
            this.mapdata = data.content;
            this.mapdataConst = JSON.stringify(data.content);
            // console.log(this.mapdata, "data");
          } else {
            this.$message.warning(res.data.info);
          }
          this.editMapDrawer = true;
        })
        .catch(error => {
          this.detailLoading = false;
          this.$message.error(error);
        });
    },
    // --------思维导图操作-------
    findEditNode(val, state) {
      // 通过插件回调函数返回的id在思维导图中找正在编辑的节点 val:0-1-2-1-0 state : 1/null
      // 依次找到mapdata[0][1][2][1][0],找到当前节点
      var idxList = val.split("-");
      if (state) {
        if (idxList.length === 1) {
          return val;
        } else {
          idxList.length = idxList.length - 1;
        }
      }
      let data = JSON.parse(this.mapdataConst);
      idxList.forEach((idx, index) => {
        if (index === idxList.length - 1) {
          data = data[idx];
        } else {
          data = data[idx].children;
        }
      });
      return data;
    },
    // 节点删除
    nodeDel() {
      var data = {
        mind_id: this.curMapData.id,
        node_id: this.editNode.id_source
      };
      delNode(data)
        .then(res => {
          if (res.data.success) {
            this.$message.warning("删除节点成功");
            // todo
          } else {
            this.$refs.mindView.undo();
            this.$message.warning(res.data.info);
          }
        })
        .catch(error => {
          this.$refs.mindView.undo();
          this.$message.error(error);
        });
    },
    // 更新节点名称
    updataNodeName(n, val) {
      // var data = this.findEditNode(id);
      var id = val.id_source;
      var parent = val.parent;
      var ind = val.node_index || 0;
      if (n.name.length > 50) {
        this.$message.warning("节点名称过长，请重新输入");
        this.$refs.mindView.undo();
        return;
      }
      if (id) {
        var params = {
          task_id: this.taskId,
          mind_id: this.curMapData.id,
          left: n.left,
          name: n.name,
          index: ind,
          node_id: id
        };
        modifyNode(params)
          .then(res => {
            if (res.data.success) {
              // todo
              this.unLock();
            } else {
              this.$refs.mindView.undo();
              this.$message.warning(res.data.info);
            }
          })
          .catch(error => {
            this.$message.error(error);
            this.$refs.mindView.undo();
          });
      } else {
        // var iddata = this.findEditNode(id, 1);
        this.getChangeMsg = false;
        var param = {
          task_id: this.taskId,
          mind_id: this.curMapData.id,
          left: n.left,
          name: n.name,
          index: ind,
          parent_id: parent
        };
        addNode(param)
          .then(res => {
            if (res.data.success) {
              this.$message.warning("添加节点成功");
              setTimeout(() => {
                if (this.getChangeMsg === false) this.getMapData();
              }, 200);
              // todo
            } else {
              this.$refs.mindView.undo();
              this.$message.warning(res.data.info);
            }
          })
          .catch(error => {
            this.$refs.mindView.undo();
            this.$message.error(error);
          });
      }
    },
    dragEnd(n, ind) {
      var val = {
        id_source: n.id_source,
        parent: n.parentId,
        node_index: ind
      };
      this.updataNodeName(n, val);
    },
    // 右键点击事件
    nodeContextMenu(n, id, praent) {
      // eidtable 控制节点是否可以编辑 掉接口后给它赋值即可
      // this.mapEditLoading = true;
      this.editable = false;
      // var len = id.split("-");
      // var tempdata = null;
      // if (len.length > 1 && n.name === "") {
      //   // 连续添加两次时的处理
      //   // eslint-disable-next-line
      //   var po = len.pop();
      //   var temp = len.join("-");
      //   tempdata = this.findEditNode(temp);
      //   if (!tempdata) {
      //     this.editable = false;
      //     return;
      //   }
      // }
      // var len = id.split("-");
      // if (len.length > 1 && n.name === "") {
      //   var tempdata = this.findEditNode(id, 1);
      //   if (!tempdata) {
      //     this.editable = false;
      //     return;
      //   }
      // }
      // var data = this.findEditNode(id);
      n.id_source = id;
      n.parent = praent;
      // 如果之前有节点被锁 解锁
      this.unLock(n.name);
      if (praent === "") {
        //   // 连续添加两次
        //     return
      }
      if (id !== "") {
        this.editNode = n;
        nodeLockState({ node_id: id })
          .then(res => {
            if (res.data.success) {
              // 节点正在被编辑
              this.editable = false;
              this.$message.warning("此节点正在被其他用户编辑");
            } else {
              // 没有人正在编辑 给节点上锁
              this.editable = true;
            }
            // 根节点不允许编辑
            // if (len === 1) this.editable = false;
            setTimeout(() => {
              this.mapEditLoading = false;
            }, 50);
          })
          .catch(error => {
            this.mapEditLoading = false;
            this.$message.error(error);
          });
      } else {
        this.mapEditLoading = false;
        this.editable = true;
      }
    },
    // 节点点击 调接口查看是否可以编辑
    nodeClick(n, id) {
      // 点击后先将editable设为false 拒绝任何操作，接口返回后再变换可编辑状态
      this.editable = false;
      // var data = this.findEditNode(id);
      n.id_source = id;
      if (n.name === "") return;
      this.unLock(n.name);
      if (id !== "") {
        this.editNode = n;
        nodeLockState({ node_id: id })
          .then(res => {
            if (res.data.success) {
              // 节点正在被编辑
              this.editable = false;
              this.$message.warning("此节点正在被其他用户编辑");
            } else {
              this.editable = true;
            }
          })
          .catch(error => {
            this.$message.error(error);
          });
      }
    },
    // 节点详情查看
    nodeDetail(n, id) {
      // 点击后先将editable设为false 拒绝任何操作，接口返回后再变换可编辑状态
      this.editable = false;
      // var data = this.findEditNode(id);
      if (n) {
        n.id_source = id;
        // var len = id.split("-");
        if (n.name === "") return;
        this.unLock(n.name);
      }
      if (id) {
        if (n) this.editNode = n;
        nodeLockState({ node_id: id })
          .then(res => {
            if (res.data.success) {
              // 节点正在被编辑
              this.editable = false;
              this.$message.warning("此节点正在被其他用户编辑");
            } else {
              // 没有人正在编辑 给节点上锁
              this.editable = true;
              this.getNodeDetail(id);
              setTimeout(() => {
                this.innerDrawer = true;
              }, 50);
            }
            // 根节点不允许编辑
            // if (len === 1) this.editable = false;
          })
          .catch(error => {
            this.$message.error(error);
          });
        this.addLock();
        // 节点主机数据获取
        hostList({ node_id: this.editNode.id_source })
          .then(res => {
            if (res.data.success) {
              this.hostLists = res.data.data;
            } else {
              this.$message.warning(res.data.info);
            }
          })
          .catch(error => {
            this.$message.error(error);
          });
      }
    },
    // 节点点击查看详情
    getNodeDetail(val) {
      // 获取脚本数据
      fileslist({ task_id: this.taskId })
        .then(res => {
          if (res.data.success) {
            this.fileList = res.data.data;
          } else {
            this.$message.warning(res.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error);
        });
      nodedetail({ node_id: val })
        .then(res => {
          if (res.data.success) {
            res.data.data.dir.length =
              res.data.data.dir.length > 3 ? 3 : res.data.data.dir.length;
            res.data.data.port.length =
              res.data.data.port.length > 11 ? 11 : res.data.data.port.length;
            res.data.data.dir =
              res.data.data.dir.length === 0 ? null : res.data.data.dir;
            res.data.data.port =
              res.data.data.port.length === 0 ? null : res.data.data.port;
            res.data.data.is_work = !res.data.data.is_work;
            this.nodeDetialData = res.data.data;
            this.nodeDetialData = res.data.data;
            var idList = [];
            res.data.data.file.forEach(item => {
              idList.push(item.id);
            });
            this.checkFile = idList;
          } else {
            this.$message.warning(res.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error);
        });
    },
    // 节点脚本编辑
    commitFile() {
      // console.log(this.checkFile, "checkfile");
      var idList = [];
      this.checkFile.forEach(item => {
        if (item.id) {
          idList.push(item.id);
        } else {
          idList.push(item);
        }
      });
      this.$refs.fileSelect.blur();
      var data = {
        file_id_list: idList,
        node_id: this.editNode.id_source
      };
      this.loadEdit = true;
      fileSave(data)
        .then(res => {
          this.loadEdit = false;
          if (res.data.success) {
            this.$message.success("编辑成功");
          } else {
            this.$message.warning(res.data.info);
          }
        })
        .catch(error => {
          this.loadEdit = false;
          this.$message.error(error);
        });
    },
    // 保存节点笔记
    saveNote() {
      var data = {
        node_id: this.editNode.id_source,
        note: this.nodeDetialData.note
      };
      this.loadEdit = true;
      noteSave(data)
        .then(res => {
          this.loadEdit = false;
          if (res.data.success) {
            this.$message.success("保存成功");
          } else {
            this.$message.warning(res.data.info);
          }
        })
        .catch(error => {
          this.loadEdit = false;
          this.$message.error(error);
        });
    },
    // 端口详情
    showPort(val) {
      this.portDrawer = true;
      this.fileDrawer = false;
      var data = {
        page: this.page,
        page_size: this.pagesize,
        host_id: this.hostId,
        node_id: val || this.editNode.id_source
      };
      this.portLoading = true;
      portList(data)
        .then(res => {
          this.portLoading = false;
          if (res.data.success) {
            this.portLists = res.data.data;
            this.total = res.data.count;
            if (res.data.count === 0) {
              this.detailNoData = true;
            } else {
              this.detailNoData = false;
            }
            // todo
          }
        })
        .catch(error => {
          this.$message.error(error);
        });
    },
    // 目录列表
    showFile(val) {
      this.fileDrawer = true;
      this.portDrawer = false;
      var data = {
        page: this.page,
        page_size: this.pagesize,
        search: this.search,
        node_id: val || this.editNode.id_source
      };
      this.portLoading = true;
      fileList(data)
        .then(res => {
          this.portLoading = false;
          if (res.data.success) {
            this.reportList = res.data.data;
            this.total = res.data.total;
            if (res.data.total === 0) {
              this.detailNoData = true;
            } else {
              this.detailNoData = false;
            }
            // todo
          }
        })
        .catch(error => {
          this.$message.error(error);
        });
    },
    // 节点加锁
    addLock() {
      var data = {
        node_id: this.editNode.id_source
      };
      nodeLock(data)
        .then(res => {
          if (res.data.success) {
            // todo
          }
        })
        .catch(error => {
          this.$message.error(error);
        });
    },
    // 节点解锁
    unLock(val) {
      if (this.editNode === null || (val && val === this.editNode.name)) {
        return;
      }
      this.socket = [];
      var data = {
        node_id: this.editNode.id_source
      };
      nodeUnlock(data)
        .then(res => {
          if (res.data.success) {
            // todo
          } else {
            // this.$message.warning(res.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error);
        });
    },
    // 显示文件上传表单
    importFileShow() {
      this.loadFileDialog = true;
      this.fileLoadForm.fileName = "";
      this.fileLoadForm.file = null;
    },
    // 文件上传 切换文件
    changeFile(file) {
      var isJPGCon = file.name.split(".");
      isJPGCon = isJPGCon[isJPGCon.length - 1];
      var st = ["txt", "TXT"];
      if (st.indexOf(isJPGCon) < 0) {
        this.$message.error("所选文件不是  txt/TXT  格式");
      } else if (file.size > 31457280) {
        this.$message.error("所选文件大小大于 30MB ，请重新选择");
      } else {
        this.fileLoadForm.fileName = file.name;
        this.fileLoadForm.file = file.raw;
      }
    },
    // 文件确认上传
    sureAddFile() {
      if (this.fileLoadForm.fileName === "") {
        this.$message.error("请选择要导入的文件");
        return false;
      }
      this.loadFileSureAdd = true;
      const data = new FormData();
      data.append("file", this.fileLoadForm.file);
      data.append("node_id", this.editNode.id_source);
      loadFile(data)
        .then(response => {
          this.loadFileSureAdd = false;
          this.loadFileDialog = false;
          if (response.data.success) {
            this.$message.success("文件上传成功");
            this.showFile();
            this.getNodeDetail(this.editNode.id_source);
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.loadFileSureAdd = false;
          this.loadFileDialog = false;
          this.$message.error(error.message);
        });
    },
    // 断开协同在线
    disOnline() {
      var data = {
        mind_id: this.curMapData.id
      };
      disconnect(data)
        .then(res => {
          if (res.data.success) {
            //todo
          } else {
            this.$message.warning(res.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error);
        });
    },
    // 提取笔记
    extractNote() {
      var data = {
        task_id: this.taskId,
        mind_id: this.curMapData.id
      };
      nodeExtract(data)
        .then(res => {
          if (res.data.success) {
            // todo
            this.$message.success("提取成功！");
          } else {
            this.$message.warning(res.data.detail);
          }
        })
        .catch(error => {
          this.$message.error(error);
        });
    },
    // 新建导图
    addMap() {
      this.addMapDialog = true;
      this.ruleForm.name = "";
      this.ruleForm.description = "";
    },
    // 确认创建
    addSubmit() {
      this.$refs["forms"].validate(valid => {
        if (valid) {
          this.loadFileSureAdd = true;
          var data = {
            task_id: this.taskId,
            title: this.ruleForm.name,
            description: this.ruleForm.description
          };
          createMind(data)
            .then(res => {
              this.loadFileSureAdd = false;
              this.addMapDialog = false;
              if (res.data.success) {
                // todo
                this.$message.success("创建成功");
                this.getData("");
              } else {
                this.$message.warning(res.data.info);
              }
            })
            .catch(error => {
              this.loadFileSureAdd = false;
              this.addMapDialog = false;
              this.$message.error(error);
            });
        } else {
          this.$message.warning("请输入思维导图名称");
          return;
        }
      });
    },
    // 新增端口
    addPort() {
      this.$refs["forms1"].validate(valid => {
        if (valid) {
          if (this.portForm.outport === "" && this.portForm.portname === "") {
            this.$message.warning("请输入开放端口或端口名称");
            return;
          } else if (
            this.portForm.outport &&
            typeof this.portForm.outport != "number"
          ) {
            this.$message.warning("开放端口必须为数字");
            return;
          }

          if (this.portForm.outport * 1 > 65535) {
            this.$message.warning("请输入正确端口号");
            return;
          }
          this.loadFileSureAdd = true;
          var data = {
            task_id: this.taskId,
            node_id: this.editNode.id_source,
            ip: this.portForm.ip,
            port: this.portForm.outport,
            port_name: this.portForm.portname
          };
          addhostport(data)
            .then(res => {
              this.loadFileSureAdd = false;
              this.addPortDialog = false;
              if (res.data.success) {
                // todo
                this.$message.success("创建成功");
                this.hostId = "";
                this.showPort();
                this.getNodeDetail(this.editNode.id_source);
              } else {
                this.$message.warning(res.data.info);
              }
            })
            .catch(error => {
              this.loadFileSureAdd = false;
              this.addPortDialog = false;
              this.$message.error(error);
            });
        } else {
          this.$message.warning("验证错误，请重新输入");
          return;
        }
      });
    },
    // 新增目录
    addFile() {
      this.$refs["forms2"].validate(valid => {
        if (valid) {
          this.loadFileSureAdd = true;
          var data = {
            node_id: this.editNode.id_source,
            content: this.fileForm.file
          };
          addfile(data)
            .then(res => {
              this.loadFileSureAdd = false;
              this.addFileDialog = false;
              if (res.data.success) {
                // todo
                this.$message.success("创建成功");
                this.hostId = "";
                this.showFile();
                this.getNodeDetail(this.editNode.id_source);
              } else {
                this.$message.warning(res.data.info);
              }
            })
            .catch(error => {
              this.loadFileSureAdd = false;
              this.addFileDialog = false;
              this.$message.error(error);
            });
        } else {
          this.$message.warning("请输入开放目录");
          return;
        }
      });
    },
    // 删除导图
    delMap() {
      this.delVisible = true;
      this.delCon = this.curMapData.title;
    },
    // 删除端口
    delPort(val) {
      this.delId = val.id;
      this.delCon = val.name || val.content;
      this.delVisible = true;
    },
    // 确认删除
    sureDelMind() {
      var data = { mind_id: this.curMapData.id };
      this.loadSureDel = true;
      if (this.portDrawer) {
        // 删除端口
        delport({ port_id: this.delId })
          .then(res => {
            this.loadSureDel = false;
            if (res.data.success) {
              this.delVisible = false;
              this.$message.success("删除成功");
              this.showPort();
              this.getNodeDetail(this.editNode.id_source);
              // todo
            } else {
              this.$message.warning(res.data.info);
            }
            this.delVisible = false;
          })
          .catch(error => {
            this.loadSureDel = false;
            this.$message.error(error);
          });
      } else if (this.fileDrawer) {
        // 删除目录
        delFile({ ids: this.delId })
          .then(res => {
            this.loadSureDel = false;
            if (res.data.success) {
              this.delVisible = false;
              this.$message.success("删除成功");
              this.showFile();
              this.getNodeDetail(this.editNode.id_source);
              // todo
            } else {
              this.$message.warning(res.data.info);
            }
            this.delVisible = false;
          })
          .catch(error => {
            this.loadSureDel = false;
            this.$message.error(error);
          });
      } else {
        // 删除思维导图
        delSingleNode(data)
          .then(res => {
            this.loadSureDel = false;
            if (res.data.success) {
              // todo
              this.getData("");
              this.editMapDrawer = false;
              this.$message.success("删除成功");
            } else {
              this.$message.warning(res.data.info);
            }
            this.delVisible = false;
          })
          .catch(error => {
            this.loadSureDel = false;
            this.$message.error(error);
          });
      }
    },
    // 节点工作状态改变
    workStateChg(val) {
      var data = {
        is_work: !val,
        node_id: this.editNode.id_source
      };
      nodeWorkChg(data)
        .then(response => {
          if (response.data.success) {
            // todo
          } else {
            this.nodeDetialData.is_work = !val;
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.nodeDetialData.is_work = !val;
          this.$message.error(error.message);
        });
    },
    // --------分页-----------
    // 详情抽屉关键词搜索
    enterDetailCheck(val) {
      if (val == "") {
        this.page = 1;
        this.pagesize = 10;
        this.showFile();
      }
    },
    checkDetailResult() {
      if (this.search != "") {
        this.page = 1;
        this.showFile();
      }
    },
    // 思维导图关键词搜索
    nodeDetailCheck(val) {
      if (val == "") {
        this.showTips = false;
        // this.searchNode();
        this.srhData.total = 0;
        this.srhData.list = [];
      }
    },
    nodeDetailResult() {
      if (this.detailSrh != "") {
        this.showTips = true;
        this.searchNode();
      }
    },
    searchNode() {
      var data = {
        mind_id: this.curMapData.id,
        search: this.detailSrh
      };
      nodeSearch(data)
        .then(response => {
          if (response.data.success) {
            this.srhData.total = response.data.data.length;
            this.srhData.list = response.data.data;
          } else {
            this.srhData.total = 0;
            this.srhData.list = [];
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    // 节点搜索点击
    showNodeDetile(val) {
      if (val.type === "node" || val.type === "note") {
        // 节点 查看节点详情
        this.nodeDetail(null, val.id);
      } else if (val.type === "port") {
        // 端口 查看端口详情
        this.host_id = "";
        this.page = 1;
        this.pagesize = 10;
        this.showPort(val.id);
      } else {
        // 目录 查看目录详情
        this.page = 1;
        this.pagesize = 10;
        this.showFile(val.id);
      }
    },
    // 分页
    detailSizeChange(val) {
      this.pagesize = val;
      this.fileDrawer ? this.showFile() : this.showPort();
    },
    detailCurrentChange(val) {
      this.page = val;
      this.fileDrawer ? this.showFile() : this.showPort();
    },
    // -------------------------------------
    // 思维导图查看日志
    mindLogLook() {
      var sendD = {
        task_id: this.taskId,
        page: this.logPage,
        page_size: this.logPageSize
      };
      mindLog(sendD)
        .then(response => {
          if (response.data.success) {
            if (!this.mindLogVisible) {
              this.mindLogVisible = true;
            }
            let data = response.data.data;
            if (!data) {
              data = [];
            }
            // 上次list的长度
            let len = this.mindLogDetail.length;
            this.mindLogDetail = this.mindLogDetail.concat(data);
            if (data && data.length == 0 && !len) {
              this.$message.warning("没有找到相关数据");
            } else if (data && data.length < 20) {
              if (this.logPage !== 1) {
                this.$message.warning("暂无更多日志");
              }
            } else {
              this.logDisabled = false;
            }
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.message);
        });
    },
    logPageload() {
      this.logDisabled = true;
      this.logPage += 1;
      if (!this.editMapDrawer) {
        // 所搜思维导图日志
        this.mindLogLook();
      } else {
        // 单个导图日志
        this.showLogs();
      }
    },
    mindInformation() {
      if (this.searchInfo === "") {
        if (this.infoFlag === 1) {
          this.$message.warning("请输入需要查询的IP地址");
          return false;
        } else if (this.infoFlag === 2) {
          this.$message.warning("请输入需要查询的域名");
          return false;
        } else {
          this.$message.warning("请输入需要查询的域名");
          return false;
        }
      }
      this.informationLoad = true;
      let sendD = {
        site: this.searchInfo, // 目标站点
        flag: this.infoFlag, // 1.ip  2.域名  3.网段
        page: this.infoPage // 页数
      };
      let url = this.infoType;
      infoDetail(sendD, url)
        .then(response => {
          this.informationLoad = false;
          if (response.data.success) {
            if (
              JSON.stringify(response.data.data) !== "{}" ||
              response.data.data === null ||
              response.data.data.length === 0
            ) {
              this.infoData = response.data.data;
              this.infoTotalSize = response.data.total;
            } else {
              this.infoData = null;
              if (this.infoPage === 1) {
                this.$message.warning("暂无数据！");
              } else {
                this.$message.warning("第" + this.infoPage + "页暂无数据！");
              }
            }
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.informationLoad = false;
          this.$message.error(error.message);
        });
    },
    infoCurrentChange(val) {
      this.infoPage = val;
      this.mindInformation();
    },
    // 关键词搜索
    enterCheck(val) {
      if (val == "") {
        this.infoPage = 1;
        this.mindInformation();
      }
    },
    clickCheck() {
      if (this.searchInfo != "") {
        this.infoPage = 1;
        this.mindInformation();
      }
    },
    infoFlagChange() {
      this.infoPage = 1;
      this.searchInfo = "";
    }
  },
  filters: {
    beautySub(str, len) {
      let reg = /[\u4e00-\u9fa5]/g, //专业匹配中文
        slice = str.substring(0, len),
        chineseCharNum = ~~(slice.match(reg) && slice.match(reg).length),
        realen = slice.length * 2 - chineseCharNum;
      return str.substr(0, realen) + (realen < str.length ? "..." : "");
    }
  },
  beforeDestroy() {
    this.mindmapsocket && this.mindmapsocket.close();
    this.onlinesocket && this.onlinesocket.close();
    this.socket = [];
  },
  computed: {}
};
</script>
<style lang="scss" scoped>
.fileTableBox {
  height: 100%;
  padding: 20px 30px !important;
  background: #eff2f6;
  border-radius: 20px;
  .pageStyle {
    display: inline-block;
    width: 100%;
    text-align: right;
    padding-right: 30px;
    .el-pagination {
      float: right;
      padding: 0;
      .el-pagination__total {
        float: left;
      }
      .el-pagination__sizes {
        margin: 0 0 0 24px;
        float: right;
        .el-select {
          .el-input {
            margin: 0;
          }
        }
      }
      .el-pager {
        .number {
          margin: 0 5px;
          border: 1px solid #d9d9d9;
          border-radius: 3px;
        }
        .number.active,
        .number:hover {
          color: #fff;
          background: #409eff;
          border: 1px solid #409eff;
        }
      }
    }
  }
  .list_box {
    height: calc(100% - 60px);
    padding-left: 20px;
    background: #fff;
    border-radius: 20px;
    &::-webkit-scrollbar {
      width: 6px;
    }
    .filesTable {
      border-radius: 20px;
    }
    .sinNote {
      float: left;
      width: 30%;
      height: 200px;
      padding: 20px;
      border-radius: 10px;
      background: #fff;
      margin: 1% 3% 1% 0;
      cursor: pointer;
      -moz-box-shadow: 0px 7px 5px 3px #ebedf0;
      -webkit-box-shadow: 0px 7px 5px 3px #ebedf0;
      box-shadow: 0px 7px 5px 3px #ebedf0;
      transition: all 0.5s;
      &:hover {
        transform: translateY(-10px);
        // transform: scale(1.05, 1.05);
        -moz-box-shadow: 0px 5px 10px 5px #d0e4ff;
        -webkit-box-shadow: 0px 5px 10px 5px #d0e4ff;
        box-shadow: 0px 5px 10px 5px #d0e4ff;
        .title {
          .delMindBtn {
            display: block;
          }
        }
      }
      .title {
        font-weight: bold;
        font-size: 20px;
        color: #2a2c33;
        position: relative;
        .icon-wendang {
          color: #1e89ff;
          font-size: 30px;
        }
        .name {
          width: calc(100% - 40px);
          display: inline-block;
          position: absolute;
          left: 50px;
          top: 10px;
        }
        .delMindBtn {
          display: none;
        }
      }
      .graph {
        height: 70px;
        margin: 10px 0;
        line-height: 24px;
        color: #636469;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
      }
      .btm {
        div {
          float: left;
          margin-right: 5px;
          margin-top: -5px;
          height: 28px;
          line-height: 28px;
          padding: 0 12px;
          border-radius: 28px;
          background: #ffffff;
          border: 1px solid;
          &.tag_one {
            color: #fcda8f;
            border-color: #fcda8f;
          }
          &.tag_two {
            color: #acb0f1;
            border-color: #acb0f1;
          }
          &.tag_three {
            width: 45%;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            color: #00c35c;
            border-color: #00c35c;
          }
        }
      }
    }
  }
  .task_filter {
    margin-bottom: 20px;
    .title {
      font-size: 30px;
    }
    .pull_right {
      float: right;
      color: #fff;
      .addDirectory {
        height: 34px;
        padding: 8px 20px;
        margin-left: 10px;
        background-image: linear-gradient(to right, #5861f0, #3b44db);
        border-color: #5861f0;
        color: #fff;
      }
      .addNote {
        height: 34px;
        padding: 8px 20px;
        margin-left: 10px;
        background-image: linear-gradient(to right, #64db7d, #3fbf59);
        border-color: #64db7d;
        color: #fff;
      }
      .lookAtLog {
        height: 34px;
        padding: 8px 20px;
        margin-left: 10px;
        background-image: linear-gradient(to right, #0e9ef8, #0775eb);
        border-color: #0e9ef8;
        color: #fff;
      }
      .delNote {
        height: 34px;
        padding: 8px 20px;
        margin-left: 10px;
        background-image: linear-gradient(to right, #ff7086, #f65160);
        border-color: #ff7086;
        color: #fff;
      }
    }
  }
}
.nodeDetail {
  height: 100%;
  width: 100%;
  padding: 0px 50px;
  position: relative;
  .ondoBtn {
    height: 50px;
    width: 100%;
    padding-left: 20px;
  }
  .title {
    height: 50px;
    width: 80%;
    display: inline-flex;
    span {
      float: left;
      font-size: 28px;
      font-weight: bold;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .addDirectory {
      position: absolute;
      box-shadow: 0px 5px 7px #787dd8;
      border-radius: 20px;
      right: 50px;
      float: right;
      height: 34px;
      padding: 8px 20px;
      margin-left: 10px;
      background-image: linear-gradient(to right, #5861f0, #3b44db);
      border-color: #5861f0;
      color: #fff;
    }
  }
  .os {
    height: 35px;
    width: 100%;
    display: inline-flex;
    .system,
    .systemtype {
      line-height: 35px;
      color: #fff;
      font-size: 20px;
      background-color: #b8bccc;
      border-radius: 10px;
      padding: 0px 10px;
      margin-right: 20px;
    }
  }
  .ports {
    position: relative;
    height: 20%;
    width: 100%;
    span {
      position: absolute;
      top: 20px;
      left: 5px;
      color: #7a7a7a;
      font-size: 16px;
    }
    .postslist {
      padding-top: 50px;
      height: calc(100% - 20px);
      width: 100%;
      .portsUl {
        .moreport {
          border: 1px solid #3b44db;
          color: rgb(59, 68, 219) !important;
          background-image: initial !important;
          cursor: pointer;
        }
        .portli {
          width: 15%;
          height: 60px;
          display: inline-block;
          padding: 10px;
          margin-right: 1%;
          margin-bottom: 10px;
          box-shadow: 2px 2px 18px #9396d6;
          background-image: -webkit-gradient(
            linear,
            left top,
            right top,
            from(#5861f0),
            to(#3b44db)
          );
          background-image: linear-gradient(to right, #5861f0, #3b44db);
          border-radius: 10px;
          color: #fff;
          &:hover {
            transform: translateY(-5px);
          }
          .port {
            height: 60%;
            width: 100%;
            font-size: 20px;
            float: center;
            text-align: center;
            overflow: hidden;
          }
          .portname {
            height: 30%;
            width: 100%;
            overflow: hidden;
            font-size: 12px;
            text-align: center;
          }
        }
      }
    }
  }
  .strs {
    position: relative;
    height: 20%;
    width: 100%;
    span {
      position: absolute;
      top: 20px;
      left: 5px;
      color: #7a7a7a;
      font-size: 16px;
    }
    .strsslist {
      padding-top: 50px;
      padding-left: 20px;
      .strsUl {
        li {
          font-weight: bold;
          width: 100%;
          height: 20px;
          font-size: 16px;
          margin-bottom: 5px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          .morestr {
            border: 1px solid #4f57e9;
            border-radius: 30px;
            color: #4f57e9;
            margin-top: 15px;
          }
        }
      }
    }
  }
  .files {
    position: relative;
    display: inline-block;
    height: 70px;
    width: 100%;
    .select {
      margin-top: 13px;
      float: right;
      width: 90%;
      .btn {
        position: absolute;
        bottom: 10px;
        right: 20px;
      }
    }
    span {
      position: absolute;
      top: 20px;
      left: 10px;
      color: #7a7a7a;
      font-size: 16px;
    }
    &::-webkit-scrollbar {
      width: 2px;
    }
  }
  .note {
    height: 35%;
    width: 100%;
    position: relative;
    .btn {
      position: absolute;
      right: 20px;
      top: 10px;
      height: 34px;
      background-image: linear-gradient(to right, #5861f0, #3b44db);
      color: #fff;
    }
    span {
      position: absolute;
      top: 20px;
      left: 15px;
      color: #7a7a7a;
      font-size: 16px;
    }
    .nodeContent {
      position: relative;
      margin-left: 30px;
      width: 100%;
      padding: 20px;
      font-size: 18px;
      height: calc(100% - 100px);
      background-color: #f2f3f7;
      border-radius: 20px;
      .text {
        height: 100%;
        overflow: hidden;
        .el-textarea__inner {
          max-height: 100%;
        }
      }
      .addDirectory {
        position: absolute;
        bottom: 10px;
        right: 10px;
      }
      &::-webkit-scrollbar {
        width: 6px;
      }
    }
  }
}
.addTaskModal {
  .addTaskBox {
    height: 100%;
    background: none;
    .addDirectory {
      right: 280px;
      top: 120px;
      height: 34px;
      padding: 8px 20px;
      margin-left: 10px;
      background-image: -webkit-gradient(
        linear,
        left top,
        right top,
        from(#5861f0),
        to(#3b44db)
      );
      background-image: linear-gradient(to right, #5861f0, #3b44db);
      border-color: #5861f0;
      color: #fff;
      box-shadow: 2px 4px 9px #6d73d2;
    }
    .pageStyle {
      display: inline-block;
      width: 100%;
      text-align: right;
      padding-top: 20px;
      padding-right: 30px;
      .el-pagination {
        float: right;
        padding: 0;
        .el-pagination__total {
          float: left;
        }
        .el-pagination__sizes {
          margin: 0 0 0 24px;
          float: right;
          .el-select {
            .el-input {
              margin: 0;
            }
          }
        }
        .el-pager {
          .number {
            margin: 0 5px;
            border: 1px solid #d9d9d9;
            border-radius: 3px;
          }
          .number.active,
          .number:hover {
            color: #fff;
            background: #409eff;
            border: 1px solid #409eff;
          }
        }
      }
    }
    .modalMain {
      .newSearch {
        position: absolute;
        left: 40px;
        top: 50px;
        height: calc(100% - 100px);
        width: 330px;
        padding: 10px;
        .srh {
          width: 100%;
          top: 10px;
          z-index: 10000;
        }
        .contents {
          position: absolute;
          top: 90px;
          width: 100%;
          height: calc(100% - 70px);
          .sinNote {
            position: relative;
            z-index: 10000;
            float: left;
            width: 95%;
            height: 200px;
            padding: 20px;
            border-radius: 10px;
            background: #fff;
            margin: 1% 3% 3.9% 0;
            cursor: pointer;
            -moz-box-shadow: 0px 7px 5px 3px #ebedf0;
            -webkit-box-shadow: 0px 7px 5px 3px #ebedf0;
            box-shadow: 0px 7px 5px 3px #ebedf0;
            transition: all 0.5s;
            &:hover {
              transform: translateY(-10px);
              // transform: scale(1.05, 1.05);
              -moz-box-shadow: 0px 5px 10px 5px #d0e4ff;
              -webkit-box-shadow: 0px 5px 10px 5px #d0e4ff;
              box-shadow: 0px 5px 10px 5px #d0e4ff;
              .title {
                .delMindBtn {
                  display: block;
                }
              }
            }
            .type {
              top: 55px;
              position: absolute;
              color: #b0b0b0;
            }
            .title {
              font-weight: bold;
              font-size: 20px;
              color: #2a2c33;
              position: relative;
              .icon-wendang {
                color: #1e89ff;
                font-size: 30px;
              }
              .name {
                width: calc(100% - 40px);
                display: inline-block;
                position: absolute;
                left: 0px;
                top: 0px;
                font-size: 22px;
                text-overflow: ellipsis;
                overflow: hidden;
                white-space: nowrap;
              }
              .delMindBtn {
                display: none;
              }
            }
            .graph {
              width: 90%;
              position: absolute;
              top: 72px;
              font-weight: bold;
              color: #000;
              height: 100px;
              margin: 10px 0;
              line-height: 24px;
              overflow: hidden;
              text-overflow: ellipsis;
              display: -webkit-box;
              -webkit-line-clamp: 4;
              -webkit-box-orient: vertical;
            }
          }
        }
        span {
          position: absolute;
          top: 58px;
          z-index: 10000;
          left: 26%;
          font-weight: bold;
          font-size: 13px;
        }
        &::-webkit-scrollbar {
          width: 2px;
        }
      }
      .mapCol {
        height: 100%;
        background-color: #eeeef3;
      }
      .infoCol {
        padding: 20px;
      }
    }
    .pull_right {
      float: right;
      color: #fff;
      .addDirectory {
        height: 34px;
        padding: 8px 20px;
        margin-left: 10px;
        background-image: linear-gradient(to right, #5861f0, #3b44db);
        border-color: #5861f0;
        color: #fff;
      }
      .addNote {
        height: 34px;
        padding: 8px 20px;
        margin-left: 10px;
        background-image: linear-gradient(to right, #64db7d, #3fbf59);
        border-color: #64db7d;
        color: #fff;
      }
      .lookAtLog {
        height: 34px;
        padding: 8px 20px;
        margin-left: 10px;
        background-image: linear-gradient(to right, #0e9ef8, #0775eb);
        border-color: #0e9ef8;
        color: #fff;
      }
      .delNote {
        height: 34px;
        padding: 8px 20px;
        margin-left: 10px;
        background-image: linear-gradient(to right, #ff7086, #f65160);
        border-color: #ff7086;
        color: #fff;
      }
    }
  }
}
.mindMapVal {
  height: 100%;
  width: 100%;
}
</style>
<style lang="scss">
.mindmapdialog {
  .el-drawer {
    border-radius: 0;
  }
  .el-popover {
    max-height: 500px;
    &::-webkit-scrollbar {
      width: 5px;
    }
  }
}
.nodeContent {
  .el-textarea__inner {
    max-height: 100%;
  }
}
.addDialog {
  .el-dialog {
    border-radius: 20px;
  }
}
</style>
