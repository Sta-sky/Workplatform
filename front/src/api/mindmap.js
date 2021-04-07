import request from "@/request/request";
// 创建思维导图
export function createMind(data) {
  return request({
    url: "/mind/create_mind",
    method: "post",
    data: data
  });
}
// 思维导图列表
export function mapList(data) {
  return request({
    url: "/mind/mind_map",
    method: "get",
    params: data
  });
}
// 思维导图端口列表
export function portList(data) {
  return request({
    url: "/mind/node_port_list",
    method: "get",
    params: data
  });
}
// 思维导图端口新增
export function addhostport(data) {
  return request({
    url: "/mind/node_port_list",
    method: "post",
    data: data
  });
}
// 思维导图节点目录列表
export function fileList(data) {
  return request({
    url: "/scan/dirsearch/report",
    method: "post",
    data: data
  });
}
// 思维导图节点脚本编辑
export function fileSave(data) {
  return request({
    url: "/mind/node_file",
    method: "post",
    data: data
  });
}
// 思维导图节点笔记编辑
export function noteSave(data) {
  return request({
    url: "/mind/node_note",
    method: "post",
    data: data
  });
}
// 上传目录文件
export function loadFile(data) {
  return request({
    url: "/scan/dirsearch/import",
    method: "post",
    headers: {
      "Content-Type": "multipart/form-data"
    },
    data: data
  });
}
// 脚本下拉框数据
export function fileslist(data) {
  return request({
    url: "/mind/node_file",
    method: "get",
    params: data
  });
}
// 思维导图节点主机列表
export function hostList(data) {
  return request({
    url: "/mind/host_list_node",
    method: "post",
    data: data
  });
}
// 单个思维导图
export function mapDetail(data) {
  return request({
    url: "/mind/mind_map",
    method: "post",
    data: data
  });
}
// 删除思维导图
export function delSingleNode(data) {
  return request({
    url: "/mind/mind_map",
    method: "delete",
    data: data
  });
}
// 删除端口
export function delport(data) {
  return request({
    url: "/mind/node_port_list",
    method: "delete",
    data: data
  });
}
// 删除目录
export function delFile(data) {
  return request({
    url: "/scan/dirsearch/delete",
    method: "post",
    data: data
  });
}
// 修改节点
export function modifyNode(data) {
  return request({
    url: "/mind/mind_node",
    method: "put",
    data: data
  });
}
// 添加节点
export function addNode(data) {
  return request({
    url: "/mind/mind_node",
    method: "post",
    data: data
  });
}

// 添加目录
export function addfile(data) {
  return request({
    url: "/scan/dirsearch/add",
    method: "post",
    data: data
  });
}
// 删除节点
export function delNode(data) {
  return request({
    url: "/mind/mind_node",
    method: "delete",
    data: data
  });
}
// 断开协同在线
export function disconnect(data) {
  return request({
    url: "/mind/mind_disconnect",
    method: "post",
    data: data
  });
}
// 思维导图节点状态查询 加锁
export function nodeLock(data) {
  return request({
    url: "/mind/lock_node",
    method: "post",
    data: data
  });
}
// 思维导图节点状态查询
export function nodeLockState(data) {
  return request({
    url: "/mind/lock_node",
    method: "put",
    data: data
  });
}
// 思维导图节点解锁
export function nodeUnlock(data) {
  return request({
    url: "/mind/lock_node",
    method: "delete",
    data: data
  });
}
// 节点详情
export function nodedetail(data) {
  return request({
    url: "/mind/node",
    method: "post",
    data: data
  });
}
// 节点搜索
export function nodeSearch(data) {
  return request({
    url: "/mind/node_search",
    method: "post",
    data: data
  });
}
// 待工作列表
export function todoList(data) {
  return request({
    url: "/mind/node_work_list",
    method: "post",
    data: data
  });
}
// 节点工作状态切换
export function nodeWorkChg(data) {
  return request({
    url: "/mind/node_work",
    method: "post",
    data: data
  });
}
export function nodeExtract(data) {
  return request({
    url: "/mind/create_note",
    method: "post",
    data: data
  });
}
export function usertypeList() {
  return request({
    method: "get",
    url: "/user/v1/usertype"
  });
}
export function userDel(data) {
  return request({
    url: "/user/v1/modify_del_user",
    method: "get",
    params: data
  });
}
export function apiDel(data) {
  return request({
    url: "/user/v1/key_create_del",
    method: "get",
    params: data
  });
}
export function apiAdd(data) {
  return request({
    url: "/user/v1/key_create_del",
    method: "post",
    data: data
  });
}
// -----------------------
// -------------------------------------
export function mindLog(data) {
  return request({
    // url:
    //   "http://192.168.8.236:7300/mock/5fbcd1ec415fce0022cf161b/unifyFightPlat/resource/saveMind",
    url: "/mind/e_mind_log",
    method: "get",
    params: data
  });
}
export function singlemindLog(data) {
  return request({
    // url:
    //   "http://192.168.8.236:7300/mock/5fbcd1ec415fce0022cf161b/unifyFightPlat/resource/saveMind",
    url: "/mind/mind_log",
    method: "get",
    params: data
  });
}
export function infoDetail(data, url) {
  return request({
    url: "/scan/" + url,
    method: "post",
    data: data
  });
}
//
//
