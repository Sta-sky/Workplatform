<template>
  <el-col :span="24" class="summary" style="padding: 0;">
    <p class="title">摘要</p>
    <el-col :span="24" style="padding: 5px 25px;" class="summaryCont">
      <el-col :span="14" style="padding: 0;" class="fileLeft">
        <p class="fileName" v-html="fileChange(fileName)"></p>
        <ul class="detail_box" v-if="summaryList">
          <li>
            <p class="name" style="border-right: 0px;background: #fff;">摘要</p>
            <!-- <p class="value" style="text-align: right;">
              <el-link
                class="linkBtn"
                :href="$ctx + '/analysis/DownFile/' + summaryList.file_id"
                >下载</el-link
              >
              <el-button plain size="mini" @click="reboot(summaryList.file_id)"
                >重新提交样本</el-button
              >
            </p> -->
          </li>
          <li>
            <p class="name">文件大小</p>
            <p class="value">{{ summaryList.size | countSize }}</p>
          </li>
          <li>
            <p class="name">类型</p>
            <p class="value" style="word-break:break-word;">
              {{ summaryList.type }}
            </p>
          </li>
          <li>
            <p class="name">MD5</p>
            <p class="value">{{ summaryList.md5 }}</p>
          </li>
          <li>
            <p class="name">SHA1</p>
            <p class="value">{{ summaryList.sha1 }}</p>
          </li>
          <li>
            <p class="name">SHA256</p>
            <p class="value">{{ summaryList.sha256 }}</p>
          </li>
          <li>
            <p class="name">SHA512</p>
            <p class="value">{{ summaryList.sha512 }}</p>
          </li>
          <li>
            <p class="name">CRC32</p>
            <p class="value">{{ summaryList.crc32 }}</p>
          </li>
          <li>
            <p class="name">ssdeep</p>
            <p
              class="value"
              v-text="summaryList.ssdeep === null ? '--' : summaryList.ssdeep"
            ></p>
          </li>
          <li>
            <p class="name">Yara</p>
            <p class="value">{{ summaryList.yard }}</p>
          </li>
        </ul>
      </el-col>
      <el-col :span="10" class="fileRight" style="padding: 0;">
        <p class="fileName">得分</p>
        <div class="scoreBox">{{ fileScore }}分</div>
        <div class="scoreTip">
          <p>该文件显示为良性，得分为{{ fileScore }}分（满分10）。</p>
          <div class="progressLable">
            0分
          </div>
          <div class="progressCont">
            <el-progress
              :percentage="scorePro"
              color="#90c073"
              :stroke-width="8"
              :format="format"
            ></el-progress>
          </div>
          <!-- <div class="mark">
            *注意：记分系统目前仍在开发中，应视为Alpha功能。
          </div>
          <div class="feedback">
            <p class="header">反馈</p>
            <div>
              期待不同的结果？<br />向我们发送次分析，我们将对其进行检查。点击下方进行反馈！
            </div>
            <el-button plain @click="gotoFeedback">反馈</el-button>
          </div> -->
        </div>
      </el-col>
      <!-- <el-col
        :span="24"
        class="actionMsg"
        style="padding: 0;"
      >
        <p class="actionTitle">执行信息(分析)</p>
        <el-table
          :data="actionData"
          style="width: 100%"
          border
          :header-cell-style="{ background: '#f5f8ff', color: '#000000' }"
        >
          <el-table-column prop="category" label="类别"> </el-table-column>
          <el-table-column prop="started" label="开始时间"> </el-table-column>
          <el-table-column prop="ended" label="完成时间"> </el-table-column>
          <el-table-column prop="duration" label="持续时间"> </el-table-column>
          <el-table-column prop="route" label="Routing">
            <template slot-scope="scope">
              {{ scope.row.route }}
            </template>
          </el-table-column>
          <el-table-column label="日志">
            <template>
              <el-link
                :underline="false"
                class="linkBtn"
                @click="summaryLogs(taskid, 1)"
                >显示分析仪日志</el-link
              >
              <el-link
                :underline="false"
                class="linkBtn"
                @click="summaryLogs(taskid, 2)"
                >显示在线杀毒日志</el-link
              >
            </template>
          </el-table-column>
        </el-table>
        <div class="analysisLog" v-if="anaslyLog">
          <p class="an_title"><span>●</span>显示分析仪日志</p>
          <ul class="logBox">
            <li v-for="(item, index) in analysisLoglist" :key="index">
              {{ item }}
            </li>
          </ul>
        </div>
        <div class="analysisLog" v-if="antivirusLog">
          <p class="an_title"><span>●</span>显示在线杀毒日志</p>
          <ul class="logBox">
            <li v-for="(item, index) in antivirusLoglist" :key="index">
              {{ item }}
            </li>
          </ul>
        </div>
      </el-col> -->
      <el-col :span="24" class="signatures" style="padding: 0;">
        <p class="signTitle">签名</p>
        <div class="noSign" v-if="signatureData.length === 0">没有签名</div>
        <!-- <el-table
          class="signCollapse"
          v-if="signatureData.length !== 0"
          :data="signatureData"
          style="width: 100%"
          :row-class-name="tableRowClassName"
          @expand-change="signChange"
          :show-header="false"
        > -->
        <el-table
          class="signCollapse"
          v-if="signatureData.length !== 0"
          :data="signatureData"
          style="width: 100%"
          :row-class-name="tableRowClassName"
          :show-header="false"
        >
          <el-table-column type="expand" prop="children">
            <template slot-scope="props">
              <el-table
                v-if="signatureData.length !== 0 && signType === 'ioc'"
                :data="props.row.children"
                style="width: 100%"
                :show-header="false"
              >
                <!-- <el-table-column label="category">
                  <template slot-scope="scope">
                    <span>{{ scope.row.category }}</span>
                  </template>
                </el-table-column> -->
                <el-table-column prop="ioc" label="ioc"></el-table-column>
                <el-table-column
                  prop="description"
                  label="description"
                ></el-table-column>
              </el-table>
              <el-table
                v-else-if="signatureData.length !== 0 && signType === 'call'"
                :data="props.row.children"
                style="width: 100%"
              >
                <el-table-column label="时间&API">
                  <template slot-scope="scope">
                    <span>{{ scope.row.call.api }}</span>
                    <br />
                    <span>{{ scope.row.call.time | time }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="ioc" label="冲突">
                  <template slot-scope="scope">
                    <span
                      v-html="
                        JSON.stringify(scope.row.call.arguments) != '{}'
                          ? $options.filters.objArrange(
                              scope.row.call.arguments
                            )
                          : '--'
                      "
                    ></span>
                  </template>
                </el-table-column>
                <el-table-column label="状态">
                  <template slot-scope="scope">
                    <span>{{ scope.row.call.status }}个</span>
                  </template>
                </el-table-column>
                <el-table-column label="返回">
                  <template slot-scope="scope">
                    <span>{{ scope.row.call.return_value }}个</span>
                  </template>
                </el-table-column>
                <el-table-column label="重复">
                  <template>
                    <span>0个</span>
                  </template>
                </el-table-column>
              </el-table>
              <el-table
                v-if="signatureData.length !== 0 && signType === 'generic'"
                :data="props.row.children"
                style="width: 100%"
              >
                <el-table-column label="section">
                  <template slot-scope="scope">
                    <span
                      v-html="
                        JSON.stringify(scope.row.section) != '{}'
                          ? scope.row.section
                          : ''
                      "
                    ></span>
                  </template>
                </el-table-column>
                <el-table-column label="entropy">
                  <template slot-scope="scope">
                    <span>{{ scope.row.entropy }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="description">
                  <template slot-scope="scope">
                    <span>{{ scope.row.description }}</span>
                  </template>
                </el-table-column>
              </el-table>
            </template>
          </el-table-column>
          <el-table-column>
            <template slot-scope="scope">
              <span v-html="signatureType(scope.row)"></span>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
      <el-col
        :span="24"
        class="screenShots"
        style="padding: 0;"
        v-if="typefile === 'weapon'"
      >
        <p class="shotTitle">屏幕截图</p>
        <el-collapse v-model="shotsActive" class="shotBox">
          <el-collapse-item
            :title="'截图共' + url.length + '张'"
            name="1"
            class="shotCont"
          >
            <el-image
              v-for="(item, index) in url"
              :key="index"
              class="imglist"
              :src="item"
              :preview-src-list="[item]"
            >
            </el-image>
          </el-collapse-item>
        </el-collapse>
      </el-col>
      <!-- <el-col
        :span="14"
        style="padding: 0;width: calc(58.33333% - 10px);margin-right: 10px;"
      >
        <el-table
          :data="dnsData"
          style="width: 100%"
          border
          :header-cell-style="{ background: '#f5f8ff', color: '#000000' }"
        >
          <el-table-column prop="request" label="名称"> </el-table-column>
          <el-table-column label="响应">
            <template slot-scope="scope">
              <span
                v-html="
                  scope.row.answers.length === 0
                    ? '--'
                    : scope.row.answers[0].data
                "
              ></span>
            </template>
          </el-table-column>
          <el-table-column prop="domainlookups" label="分析后查找">
            <template slot-scope="scope">
              <span
                v-html="
                  scope.row.domainlookups == '' ? '--' : scope.row.domainlookups
                "
              ></span>
            </template>
          </el-table-column>
        </el-table>
      </el-col> -->
      <!-- <el-col :span="10" style="padding: 0;">
        <el-table
          :data="hostData"
          style="width: 100%"
          border
          :header-cell-style="{ background: '#f5f8ff', color: '#000000' }"
        >
          <el-table-column prop="ip" label="IP"> </el-table-column>
          <el-table-column prop="state" label="状态"> </el-table-column>
          <el-table-column prop="Action" label="Action"> </el-table-column>
        </el-table>
      </el-col> -->
    </el-col>
  </el-col>
</template>

<script>
import { weaponFileDetail, taskFileDetail } from "@/api/source";
export default {
  props: { changeList: Number, taskid: String },
  data() {
    return {
      fileDetail: null,
      fileName: "", //文件名
      fileScore: 0, //文件得分
      scorePro: 0, //进度条进度
      summaryList: null,
      actionData: [], //执行信息
      analysisLoglist: [],
      anaslyLog: false,
      antivirusLoglist: [],
      antivirusLog: false,
      signatureData: [],
      // signOpenData:[],
      signType: "",
      shotsActive: ["1"],
      url: [
        // "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
        // "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
        // "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
        // "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
        // "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
        // "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
        // "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg"
      ],
      dnsData: [],
      hostData: [],
      typefile: ""
    };
  },
  watch: {
    changeList: {
      immediate: true,
      handler() {
        this.typefile = window.sessionStorage.getItem("typefile");
        this.summaryload(this.taskid);
      }
    }
  },
  created() {},
  mounted() {
    //监听后退事件
    if (window.history && window.history.pushState) {
      history.pushState(null, null, document.URL);
      window.addEventListener("popstate", this.cancel, false);
    }
  },
  methods: {
    cancel() {
      this.$router.push({
        path: "/apt/antiv/anylize"
      });
    },
    summaryload(taskid) {
      if (this.typefile === "task") {
        taskFileDetail({ id: taskid })
          .then(res => {
            if (res.data.success) {
              let data = res.data.data;
              this.fileName = data.filename;
              this.scorePro = data.score * 10;
              this.fileScore = data.score;
              this.summaryList = data.file;
              this.summaryList.file_id = data.file_id;
              this.actionData.push(data.info);
              let sign = data.signatures;
              for (let i = 0; i < sign.length; i++) {
                sign[i].index = i;
                sign[i].children = [];
              }
              this.signatureData = sign;
              // this.dnsData = data.dns;
              // this.hostData = data.host;
              // let urls = data.url;
              // let urlArr = [];
              // for (let i = 0; i < urls.length; i++) {
              //   urlArr.push(urls[i]);
              // }
              // this.srcList = urlArr;
              // this.url = urlArr;
              // 储存fileid
              // window.sessionStorage.setItem("fileId", data.file_id);
            }
          })
          .catch(error => {
            this.$message.error(error.info);
          });
      } else {
        weaponFileDetail({ cuckoo_task_id: taskid })
          .then(res => {
            if (res.data.success) {
              let data = res.data.data;
              this.fileName = data.filename;
              this.scorePro = data.score * 10;
              this.fileScore = data.score;
              this.summaryList = data.file;
              this.summaryList.file_id = data.file_id;
              this.actionData.push(data.info);
              let sign = data.signatures;
              for (let i = 0; i < sign.length; i++) {
                sign[i].index = i;
                sign[i].children = [];
              }
              this.signatureData = sign;
              // this.dnsData = data.dns;
              // this.hostData = data.host;
              let urls = data.url;
              let urlArr = [];
              for (let i = 0; i < urls.length; i++) {
                urlArr.push(urls[i]);
              }
              this.srcList = urlArr;
              this.url = urlArr;
              //储存fileid
              // window.sessionStorage.setItem("fileId", data.file_id);
            }
          })
          .catch(error => {
            this.$message.error(error.info);
          });
      }
    },
    summaryLogs(task_id, log) {
      if (log === 1) {
        if (!this.anaslyLog) {
          this.$axios({
            method: "POST",
            url: this.$ctx + "/analysis/log",
            data: {
              task_id: task_id,
              log: log
            }
          })
            .then(res => {
              if (res.data.state === 0) {
                this.anaslyLog = true;
                this.analysisLoglist = res.data.data.log;
              }
            })
            .catch(error => {
              this.$message.error(error.info);
            });
        } else {
          this.anaslyLog = false;
        }
      } else if (log === 2) {
        if (!this.antivirusLog) {
          this.$axios({
            method: "POST",
            url: this.$ctx + "/analysis/log",
            data: {
              task_id: task_id,
              log: log
            }
          })
            .then(res => {
              if (res.data.state === 0) {
                this.antivirusLog = true;
                this.antivirusLoglist = res.data.data.log;
              }
            })
            .catch(error => {
              this.$message.error(error.info);
            });
        } else {
          this.antivirusLog = false;
        }
      }
    },
    fileChange(name) {
      if (name != "") {
        let txt = [];
        txt = name.split(".");
        if (txt[1] === undefined) {
          return "文件 " + name;
        }
        if (
          txt[1].toLowerCase() === "zip" ||
          txt[1].toLowerCase() === "rar" ||
          txt[1].toLowerCase() === "7z"
        ) {
          return "压缩包 " + name;
        } else {
          return "文件 " + name;
        }
      } else {
        return name;
      }
    },
    //进度条
    format() {
      return "10分";
    },
    signatureType(row) {
      if (row.severity <= 1) {
        return (
          '<i class="header-icon el-icon-info"></i> ' +
          row.name +
          " (" +
          row.count +
          "个事件)"
        );
      } else if (row.severity == 2) {
        return (
          '<i class="header-icon el-icon-warning"></i> ' +
          row.name +
          " (" +
          row.count +
          "个事件)"
        );
      } else {
        return (
          '<i class="header-icon el-icon-error"></i> ' +
          row.name +
          " (" +
          row.count +
          "个事件)"
        );
      }
    },
    tableRowClassName({ row }) {
      if (row.severity <= 1) {
        return "info";
      } else if (row.severity == 2) {
        return "warning";
      } else {
        return "danger";
      }
    },
    signChange(row) {
      if (row.count === 0) {
        return false;
      } else {
        this.$axios({
          method: "POST",
          url: this.$ctx + "/analysis/Signatures",
          data: {
            task_id: this.taskid,
            index: row.index
          }
        })
          .then(res => {
            if (res.data.state === 0) {
              let data = res.data.data;
              this.signType = data[0].type;
              row.children = data;
            }
          })
          .catch(error => {
            this.$message.error(error.info);
          });
      }
    },
    reboot(file_id) {
      this.$axios({
        method: "POST",
        url: this.$ctx + "/analysis/CreateFile",
        data: {
          file_id: file_id
        }
      })
        .then(res => {
          if (res.data.status === 0) {
            this.$router.push({
              name: "分析任务提交",
              params: {
                taskId: res.data.task_id
              }
            });
          } else {
            this.$message.warning(res.data.info);
          }
        })
        .catch(error => {
          this.$message.error(error.info);
        });
    },
    //反馈
    gotoFeedback() {
      this.$router.push({ path: "/antiv/feedback" });
    }
  },
  destroyed() {
    //删除监听
    window.removeEventListener("popstate", this.cancel, false);
  },
  filters: {
    countSize(limit) {
      let size = "";
      if (limit < 0.1 * 1024) {
        // 小于0.1KB，则转化成B
        size = limit.toFixed(2) + "B";
      } else if (limit < 0.1 * 1024 * 1024) {
        // 小于0.1MB，则转化成KB
        size = (limit / 1024).toFixed(2) + "KB";
      } else if (limit < 0.1 * 1024 * 1024 * 1024) {
        // 小于0.1GB，则转化成MB
        size = (limit / (1024 * 1024)).toFixed(2) + "MB";
      } else {
        // 其他转化成GB
        size = (limit / (1024 * 1024 * 1024)).toFixed(2) + "GB";
      }
      let sizeStr = size + ""; // 转成字符串
      let index = sizeStr.indexOf("."); // 获取小数点处的索引
      let dou = sizeStr.substr(index + 1, 2); // 获取小数点后两位的值
      if (dou == "00") {
        // 判断后两位是否为00，如果是则删除00
        return sizeStr.substring(0, index) + sizeStr.substr(index + 3, 2);
      }
      return size;
    },
    // 将日期过滤为 hour:minutes
    time(date) {
      let arr1 = [];
      let arr2 = [];
      arr1 = date.split(".");
      arr2 = arr1[0].split("T");
      let time = arr2[0] + " " + arr2[1];
      return time;
    },
    objArrange(obj) {
      if (JSON.stringify(obj) !== "{}") {
        let str = "";
        for (let key in obj) {
          str =
            str +
            '<span style="color:#999;">' +
            key +
            ': <span><span style="color:#000;">' +
            obj[key] +
            "<span><br/>";
        }
        return str;
      } else {
        return "--";
      }
    }
  }
};
</script>

<style lang="scss" scoped="scoped">
.summary {
  height: 100%;
  .title {
    height: 50px;
    line-height: 50px;
    font-weight: 600;
    border-bottom: 1px solid #eeeeee;
    padding: 0 25px;
  }
  .summaryCont {
    overflow-y: auto;
    height: calc(100% - 50px);
    &::-webkit-scrollbar {
      /*滚动条整体样式*/
      width: 10px; /*高宽分别对应横竖滚动条的尺寸*/
      height: 1px;
    }
    &::-webkit-scrollbar-thumb {
      /*滚动条里面小方块*/
      border-radius: 10px;
      box-shadow: inset 0 0 5px rgba(153, 153, 153, 0.2);
      background: #b0afaf;
    }
    &::-webkit-scrollbar-track {
      /*滚动条里面轨道*/
      box-shadow: inset 0 0 5px rgba(153, 153, 153, 0.2);
      border-radius: 10px;
      background: #ededed;
    }
    .fileName {
      padding: 10px 0;
      font-weight: 600;
    }
    .fileLeft {
      .detail_box {
        width: calc(100% - 10px);
        border-top: 1px solid #eeeeee;
        border-left: 1px solid #eeeeee;
        li {
          display: table;
          width: 100%;
          .linkBtn {
            display: inline-block;
            line-height: 1;
            white-space: nowrap;
            cursor: pointer;
            border: 1px solid #dcdfe6;
            color: #ffffff;
            background: #90c073;
            border-color: #90c073;
            -webkit-appearance: none;
            text-align: center;
            outline: 0;
            margin-right: 10px;
            font-weight: 500;
            padding: 7px 15px;
            font-size: 12px;
            border-radius: 3px;
          }
          .name {
            display: table-cell;
            padding: 10px 15px;
            width: 20%;
            min-width: 100px;
            background: #f5f8ff;
            font-weight: 600;
            color: #000;
            border-bottom: 1px solid #eeeeee;
            border-right: 1px solid #eeeeee;
          }
          .value {
            display: table-cell;
            width: 80%;
            border-bottom: 1px solid #eeeeee;
            border-right: 1px solid #eeeeee;
            padding: 10px 15px;
            word-break: break-all;
            .el-button {
              &:first-child {
                color: #ffffff;
                background: #90c073;
                border-color: #90c073;
              }
              &:last-child {
                color: #ffffff;
                background: #6e97f1;
                border-color: #6e97f1;
              }
            }
          }
        }
      }
    }
    .fileRight {
      .scoreBox {
        height: 49px;
        line-height: 49px;
        padding-left: 15px;
        border: 1px solid #eeeeee;
        font-size: 16px;
      }
      .scoreTip {
        width: 100%;
        p {
          height: 45px;
          line-height: 45px;
          padding-left: 15px;
          border-left: 1px solid #eeeeee;
          border-right: 1px solid #eeeeee;
        }
        .progressLable {
          float: left;
          width: 45px;
          height: 45px;
          line-height: 45px;
          padding-left: 15px;
          border-left: 1px solid #eeeeee;
          border-bottom: 1px solid #eeeeee;
        }
        .progressCont {
          float: left;
          height: 45px;
          width: calc(100% - 45px);
          padding: 13px 0;
          border-right: 1px solid #eeeeee;
          border-bottom: 1px solid #eeeeee;
        }
        .mark {
          margin-top: 55px;
        }
        .feedback {
          margin-top: 50px;
          .header {
            border: 0;
            padding: 0;
            font-weight: 600;
          }
          .el-button {
            margin-top: 15px;
            width: 150px;
            color: #ffffff;
            background: #6e97f1;
            border-color: #6e97f1;
          }
        }
      }
    }
    .actionMsg {
      margin-top: 10px;
      .actionTitle {
        line-height: 40px;
        font-weight: 600;
      }
      .el-table {
        margin-bottom: 10px;
        .linkBtn {
          color: #6e97f1;
        }
      }
      .analysisLog {
        .an_title {
          padding: 5px 0;
          span {
            color: #bfbfbf;
            margin-right: 5px;
          }
        }
        .logBox {
          padding: 15px;
          border: 1px solid #e5e5e5;
          li {
            line-height: 20px;
          }
        }
      }
    }
    .signatures {
      margin-top: 10px;
      .signTitle {
        line-height: 40px;
        font-weight: 600;
      }
      .noSign {
        padding: 0 15px;
      }
    }
    .screenShots {
      margin-bottom: 15px;
      .shotTitle {
        line-height: 40px;
        font-weight: 600;
      }
      .shotBox {
        border: 1px solid #dcdcdc;
        .shotCont {
          .imglist {
            width: 240px;
            height: 136px;
            margin-right: 10px;
          }
        }
      }
    }
  }
}
</style>
<style lang="scss">
.summary {
  .summaryCont {
    .signatures {
      .signCollapse {
        .header-icon {
          font-size: 16px;
        }
        tr:hover > td {
          background-color: rgba(0, 0, 0, 0.05);
        }
        .info {
          color: #31708f;
          border-color: #bce8f1;
          background-color: #d9edf7;
          font-weight: 600;
        }
        .warning {
          color: #8a6d40;
          border-color: #faebcc;
          background-color: #fcf8e6;
          font-weight: 600;
        }
        .danger {
          color: #a94441;
          border-color: #ebccd1;
          background-color: #f2dede;
          font-weight: 600;
        }
        .el-table__expanded-cell {
          padding: 0;
        }
      }
    }
    .screenShots {
      .shotCont {
        .el-collapse-item__header {
          border-bottom: 1px solid #dcdcdc;
          padding-left: 10px;
        }
        .el-collapse-item__content {
          padding: 20px 0px 20px 20px;
        }
      }
    }
  }
}
</style>
