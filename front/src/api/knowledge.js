import request from "@/request/request";

export function treeList(data) {
  return request({
    method: "get",
    url: "/task/v1/knowledge_lib",
    params: data
  });
}
export function usertypeList() {
  return request({
    method: "get",
    url: "/task/v1/modify_query_label"
  });
}
export function editState(data) {
  return request({
    method: "get",
    url: "/task/v1/edit_note",
    params: data
  });
}
export function notesList(data) {
  return request({
    method: "post",
    url: "/lanegean/knowledge/tesktable",
    data: data
  });
}
export function getTaskDetail(data) {
  return request({
    method: "get",
    url: "/task/v1/knowledge_detail",
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
export function noteBack(data) {
  return request({
    method: "get",
    url: "log/v1/back_data",
    params: data
  });
}
export function noteedit(data) {
  return request({
    method: "post",
    url: "task/v1/modify_query_note",
    data: data
  });
}

//
//
//
//
//
//
//

export function bugList(data) {
  return request({
    method: "post",
    url: "/resource/knowledge/buglist",
    data: data
  });
}
export function workerList(data) {
  return request({
    method: "post",
    url: "/resource/knowledge/workerlist",
    data: data
  });
}
export function noteList(data) {
  return request({
    method: "get",
    url: "/technology/notelist",
    params: data
  });
}
export function delSinKnowledge(data) {
  return request({
    method: "delete",
    url: "/technology/skills",
    data: data
  });
}
export function addWorker(data) {
  return request({
    method: "post",
    url: "/resource/social/add/",
    data: data
  });
}
export function delWorkers(data) {
  return request({
    method: "post",
    url: "/resource/social/delete/",
    data
  });
}
export function socialImport(data) {
  return request({
    method: "post",
    url: "/resource/social/import/",
    headers: {
      "Content-Type": "multipart/form-data"
    },
    data
  });
}

export function addBug(data) {
  return request({
    method: "post",
    url: "/resource/vulnerabilities/create/",
    data: data
  });
}

export function addKnow(data) {
  return request({
    method: "post",
    url: "/technology/skill",
    data
  });
}
// export function getEnumList() {
//   return request({
//     method: "get",
//     url: "/resource/task/taskRoles/hostList"
//   });
// }
export function delBug(data) {
  return request({
    url: "/resource/vulnerabilities/delete/",
    method: "post",
    data: data
  });
}
export function noteDetail(data) {
  return request({
    method: "post",
    url: "/technology/notelist",
    data: data
  });
}
export function userComment(data) {
  return request({
    method: "post",
    url: "/technology/comment",
    data: data
  });
}
export function likeStateChg(data) {
  return request({
    method: "post",
    url: "/technology/changeLike",
    data: data
  });
}
export function cancleteChg(data) {
  return request({
    method: "delete",
    url: "/technology/changeLike",
    data: data
  });
}
