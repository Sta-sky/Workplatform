import request from "@/request/request";

export function taskList(data) {
  return request({
    url: "/task/v1/modify_query_task",
    method: "get",
    params: data
  });
}
export function taskDetails(id) {
  return request({
    url: "/task/info",
    method: "post",
    data: { task_id: id }
  });
}
// 笔记&文件搜索
export function taskNoteSearch(data) {
  return request({
    url: "/task/v1/note_file_search",
    method: "get",
    params: data
  });
}
// 详情笔记列表
export function taskNoteTree(data) {
  return request({
    url: "/task/v1/modify_query_subdir",
    method: "get",
    params: data
  });
}
// 笔记--目录操作
export function dirAdd(data) {
  return request({
    url: "/task/v1/add_del_subdir",
    method: "post",
    data: data
  });
}
export function dirEdit(data) {
  return request({
    url: "/task/v1/modify_query_subdir",
    method: "post",
    data: data
  });
}
export function dirDelete(data) {
  return request({
    url: "/task/v1/add_del_subdir",
    method: "get",
    params: data
  });
}
// 笔记--笔记操作
export function taskNotesAdd(data) {
  return request({
    url: "/task/v1/add_del_note",
    method: "post",
    data: data
  });
}
export function taskNotesEdit(data) {
  return request({
    url: "/task/v1/modify_query_note",
    method: "post",
    data: data
  });
}
export function getTaskDetail(data) {
  return request({
    method: "get",
    url: "/task/v1/modify_query_note",
    params: data
  });
}
export function editState(data) {
  return request({
    method: "get",
    url: "/task/v1/edit_note",
    params: data
  });
}
export function delNote(data) {
  return request({
    method: "get",
    url: "/task/v1/add_del_note",
    params: { note_id: data }
  });
}
export function noteedit(data) {
  return request({
    method: "post",
    url: "/task/v1/modify_query_note",
    data: data
  });
}
export function noteBack(data) {
  return request({
    method: "get",
    url: "/back/v1/back_data",
    params: data
  });
}
export function noteUpload(data) {
  return request({
    method: "post",
    url: "/task/v1/upload_notes",
    data: data
  });
}
export function noteLabel() {
  return request({
    method: "get",
    url: "/task/v1/modify_query_label"
  });
}
export function noteExport(data) {
  return request({
    method: "get",
    url: "/task/v1/download_note",
    params: data
  });
}
// 标签操作
export function tagAdd(data) {
  return request({
    method: "post",
    url: "/task/v1/add_del_label",
    data: data
  });
}
export function tagDel(data) {
  return request({
    method: "get",
    url: "/task/v1/add_del_label",
    params: data
  });
}
// 文件--目录操作
export function fileDirAdd(data) {
  return request({
    url: "/file/v1/add_file_dir",
    method: "post",
    data: data
  });
}
export function fileDirEdit(data) {
  return request({
    url: "/file/v1/modify_query_dir",
    method: "post",
    data: data
  });
}
export function fileDirDelete(data) {
  return request({
    url: "/file/v1/add_file_dir",
    method: "get",
    params: data
  });
}
// 文件--操作
export function taskFiles(data) {
  return request({
    url: "/file/v1/modify_query_dir",
    method: "get",
    params: data
  });
}
// 获取漏洞列表
export function taskLeaks(data) {
  return request({
    url: "/task/vulnerability/list",
    method: "get",
    params: data
  });
}
export function addBug(data) {
  return request({
    url: "/task/vulnerability",
    method: "post",
    data: data
  });
}
export function delBug(data) {
  return request({
    url: "/task/vulnerability",
    method: "delete",
    data: data
  });
}
// 获取凭证
export function taskRoles(data) {
  return request({
    url: "/task/certificate/list",
    method: "get",
    params: data
  });
}
export function addProof(data) {
  return request({
    url: "/task/certificate",
    method: "post",
    data: data
  });
}
export function delProof(data) {
  return request({
    url: "/task/certificate",
    method: "delete",
    data: data
  });
}
// 主机列表
export function taskMasters(data) {
  return request({
    url: "/task/host/list",
    method: "post",
    data: data
  });
}
export function optHost(data, method) {
  return request({
    url: "/task/host",
    method: method,
    data: data
  });
}
// 主机-端口获取delHost
export function portDetail(data) {
  return request({
    url: "/task/host/ports",
    method: "get",
    params: data
  });
}
export function portOperation(data, method) {
  return request({
    url: "/task/host/ports",
    method: method,
    data: data
  });
}
export function taskAddArr() {
  return request({
    url: "/task/add",
    method: "get"
  });
}
// 任务操作
export function allUser() {
  return request({
    url: "/user/v1/all_user",
    method: "get"
  });
}
export function taskAdd(data) {
  return request({
    url: "/task/v1/add_del_task",
    method: "post",
    data: data
  });
}
export function taskEdit(data) {
  return request({
    url: "/task/v1/modify_query_task",
    method: "post",
    data: data
  });
}
export function taskDel(data) {
  return request({
    url: "/task/v1/add_del_task",
    method: "get",
    params: data
  });
}
export function fileAdd(data) {
  return request({
    url: "/file/v1/add_del_file",
    method: "post",
    data: data
  });
}
export function fileDel(data) {
  return request({
    url: "/file/v1/add_del_file",
    method: "get",
    params: data
  });
}
export function logDetails(data) {
  return request({
    url: "/log/v1/file_log",
    method: "get",
    params: data
  });
}
export function getTaskReview(id) {
  return request({
    url: "/task/getReview",
    method: "get",
    params: { id }
  });
}
export function sureTaskReview(data) {
  return request({
    url: "/task/getReview",
    method: "post",
    data: data
  });
}
export function getSinTaskScore(id) {
  return request({
    url: "/task/score",
    // url:
    //   "http://192.168.8.236:7300/mock/5fbcd1ec415fce0022cf161b/unifyFightPlat/task/getScore",
    method: "get",
    params: { task_id: id }
  });
}
export function sureChangeScore(data) {
  return request({
    url: "/task/score",
    method: "post",
    data: data
  });
}

// 下载文件
export function taskFileDown(data) {
  return request({
    // url: "/resource/fileManage/detail/",
    url: "/resource/fileManage/analysis/",
    method: "post",
    data
  });
}
// 上传图片
export function uploadImg(data) {
  return request({
    url: "/task/v1/upload_img",
    method: "post",
    data: data
  });
}
export function delImg(data) {
  return request({
    url: "/task/v1/upload_img",
    method: "get",
    params: data
  });
}
// 思维导图列表
export function mindList(data) {
  return request({
    // url:
    //   "http://192.168.8.236:7300/mock/5fbcd1ec415fce0022cf161b/unifyFightPlat/resource/mindList",
    url: "/resource/mindList",
    method: "post",
    data
  });
}

export function sinMindDet(data) {
  return request({
    // url:
    //   "http://192.168.8.236:7300/mock/5fbcd1ec415fce0022cf161b/unifyFightPlat/resource/sinMind",
    url: "/resource/sinMind",
    method: "post",
    data
  });
}

export function delMind(data) {
  return request({
    // url:
    //   "http://192.168.8.236:7300/mock/5fbcd1ec415fce0022cf161b/unifyFightPlat/resource/saveMind",
    url: "/resource/saveMind",
    method: "delete",
    data
  });
}

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
export function infoDetail(data, url) {
  return request({
    url: "/scan/" + url,
    method: "post",
    data: data
  });
}
// 全局搜索
export function allSearch(data) {
  return request({
    url: "/task/v1/allsearch",
    method: "get",
    params: data
  });
}
