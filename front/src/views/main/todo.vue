<template>
  <div
    class="taskView"
    v-loading="listLoading"
    element-loading-text="数据加载中"
    element-loading-background="rgba(0, 0, 0, 0.6)"
  >
    <div class="mainTop">
      <el-row style="margin-bottom: 8px;" :gutter="20">
        <el-col :span="19">
          <span class="englishView">待工作</span>
          <img src="@/assets/img/todo.png" alt="" />
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
        fit
        border
        class="proTable scrollStyle"
        style="width: 100%;"
      >
        <el-table-column
          prop="task_name"
          label="任务名称"
          show-overflow-tooltip
        >
        </el-table-column>
        <el-table-column prop="mind_name" label="导图名称"> </el-table-column>
        <el-table-column prop="name" label="节点名称"></el-table-column>
        <el-table-column prop="create_time" label="标记时间"></el-table-column>
        <!-- <el-table-column label="操作" width="150" fixed="right">
          <template slot-scope="scope">
            <el-button
              title="跳转"
              class="sinProBtn editBtn"
              @click="jumpTo(scope.row)"
            >
              跳转
            </el-button>
          </template>
        </el-table-column> -->
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
</template>
<script>
/* eslint-disable */
import {
  todoList
} from "@/api/mindmap";
export default {
  name: "todo",
  data() {
    return {
      proListData: [],
      search: "",
      page: 1,
      noDataIs:true,
      page_size: 10,
      listLoading:false,
      totalSize: 0,
    };
  },
  computed: {
  },
  watch: {
  },
  mounted() {
    this.getAlltodoList();
  },
  created() {},
  methods: {
    // 获取任务列表
    getAlltodoList() {
      var sendD = {
        search: this.search,
        page: this.page,
        page_size: this.page_size
      };
      this.listLoading = true;
      todoList(sendD)
        .then(response => {
          this.listLoading = false;
          if (response.data.success) {
            this.proListData = response.data.data;
            this.totalSize = response.data.count;
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
        .catch(() => {
          this.listLoading = false;
          // this.$message.error(error.message);
        });
    },
    // 跳转
    jumpTo(val) {
      console.log(val)
    },
    // 关键词搜索
    enterCheck(val) {
      if (val == "") {
        this.page = 1;
        this.page_size = 10;
        this.getAlltodoList();
      }
    },
    clickCheck() {
      if (this.search != "") {
        this.page = 1;
        this.getAlltodoList();
      }
    },
    // 分页
    handleSizeChange(val) {
      this.page_size = val;
      this.getAlltodoList();
    },
    handleCurrentChange(val) {
      this.page = val;
      this.getAlltodoList();
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
