<template>
  <div
    class="sysmanage"
    v-loading="listLoading"
    element-loading-text="数据加载中"
    element-loading-background="rgba(0, 0, 0, 0.6)"
  >
    <div class="mainTop">
      <el-row style="margin-bottom: 8px;" :gutter="20">
        <el-col :span="24">
          <span class="englishView">系统管理</span>
          <img src="@/assets/img/system_management.png" alt="" />
        </el-col>
      </el-row>
      <div class="tabs">
        <el-input
          v-show="activetab === 'second'"
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
        <el-button
          v-show="activetab === 'third'"
          title="开始备份"
          class="searchbtn"
          icon="el-icon-folder-opened"
          type="primary"
          @click="beginBackup"
          >开始备份</el-button
        >
        <el-tabs v-model="activetab" @tab-click="handleClick">
          <el-tab-pane label="系统概览" name="first"></el-tab-pane>
          <el-tab-pane
            label="系统日志"
            name="second"
            v-if="$store.getters.roles === 'admin'"
          ></el-tab-pane>
          <el-tab-pane
            label="数据备份"
            name="third"
            v-if="$store.getters.roles === 'admin'"
          ></el-tab-pane>
        </el-tabs>
      </div>
    </div>
    <div class="mainList">
      <div class="firstTab" style="height:100%" v-show="activetab === 'first'">
        <el-row style="height:100%">
          <!-- CPU -->
          <el-col :span="8" class="overviewCols">
            <p class="itemName">CPU</p>
            <p class="itemDetail">{{ system.cpu.detail }}</p>
            <div id="cpu"></div>
            <el-row
              :gutter="40"
              v-for="(item, index) in system.cpu"
              style="margin-top:10px"
              :key="index"
              v-show="index !== 'detail'"
            >
              <el-col
                :span="6"
                style="text-align:right;font-size:16px;color:#2a2c33a3;"
                >{{ index }}</el-col
              >
              <el-col
                :span="18"
                style="text-align:left;font-size:16px;font-family:'strong';"
                >{{ item }}</el-col
              >
            </el-row>
          </el-col>
          <!-- RAM -->
          <el-col :span="8" class="overviewCols">
            <p class="itemName">内存</p>
            <p class="itemDetail">{{ system.ram.detail }}</p>
            <div id="ram"></div>
            <el-row
              :gutter="40"
              v-for="(item, index) in system.ram"
              style="margin-top:10px"
              :key="index"
              v-show="index !== 'detail'"
            >
              <el-col
                :span="6"
                style="text-align:right;font-size:16px;color:#2a2c33a3;"
                >{{ index }}</el-col
              >
              <el-col
                :span="18"
                style="text-align:left;font-size:16px;font-family:'strong';"
                >{{ item }}</el-col
              >
            </el-row>
          </el-col>
          <!-- 磁盘 -->
          <el-col :span="8" class="overviewCols">
            <p class="itemName">磁盘</p>
            <p class="itemDetail">{{ system.disk.detail }}</p>
            <div id="disk"></div>
            <el-row
              :gutter="40"
              v-for="(item, index) in system.disk"
              style="margin-top:10px"
              :key="index"
              v-show="index !== 'detail'"
            >
              <el-col
                :span="6"
                style="text-align:right;font-size:16px;color:#2a2c33a3;"
                >{{ index }}</el-col
              >
              <el-col
                :span="18"
                style="text-align:left;font-size:16px;font-family:'strong';"
                >{{ item }}</el-col
              >
            </el-row>
          </el-col>
        </el-row>
      </div>
      <div
        class="secondTab"
        style="height:100%"
        v-show="activetab === 'second'"
      >
        <el-table
          :data="systemLog"
          v-if="noDataIs"
          border
          class="proTable scrollStyle"
          style="width: 100%;"
        >
          <el-table-column
            prop="content"
            label="操作内容"
            show-overflow-tooltip
          >
          </el-table-column>
          <el-table-column
            prop="operator_id"
            label="操作人"
            show-overflow-tooltip
          >
          </el-table-column>
          <el-table-column
            prop="update_time"
            label="操作时间"
            show-overflow-tooltip
          >
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template slot-scope="scope">
              <el-button
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
      <div class="thirdTab" style="height:100%" v-show="activetab === 'third'">
        <el-table
          :data="systemBackup"
          v-if="noDataIs1"
          border
          class="proTable scrollStyle"
          style="width: 100%;"
        >
          <el-table-column
            prop="status"
            label="备份状态"
            width="250"
            show-overflow-tooltip
          >
            <template slot-scope="scope">
              <el-tag
                :type="
                  scope.row.status === 0
                    ? 'info'
                    : scope.row.status === 1
                    ? 'primary'
                    : 'danger'
                "
                disable-transitions
                >{{
                  scope.row.status === 0
                    ? "备份中"
                    : scope.row.status === 1
                    ? "备份成功"
                    : "备份失败"
                }}</el-tag
              ></template
            >
          </el-table-column>
          <el-table-column prop="create_time" label="操作时间" width="600">
          </el-table-column>
          <el-table-column width="660" label="备份进程" prop="progress">
            <template slot-scope="scope">
              <el-progress
                :stroke-width="10"
                :percentage="scope.row.progress"
                :class="[scope.row.progress === 100 ? 'hundred' : '']"
              ></el-progress>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="300">
            <template slot-scope="scope">
              <el-button
                title="删除"
                :disabled="scope.row.status !== 1"
                class="sinProBtn delBtn"
                @click="delBackup(scope.row)"
              >
                删除
              </el-button>
              <el-button
                title="下载备份"
                type="primary"
                :disabled="scope.row.status !== 1"
                class="sinProBtn"
                @click="downloadBackup(scope.row)"
              >
                下载
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="pageShowStyle" v-if="noDataIs1">
          <el-pagination
            class="pageShowView"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="page1"
            :page-sizes="[10, 25, 50, 100]"
            :page-size="page_size1"
            layout="total, sizes, prev, pager, next, jumper"
            :total="totalSize1"
          >
          </el-pagination>
        </div>
        <div class="noDataIs" v-if="!noDataIs1">
          <img src="@/assets/img/noData.png" alt="" />
          <p>暂无数据</p>
        </div>
      </div>
    </div>
    <!--删除确认模态框-->
    <el-dialog
      :visible.sync="delVisible"
      width="25%"
      top="15%"
      class="delDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <p class="contentPsty">
        是否确认移除此日志?
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
    <!--删除确认备份模态框-->
    <el-dialog
      :visible.sync="delVisible1"
      width="25%"
      top="15%"
      class="delDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <p class="contentPsty">
        是否确认移除此备份?
      </p>
      <div slot="footer">
        <el-button
          @click="sureDelBackup"
          class="btnSure"
          type="warning"
          :loading="loadSureDel1"
          >确 定</el-button
        >
        <el-button type="info" class="btnCancle" @click="delVisible1 = false"
          >放 弃</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>
<script>
import {
  logList,
  logDel,
  systemInformation,
  backupProgress,
  backupChange,
  backupDel,
  // download,
  backupList,
  backupListPost
} from "@/api/system";
export default {
  name: "taskList",
  data() {
    return {
      activetab: "first",
      system: {
        cpu: {},
        ram: {},
        disk: {}
      },
      chartData: {
        id: "cpu",
        name: "CPU",
        progress: 54
      },
      readyBackup: {
        作战任务: 0,
        组织队伍: 0,
        用户管理: 0,
        资源管理: 0
      },
      onBackup: {
        作战任务: 0,
        组织队伍: 0,
        用户管理: 0,
        资源管理: 0
      },
      haveBackup: {
        作战任务: 0,
        组织队伍: 0,
        用户管理: 0,
        资源管理: 0
      },
      backupState: 0,
      listLoading: false,
      systemLog: [],
      systemBackup: [],
      search: "",
      page: 1,
      page1: 1,
      page_size: 10,
      page_size1: 10,
      totalSize: 0,
      totalSize1: 0,
      delVisible: false,
      delVisible1: false,
      loadSureDel: false,
      loadSureDel1: false,
      leakId: [],
      leakId1: [],
      noDataIs: true,
      noDataIs1: true
    };
  },
  mounted() {
    this.getInformation();
  },
  created() {},
  methods: {
    // 获取日志列表
    getLogList() {
      var sendD = {
        search: this.search,
        page: this.page,
        page_size: this.page_size
      };
      this.listLoading = true;
      logList(sendD)
        .then(response => {
          this.listLoading = false;
          if (response.data.success) {
            this.systemLog = response.data.data;
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
        .catch(error => {
          this.listLoading = false;
          this.$message.error(error.message);
        });
    },
    // 开始备份
    beginBackup() {
      backupListPost({})
        .then(response => {
          this.listLoading = false;
          if (response.data.success) {
            this.getBackupList();
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.listLoading = false;
          this.$message.error(error.message);
        });
    },
    // 详情切换
    handleClick() {
      if (this.activetab === "first") {
        this.getInformation();
      } else if (this.activetab === "second") {
        this.search = "";
        this.page = 1;
        this.page_size = 10;
        this.getLogList();
      } else {
        this.page1 = 1;
        this.page_size1 = 10;
        this.getBackupList();
      }
    },
    // 获取备份列表
    getBackupList() {
      var sendD = {
        page: this.page1,
        page_size: this.page_size1
      };
      this.listLoading = true;
      backupList(sendD)
        .then(response => {
          this.listLoading = false;
          if (response.data.success) {
            this.systemBackup = response.data.data;
            this.totalSize1 = response.data.total;
            if (this.totalSize1 == 0) {
              this.noDataIs1 = false;
            } else {
              this.noDataIs1 = true;
            }
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(() => {
          this.listLoading = false;
          // this.$message.error(error.message);
        });
    },
    // 获取硬件信息
    getInformation() {
      this.listLoading = true;
      systemInformation()
        .then(response => {
          this.listLoading = false;
          if (response.data.success) {
            let t = response.data.data;
            this.system.cpu = {
              // detail: t.cpu_usage,
              // 速度: t.cpu_process,
              线程: t.cpu_thread,
              进程: t.cpu_process,
              运行时间: t.cpu_time
            };
            this.system.ram = {
              // detail: t.memory_usage,
              使用: t.memory_used_memory,
              可用: t.memory_free_memory
              // 已提交: response.data.data.RAM.submitted,
              // 速度: response.data.data.RAM.speed
            };
            this.system.disk = {
              // detail: t.disk_percentage,
              读: t.disk_read_velocity,
              写: t.disk_write_velocity
            };
            this.chartData = [
              {
                id: "cpu",
                progress: t.cpu_usage,
                name: "使用率"
              },
              {
                id: "ram",
                progress: t.memory_usage,
                name: "使用率"
              },
              {
                id: "disk",
                progress: t.disk_percentage,
                name: "使用率"
              }
            ];
            this.chartData.forEach(element => {
              this.initChart(element);
            });
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.listLoading = false;
          this.$message.error(error.message);
        });
    },
    // 获取备份进程
    getProgress() {
      this.listLoading = true;
      backupProgress()
        .then(response => {
          this.listLoading = false;
          if (response.data.success) {
            var val = response.data.data.backupstate;
            if (val === 0) {
              // 备份中
              this.backupState = 1;
            } else if (val === 1) {
              // 暂停备份
              this.backupState = 2;
            } else {
              // 完成备份
              this.backupState = 0;
            }
            this.readyBackup = {
              作战任务: response.data.data.beginBackup.mission,
              组织队伍: response.data.data.beginBackup.team,
              用户管理: response.data.data.beginBackup.user,
              资源管理: response.data.data.beginBackup.source
            };
            this.onBackup = {
              作战任务: response.data.data.onBackup.mission,
              组织队伍: response.data.data.onBackup.team,
              用户管理: response.data.data.onBackup.user,
              资源管理: response.data.data.onBackup.source
            };
            this.haveBackup = {
              作战任务: response.data.data.sucessBackup.mission,
              组织队伍: response.data.data.sucessBackup.team,
              用户管理: response.data.data.sucessBackup.user,
              资源管理: response.data.data.sucessBackup.source
            };
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.listLoading = false;
          this.$message.error(error.message);
        });
    },
    // 初始化圆环图
    initChart(val) {
      var id = val.id;
      var name = val.name;
      var data = [100 - val.progress, val.progress];
      let chart = this.$echarts.init(document.getElementById(id));
      let colors = {
        cpu: ["#19ecdb", "#84eee8"],
        ram: ["#f6fa005e", "#f6fa00"],
        disk: ["#3cbf5066", "#3cbf50"]
      };
      let color = colors[id];

      let option = {
        color: color,
        title: [
          {
            text: val.progress + "%",
            top: "45%",
            left: "15%",
            textStyle: {
              color: "#fff",
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
            text: name,
            top: 10,
            left: 10,
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
            center: ["20%", "50%"],
            data: data,
            label: {
              show: false
            },
            hoverAnimation: false
          }
        ]
      };
      chart.setOption(option, true);
      window.addEventListener("resize", function() {
        chart.resize();
      });
    },
    // 备份状态改变 0为开始 1为暂停 2 为继续 3 为完成
    backupStatus(val) {
      var data = { status: val };
      var vuejs = this;
      backupChange(data).then(response => {
        if (response.data.success) {
          if (val === 3) {
            vuejs.backupState = 0;
          } else {
            vuejs.backupState = val + 1;
          }
          // todo
        }
      });
    },
    // 下载备份
    downloadBackup(val) {
      var url =
        "http://127.0.0.1:10000/api/system/backup_down?id=" +
        val.id +
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
    // 关键词搜索
    enterCheck(val) {
      if (val == "") {
        this.page = 1;
        this.page_size = 10;
        this.getLogList();
      }
    },
    clickCheck() {
      if (this.search != "") {
        this.page = 1;
        this.getLogList();
      }
    },
    // 分页
    handleSizeChange(val) {
      if (this.activetab === "second") {
        this.page_size = val;
        this.getLogList();
      } else {
        this.page_size1 = val;
        this.getBackupList();
      }
    },
    handleCurrentChange(val) {
      if (this.activetab === "second") {
        this.page = val;
        this.getLogList();
      } else {
        this.page1 = val;
        this.getBackupList();
      }
    },
    // 附件下载
    downLoadFile() {
      const a = document.createElement("a");
      a.href = this.$ctx + "/vulner/download?id=" + this.leakDetailCon.id;
      a.download = this.leakDetailCon.fileName;
      document.querySelector("body").appendChild(a);
      a.click();
      document.querySelector("body").removeChild(a);
    },
    // 删除任务
    delSinLeak(row) {
      this.leakId = row.id;
      this.delVisible = true;
    },
    delBackup(row) {
      this.delVisible1 = true;
      this.leakId1 = row.id;
    },
    sureDelBackup() {
      this.loadSureDel1 = true;
      backupDel({ id: this.leakId1 })
        .then(response => {
          this.loadSureDel1 = false;
          this.delVisible1 = false;
          if (response.data.success) {
            if (this.systemBackup.length === 1) {
              this.page = 1;
            }
            this.$message.success("删除成功");
            this.getBackupList();
          } else {
            this.$message.warning(response.data.info);
          }
        })
        .catch(error => {
          this.loadSureDel1 = false;
          this.delVisible1 = false;
          this.$message.error(error.message);
        });
    },
    sureDelLink() {
      this.loadSureDel = true;
      logDel({ id: this.leakId })
        .then(response => {
          this.loadSureDel = false;
          this.delVisible = false;
          if (response.data.success) {
            if (this.systemLog.length === 1) {
              this.page = 1;
            }
            this.getLogList();
            this.$message.success("删除成功");
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
  destroyed() {}
};
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.sysmanage {
  height: 100%;
  padding: 30px 30px 20px;
  background: #fff;
  .mainTop {
    position: relative;
    margin-bottom: 10px;
    .tabs {
      .searchinput {
        z-index: 5;
        width: 15%;
        position: absolute;
        right: 20px;
      }
      .searchbtn {
        z-index: 5;
        width: 10%;
        position: absolute;
        right: 20px;
        border: 20px;
        border-radius: 20px;
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
    overflow-x: hidden;
    width: 100%;
    height: calc(100% - 99px);
    .firstTab {
      .overviewCols {
        height: 100%;
        padding: 50px 100px;
        .itemName {
          font-size: 28px;
          font-weight: 600;
          margin-bottom: 15px;
        }
        .itemDetail {
          color: #2a2c33b8;
          font-size: 22px;
          font-weight: 100;
        }
        #cpu,
        #ram,
        #disk {
          height: 40%;
          width: 100%;
          margin: 30px 0 30px 0;
        }
      }
      .overviewCols:nth-child(1) {
        background: url(../../assets/img/cpu_bak.png) no-repeat;
        background-size: 100% 100%;
      }
      .overviewCols:nth-child(2) {
        background: url(../../assets/img/ram_bak.png) no-repeat;
        background-size: 100% 100%;
      }
      .overviewCols:nth-child(3) {
        background: url(../../assets/img/disk_bak.png) no-repeat;
        background-size: 100% 100%;
      }
    }
    .thirdTab {
      .backup {
        padding: 0 20px;
        .download {
          width: 93%;
          padding: 30px 40px;
        }
      }
      .buttons {
        margin: 10px 0 30px 10px;
        .beginBackup {
          background: #4786ff;
          color: #fdf1ed;
          &:hover {
            background: #82abf8;
            color: #f5f0ee;
          }
        }
        .onBackup {
          margin-left: 25px;
          background: #ef6b5d;
          color: #fdf1ed;
          &:hover {
            background: #2fd37c;
            color: #f5f0ee;
          }
        }
        .afterBackup {
          margin-left: 25px;
          background: #2fd37c;
          color: #fdf1ed;
          &:hover {
            background: #ef6b5d;
            color: #f5f0ee;
          }
        }
      }
      .downloadBtn {
        height: 32px;
        text-align: center;
        line-height: 32px;
        border: 0;
        padding: 0;
        border-radius: 32px;
        width: 100%;
        background: #4786ff;
        color: #fdf1ed;
        &:hover {
          background: #82abf8;
          color: #f5f0ee;
        }
      }
      .backupProgress {
        margin: 30px;
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
}
</style>
<style rel="stylesheet/scss" lang="scss">
.sysmanage {
  .mainTop {
    .tabs {
      .el-tabs {
        height: 100%;
        .el-tabs__header {
          .el-tabs__nav {
            margin-left: 20px;
          }
          .el-tabs__active-bar {
            width: 40px !important;
            left: 24px;
            height: 5px;
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
    }
  }
  .mainList {
    .thirdTab {
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
    .firstTab {
      .overviewCols {
        .el-row {
          .el-col {
            line-height: 30px;
          }
        }
      }
    }
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
}
</style>
